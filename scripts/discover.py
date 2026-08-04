#!/usr/bin/env python3
"""Discover new agent sandbox repos and check staleness of existing entries.

Usage:
    python scripts/discover.py                  # Full run (search + staleness)
    python scripts/discover.py --dry-run        # Print results without creating PRs/issues
    python scripts/discover.py --staleness-only # Only check existing entries for staleness
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = ROOT / "data" / "sandboxes.yaml"
EXCLUDED_PATH = ROOT / "data" / "excluded.yaml"
PEER_LISTS_PATH = ROOT / "data" / "peer-lists.yaml"

GITHUB_API = "https://api.github.com"

# Search queries targeting agent sandbox repos.
# Each runs twice: sorted by recent update AND by stars. The updated sort
# catches new/active repos; the stars sort catches established repos that
# match but weren't pushed recently (per_page=30 windows would otherwise
# hide them behind whatever was pushed this week).
SEARCH_QUERIES = [
    '"agent sandbox" in:name,description,readme',
    '"llm sandbox" in:name,description,readme',
    '"ai sandbox" isolation OR container OR microvm in:readme',
    '"coding agent" sandbox in:readme',
    '"sandbox for ai agents" in:name,description,readme',
    '"agent sandboxing" in:name,description,readme',
]
SEARCH_SORTS = ("updated", "stars")

# Minimum filters for candidates
MIN_STARS = 5
MAX_STALENESS_MONTHS = 12

# Cap on per-run GitHub metadata lookups for peer-list repos, to bound API
# usage. If the cap is hit, the run says so rather than silently truncating.
PEER_METADATA_CAP = 50

# github.com first path segments that are not repo owners
GITHUB_NON_REPO_SEGMENTS = {
    "about", "apps", "collections", "contact", "events", "features",
    "join", "login", "marketplace", "notifications", "orgs", "pricing",
    "search", "settings", "site", "sponsors", "topics", "trending",
}

# Non-GitHub domains that appear in awesome-list markdown but are never
# product pages (badges, social, papers, licenses, community links).
PEER_LINK_SKIP_DOMAINS = {
    "arxiv.org", "awesome.re", "buymeacoffee.com", "creativecommons.org",
    "dev.to", "discord.com", "discord.gg", "docs.google.com", "forms.gle",
    "img.shields.io", "landscape.cncf.io", "medium.com",
    "news.ycombinator.com", "opencollective.com", "opensource.org",
    "reddit.com", "shields.io", "spdx.org", "star-history.com",
    "substack.com", "t.me", "trendshift.io", "twitter.com", "wikipedia.org",
    "x.com", "youtube.com",
}

# Hosts whose Cloudflare JS-challenge protection blocks all automated requests
# regardless of User-Agent or headers. Only a real browser engine can pass.
# Skip staleness checks for these — manual review required if URLs change.
STALENESS_SKIP_HOSTS = {
    "codesandbox.io",
}


def get_headers(token: str | None) -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def load_existing_repos(yaml_path: Path) -> set[str]:
    """Load repo URLs from existing YAML to skip known entries."""
    if not yaml_path.exists():
        return set()
    with open(yaml_path) as f:
        entries = yaml.safe_load(f) or []
    repos = set()
    for entry in entries:
        for field in ("repo_url", "url"):
            val = entry.get(field)
            if val and "github.com" in val.lower():
                # Normalize: strip trailing slashes, lowercase
                repos.add(val.rstrip("/").lower())
    return repos


def load_excluded_repos(excluded_path: Path) -> set[str]:
    """Load repo URLs from the excluded list to skip rejected candidates."""
    if not excluded_path.exists():
        return set()
    with open(excluded_path) as f:
        entries = yaml.safe_load(f) or []
    repos = set()
    for entry in entries:
        val = entry.get("url")
        if val and "github.com" in val.lower():
            repos.add(val.rstrip("/").lower())
    return repos


def search_github(token: str | None) -> list[dict]:
    """Search GitHub for candidate sandbox repos."""
    headers = get_headers(token)
    seen_ids = set()
    candidates = []

    for query in SEARCH_QUERIES:
        for sort in SEARCH_SORTS:
            params = {
                "q": query,
                "sort": sort,
                "order": "desc",
                "per_page": 30,
            }
            resp = requests.get(
                f"{GITHUB_API}/search/repositories",
                headers=headers,
                params=params,
                timeout=30,
            )
            if resp.status_code == 403:
                print(f"Rate limited on query: {query} (sort={sort})", file=sys.stderr)
                continue
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("items", []):
                if item["id"] in seen_ids:
                    continue
                seen_ids.add(item["id"])
                if item.get("stargazers_count", 0) < MIN_STARS:
                    continue
                if not item.get("has_wiki") and not item.get("description"):
                    continue
                candidates.append({
                    "name": item["name"],
                    "full_name": item["full_name"],
                    "description": item.get("description", ""),
                    "url": item["html_url"],
                    "stars": item.get("stargazers_count", 0),
                    "last_push": item.get("pushed_at", ""),
                    "license": (item.get("license") or {}).get("spdx_id", "Unknown"),
                    "topics": item.get("topics", []),
                })

    return candidates


def normalize_url(url: str) -> str:
    """Normalize a URL for comparison: lowercase, no scheme/www/query/fragment,
    no trailing slash."""
    parsed = urlparse(url.strip().lower())
    host = parsed.netloc.removeprefix("www.")
    path = parsed.path.rstrip("/")
    return f"{host}{path}"


def load_all_entry_urls(yaml_path: Path, excluded_path: Path) -> set[str]:
    """Normalized url + repo_url values from both YAML files, GitHub or not."""
    urls = set()
    for path, field_names in ((yaml_path, ("url", "repo_url")), (excluded_path, ("url",))):
        if not path.exists():
            continue
        with open(path) as f:
            entries = yaml.safe_load(f) or []
        for entry in entries:
            for field in field_names:
                val = entry.get(field)
                if val:
                    urls.add(normalize_url(val))
    return urls


def extract_peer_links(markdown: str) -> tuple[set[str], set[str]]:
    """Extract project links from peer-list markdown.

    Returns (github_repo_urls, other_urls). GitHub links are canonicalized to
    https://github.com/owner/repo; badge/social/paper domains are dropped.
    """
    github_repos = set()
    other = set()
    # Markdown links, excluding image links (![alt](src))
    for match in re.finditer(r"(?<!\!)\[[^\]]*\]\((https?://[^)\s]+)\)", markdown):
        url = match.group(1)
        parsed = urlparse(url)
        host = parsed.netloc.lower().removeprefix("www.")
        if host in PEER_LINK_SKIP_DOMAINS:
            continue
        if host == "github.com":
            segments = [s for s in parsed.path.split("/") if s]
            if len(segments) < 2 or segments[0].lower() in GITHUB_NON_REPO_SEGMENTS:
                continue
            owner, repo = segments[0], segments[1]
            # Deep links (blob/issues/releases/...) still identify the repo
            github_repos.add(f"https://github.com/{owner}/{repo}")
        elif host.endswith(".github.com") or host == "gist.github.com":
            continue
        else:
            other.add(f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}")
    return github_repos, other


def load_peer_lists(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path) as f:
        return yaml.safe_load(f) or []


def crosscheck_peer_lists(token: str | None, known_urls: set[str]) -> tuple[list[dict], list[dict]]:
    """Diff peer-list project links against known URLs.

    Returns (github_candidates, other_links). GitHub candidates get repo
    metadata fetched (no star filter — peer curation is signal enough) and a
    "source" key naming the peer list. Other links are {url, source} dicts
    for manual review, since non-GitHub products have no API to query.
    """
    headers = get_headers(token)
    github_candidates: list[dict] = []
    other_links: list[dict] = []
    seen_repos: set[str] = set()
    metadata_budget = PEER_METADATA_CAP

    for peer in load_peer_lists(PEER_LISTS_PATH):
        name, raw_url = peer.get("name", "?"), peer.get("raw_url")
        if not raw_url:
            continue
        try:
            resp = requests.get(raw_url, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Peer list {name}: fetch failed ({e})", file=sys.stderr)
            continue

        repos, others = extract_peer_links(resp.text)

        for url in sorted(others):
            if normalize_url(url) not in known_urls:
                other_links.append({"url": url, "source": name})

        for repo_url in sorted(repos):
            norm = normalize_url(repo_url)
            if norm in known_urls or norm in seen_repos:
                continue
            seen_repos.add(norm)
            if metadata_budget <= 0:
                print(
                    f"Peer metadata cap ({PEER_METADATA_CAP}) hit — "
                    f"skipping metadata for {repo_url} and any further peer repos",
                    file=sys.stderr,
                )
                github_candidates.append({
                    "name": repo_url.split("/")[-1],
                    "full_name": "/".join(repo_url.split("/")[-2:]),
                    "description": "(metadata not fetched — peer cap hit)",
                    "url": repo_url,
                    "stars": 0,
                    "last_push": "",
                    "license": "Unknown",
                    "topics": [],
                    "source": name,
                })
                continue
            metadata_budget -= 1
            owner_repo = "/".join(repo_url.split("/")[-2:])
            r = requests.get(f"{GITHUB_API}/repos/{owner_repo}", headers=headers, timeout=30)
            if r.status_code != 200:
                # Dead or renamed link in the peer list — still worth a look
                github_candidates.append({
                    "name": repo_url.split("/")[-1],
                    "full_name": owner_repo,
                    "description": f"(GitHub API returned {r.status_code})",
                    "url": repo_url,
                    "stars": 0,
                    "last_push": "",
                    "license": "Unknown",
                    "topics": [],
                    "source": name,
                })
                continue
            item = r.json()
            github_candidates.append({
                "name": item["name"],
                "full_name": item["full_name"],
                "description": item.get("description") or "",
                "url": item["html_url"],
                "stars": item.get("stargazers_count", 0),
                "last_push": item.get("pushed_at", ""),
                "license": (item.get("license") or {}).get("spdx_id", "Unknown"),
                "topics": item.get("topics", []),
                "source": name,
            })

    return github_candidates, other_links


def filter_new_candidates(candidates: list[dict], known_repos: set[str]) -> list[dict]:
    """Remove candidates that are already in the YAML."""
    new = []
    for c in candidates:
        url_lower = c["url"].rstrip("/").lower()
        if url_lower not in known_repos:
            new.append(c)
    return new


def check_staleness(token: str | None, yaml_path: Path) -> list[dict]:
    """Check existing entries for staleness (404s, old commits)."""
    if not yaml_path.exists():
        return []
    with open(yaml_path) as f:
        entries = yaml.safe_load(f) or []

    headers = get_headers(token)
    stale = []
    now = datetime.now(timezone.utc)

    for entry in entries:
        repo_url = entry.get("repo_url")
        if not repo_url or "github.com" not in repo_url:
            continue

        # Extract owner/repo from URL
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            continue
        owner, repo = parts[-2], parts[-1]

        resp = requests.get(
            f"{GITHUB_API}/repos/{owner}/{repo}",
            headers=headers,
            timeout=30,
        )

        if resp.status_code == 404:
            stale.append({
                "name": entry["name"],
                "url": repo_url,
                "reason": "Repository not found (404)",
            })
            continue
        elif resp.status_code == 403:
            continue  # Rate limited, skip
        elif resp.status_code != 200:
            continue

        data = resp.json()
        pushed_at = data.get("pushed_at")
        if pushed_at:
            last_push = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
            months_since = (now - last_push).days / 30
            if months_since > MAX_STALENESS_MONTHS:
                stale.append({
                    "name": entry["name"],
                    "url": repo_url,
                    "reason": f"No commits in {int(months_since)} months (last: {pushed_at[:10]})",
                })

        if data.get("archived"):
            stale.append({
                "name": entry["name"],
                "url": repo_url,
                "reason": "Repository is archived",
            })

    # Also check non-GitHub URLs. Use a browser-like User-Agent because
    # some sites (e.g., CodeSandbox) reject the default python-requests
    # UA. Fall back to GET if HEAD is rejected, since some servers don't
    # support HEAD at all.
    browser_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }
    for entry in entries:
        url = entry.get("url")
        if not url or "github.com" in url.lower():
            continue
        if any(host in url.lower() for host in STALENESS_SKIP_HOSTS):
            continue
        status = None
        try:
            resp = requests.head(
                url, timeout=15, allow_redirects=True, headers=browser_headers
            )
            status = resp.status_code
            if status >= 400:
                # Retry with GET — many sites only return useful status on GET
                resp = requests.get(
                    url, timeout=15, allow_redirects=True, headers=browser_headers
                )
                status = resp.status_code
        except requests.RequestException:
            stale.append({
                "name": entry["name"],
                "url": url,
                "reason": "URL unreachable",
            })
            continue

        if status is not None and status >= 400:
            stale.append({
                "name": entry["name"],
                "url": url,
                "reason": f"URL returned HTTP {status}",
            })

    return stale


def format_candidates_md(candidates: list[dict], peer_links: list[dict] | None = None) -> str:
    """Format new candidates as markdown for a PR body."""
    if not candidates and not peer_links:
        return "No new candidates found.\n"

    lines = ["## New Sandbox Candidates\n"]
    if candidates:
        lines.append(f"Found {len(candidates)} repo(s) not yet in `data/sandboxes.yaml`.\n")
        lines.append("| Repository | Stars | Last Push | License | Description |")
        lines.append("|------------|-------|-----------|---------|-------------|")

        for c in sorted(candidates, key=lambda x: x["stars"], reverse=True):
            push_date = c["last_push"][:10] if c["last_push"] else "Unknown"
            desc = (c["description"] or "")[:100]
            if c.get("source"):
                desc = f"[peer: {c['source']}] {desc}"[:130]
            lines.append(
                f"| [{c['full_name']}]({c['url']}) | {c['stars']} "
                f"| {push_date} | {c['license']} | {desc} |"
            )

    if peer_links:
        lines.append("\n### Peer-list projects without a GitHub repo\n")
        lines.append(
            f"{len(peer_links)} link(s) found in peer lists but not in our data — "
            "likely hosted/proprietary products. Manual review needed.\n"
        )
        lines.append("| URL | Peer list |")
        lines.append("|-----|-----------|")
        for link in peer_links:
            lines.append(f"| {link['url']} | {link['source']} |")

    lines.append("\nReview each candidate and add to `data/sandboxes.yaml` if appropriate.")
    return "\n".join(lines)


def format_staleness_md(stale: list[dict]) -> str:
    """Format staleness report as markdown for an issue body."""
    if not stale:
        return "All existing entries are healthy.\n"

    lines = ["## Staleness Report\n"]
    lines.append(f"Found {len(stale)} issue(s) with existing entries.\n")
    lines.append("| Entry | URL | Issue |")
    lines.append("|-------|-----|-------|")

    for s in stale:
        lines.append(f"| {s['name']} | {s['url']} | {s['reason']} |")

    lines.append("\nReview each entry and update or remove as appropriate.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Discover new agent sandbox repos")
    parser.add_argument("--dry-run", action="store_true", help="Print results without side effects")
    parser.add_argument("--staleness-only", action="store_true", help="Only check staleness")
    parser.add_argument("--token", help="GitHub token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--output-dir", help="Write markdown files to this directory")
    args = parser.parse_args()

    import os
    token = args.token or os.environ.get("GITHUB_TOKEN")

    if not args.staleness_only:
        print("Searching for new sandbox repos...")
        candidates = search_github(token)
        known = load_existing_repos(YAML_PATH)
        excluded = load_excluded_repos(EXCLUDED_PATH)
        new_candidates = filter_new_candidates(candidates, known | excluded)

        print("Cross-checking peer lists...")
        all_known_urls = load_all_entry_urls(YAML_PATH, EXCLUDED_PATH)
        peer_candidates, peer_links = crosscheck_peer_lists(token, all_known_urls)
        # Merge peer repos not already surfaced by search
        surfaced = {c["url"].rstrip("/").lower() for c in new_candidates}
        for pc in peer_candidates:
            if pc["url"].rstrip("/").lower() not in surfaced:
                new_candidates.append(pc)
        print(
            f"Peer lists: {len(peer_candidates)} new GitHub repo(s), "
            f"{len(peer_links)} non-GitHub link(s)."
        )

        candidates_md = format_candidates_md(new_candidates, peer_links)
        print(f"Found {len(new_candidates)} new candidate(s) from {len(candidates)} total results.")

        if args.dry_run:
            print("\n--- Candidates ---")
            print(candidates_md)
        elif args.output_dir:
            out = Path(args.output_dir)
            out.mkdir(parents=True, exist_ok=True)
            (out / "candidates.md").write_text(candidates_md)
            (out / "candidates.json").write_text(json.dumps(new_candidates, indent=2))
            print(f"Wrote candidates to {out}")

    print("\nChecking staleness of existing entries...")
    stale = check_staleness(token, YAML_PATH)
    staleness_md = format_staleness_md(stale)
    print(f"Found {len(stale)} staleness issue(s).")

    if args.dry_run:
        print("\n--- Staleness ---")
        print(staleness_md)
    elif args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "staleness.md").write_text(staleness_md)
        print(f"Wrote staleness report to {out}")


if __name__ == "__main__":
    main()
