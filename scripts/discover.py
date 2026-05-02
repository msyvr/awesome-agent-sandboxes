#!/usr/bin/env python3
"""Discover new agent sandbox repos and check staleness of existing entries.

Usage:
    python scripts/discover.py                  # Full run (search + staleness)
    python scripts/discover.py --dry-run        # Print results without creating PRs/issues
    python scripts/discover.py --staleness-only # Only check existing entries for staleness
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = ROOT / "data" / "sandboxes.yaml"
EXCLUDED_PATH = ROOT / "data" / "excluded.yaml"

GITHUB_API = "https://api.github.com"

# Search queries targeting agent sandbox repos
SEARCH_QUERIES = [
    '"agent sandbox" in:name,description,readme',
    '"llm sandbox" in:name,description,readme',
    '"ai sandbox" isolation OR container OR microvm in:readme',
    '"coding agent" sandbox in:readme',
]

# Minimum filters for candidates
MIN_STARS = 5
MAX_STALENESS_MONTHS = 12

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
        params = {
            "q": query,
            "sort": "updated",
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
            print(f"Rate limited on query: {query}", file=sys.stderr)
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


def format_candidates_md(candidates: list[dict]) -> str:
    """Format new candidates as markdown for a PR body."""
    if not candidates:
        return "No new candidates found.\n"

    lines = ["## New Sandbox Candidates\n"]
    lines.append(f"Found {len(candidates)} repo(s) not yet in `data/sandboxes.yaml`.\n")
    lines.append("| Repository | Stars | Last Push | License | Description |")
    lines.append("|------------|-------|-----------|---------|-------------|")

    for c in sorted(candidates, key=lambda x: x["stars"], reverse=True):
        push_date = c["last_push"][:10] if c["last_push"] else "Unknown"
        desc = (c["description"] or "")[:100]
        lines.append(
            f"| [{c['full_name']}]({c['url']}) | {c['stars']} "
            f"| {push_date} | {c['license']} | {desc} |"
        )

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
        candidates_md = format_candidates_md(new_candidates)
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
