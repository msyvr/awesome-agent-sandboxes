"""Tests for scripts/discover.py — no network calls."""

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from discover import (
    extract_peer_links,
    filter_new_candidates,
    format_candidates_md,
    format_staleness_md,
    load_all_entry_urls,
    is_known_url,
    load_excluded_repos,
    load_existing_repos,
    normalize_url,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_candidate(**overrides):
    base = {
        "name": "test-repo",
        "full_name": "org/test-repo",
        "description": "A sandbox tool",
        "url": "https://github.com/org/test-repo",
        "stars": 42,
        "last_push": "2026-04-01T00:00:00Z",
        "license": "MIT",
        "topics": ["sandbox"],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# load_existing_repos
# ---------------------------------------------------------------------------

class TestLoadExistingRepos:
    def test_loads_repo_urls(self, tmp_path):
        data = [
            {"name": "A", "repo_url": "https://github.com/org/a", "url": "https://a.com"},
            {"name": "B", "repo_url": "https://github.com/org/b", "url": "https://b.com"},
        ]
        yaml_file = tmp_path / "entries.yaml"
        yaml_file.write_text(yaml.dump(data))
        repos = load_existing_repos(yaml_file)
        assert "https://github.com/org/a" in repos
        assert "https://github.com/org/b" in repos

    def test_loads_github_urls_from_url_field(self, tmp_path):
        data = [{"name": "A", "url": "https://github.com/org/a"}]
        yaml_file = tmp_path / "entries.yaml"
        yaml_file.write_text(yaml.dump(data))
        repos = load_existing_repos(yaml_file)
        assert "https://github.com/org/a" in repos

    def test_ignores_non_github_urls(self, tmp_path):
        data = [{"name": "A", "url": "https://example.com", "repo_url": None}]
        yaml_file = tmp_path / "entries.yaml"
        yaml_file.write_text(yaml.dump(data))
        repos = load_existing_repos(yaml_file)
        assert len(repos) == 0

    def test_normalizes_trailing_slash(self, tmp_path):
        data = [{"name": "A", "repo_url": "https://github.com/org/a/"}]
        yaml_file = tmp_path / "entries.yaml"
        yaml_file.write_text(yaml.dump(data))
        repos = load_existing_repos(yaml_file)
        assert "https://github.com/org/a" in repos

    def test_normalizes_case(self, tmp_path):
        data = [{"name": "A", "repo_url": "https://GitHub.com/Org/Repo"}]
        yaml_file = tmp_path / "entries.yaml"
        yaml_file.write_text(yaml.dump(data))
        repos = load_existing_repos(yaml_file)
        assert "https://github.com/org/repo" in repos

    def test_missing_file_returns_empty(self, tmp_path):
        repos = load_existing_repos(tmp_path / "nonexistent.yaml")
        assert repos == set()

    def test_empty_yaml_returns_empty(self, tmp_path):
        yaml_file = tmp_path / "entries.yaml"
        yaml_file.write_text("")
        repos = load_existing_repos(yaml_file)
        assert repos == set()


# ---------------------------------------------------------------------------
# load_excluded_repos
# ---------------------------------------------------------------------------

class TestLoadExcludedRepos:
    def test_loads_urls(self, tmp_path):
        data = [
            {"url": "https://github.com/org/rejected1", "reason": "Not a sandbox"},
            {"url": "https://github.com/org/rejected2", "reason": "Agent framework"},
        ]
        yaml_file = tmp_path / "excluded.yaml"
        yaml_file.write_text(yaml.dump(data))
        repos = load_excluded_repos(yaml_file)
        assert "https://github.com/org/rejected1" in repos
        assert "https://github.com/org/rejected2" in repos

    def test_normalizes_case(self, tmp_path):
        data = [{"url": "https://GitHub.com/Org/Repo", "reason": "test"}]
        yaml_file = tmp_path / "excluded.yaml"
        yaml_file.write_text(yaml.dump(data))
        repos = load_excluded_repos(yaml_file)
        assert "https://github.com/org/repo" in repos

    def test_missing_file_returns_empty(self, tmp_path):
        repos = load_excluded_repos(tmp_path / "nonexistent.yaml")
        assert repos == set()

    def test_empty_yaml_returns_empty(self, tmp_path):
        yaml_file = tmp_path / "excluded.yaml"
        yaml_file.write_text("")
        repos = load_excluded_repos(yaml_file)
        assert repos == set()

    def test_filters_candidates_when_combined(self):
        """Excluded repos should be filtered out alongside known repos."""
        known = {"https://github.com/org/known"}
        excluded = {"https://github.com/org/rejected"}
        candidates = [
            make_candidate(url="https://github.com/org/known"),
            make_candidate(name="rejected", url="https://github.com/org/rejected"),
            make_candidate(name="new", url="https://github.com/org/new"),
        ]
        result = filter_new_candidates(candidates, known | excluded)
        assert len(result) == 1
        assert result[0]["name"] == "new"

    def test_real_excluded_yaml_parses(self):
        """The actual excluded.yaml should parse without errors."""
        excluded_path = Path(__file__).resolve().parent.parent / "data" / "excluded.yaml"
        repos = load_excluded_repos(excluded_path)
        assert len(repos) > 0, "Expected at least some excluded repos"


# ---------------------------------------------------------------------------
# filter_new_candidates
# ---------------------------------------------------------------------------

class TestFilterNewCandidates:
    def test_filters_known_repos(self):
        known = {"https://github.com/org/known"}
        candidates = [
            make_candidate(url="https://github.com/org/known"),
            make_candidate(name="new", url="https://github.com/org/new"),
        ]
        result = filter_new_candidates(candidates, known)
        assert len(result) == 1
        assert result[0]["name"] == "new"

    def test_case_insensitive_match(self):
        known = {"https://github.com/org/repo"}
        candidates = [make_candidate(url="https://github.com/Org/Repo")]
        result = filter_new_candidates(candidates, known)
        assert len(result) == 0

    def test_trailing_slash_match(self):
        known = {"https://github.com/org/repo"}
        candidates = [make_candidate(url="https://github.com/org/repo/")]
        result = filter_new_candidates(candidates, known)
        assert len(result) == 0

    def test_empty_known_returns_all(self):
        candidates = [make_candidate(), make_candidate(name="b", url="https://github.com/org/b")]
        result = filter_new_candidates(candidates, set())
        assert len(result) == 2

    def test_empty_candidates_returns_empty(self):
        result = filter_new_candidates([], {"https://github.com/org/a"})
        assert result == []


# ---------------------------------------------------------------------------
# format_candidates_md
# ---------------------------------------------------------------------------

class TestFormatCandidatesMd:
    def test_empty_candidates(self):
        result = format_candidates_md([])
        assert "No new candidates found" in result

    def test_renders_table(self):
        candidates = [make_candidate(full_name="org/tool", stars=100)]
        result = format_candidates_md(candidates)
        assert "| Repository |" in result
        assert "[org/tool]" in result
        assert "100" in result

    def test_sorted_by_stars_descending(self):
        candidates = [
            make_candidate(full_name="org/low", stars=10),
            make_candidate(full_name="org/high", stars=1000, url="https://github.com/org/high"),
        ]
        result = format_candidates_md(candidates)
        lines = result.split("\n")
        data_lines = [l for l in lines if l.startswith("| [")]
        assert "org/high" in data_lines[0]
        assert "org/low" in data_lines[1]

    def test_truncates_long_description(self):
        long_desc = "x" * 200
        candidates = [make_candidate(description=long_desc)]
        result = format_candidates_md(candidates)
        # Should be truncated to 100 chars
        assert "x" * 101 not in result

    def test_handles_missing_push_date(self):
        candidates = [make_candidate(last_push="")]
        result = format_candidates_md(candidates)
        assert "Unknown" in result

    def test_includes_count(self):
        candidates = [make_candidate(), make_candidate(name="b", url="https://github.com/org/b")]
        result = format_candidates_md(candidates)
        assert "Found 2 repo(s)" in result

    def test_peer_links_section(self):
        peer_links = [{"url": "https://leap0.dev", "source": "some-list"}]
        result = format_candidates_md([], peer_links)
        assert "Peer-list projects without a GitHub repo" in result
        assert "https://leap0.dev" in result
        assert "some-list" in result
        assert "No new candidates found" not in result

    def test_peer_sourced_candidate_tagged(self):
        result = format_candidates_md([make_candidate(source="some-list")])
        assert "[peer: some-list]" in result

    def test_empty_both_says_no_candidates(self):
        assert "No new candidates found" in format_candidates_md([], [])


# ---------------------------------------------------------------------------
# normalize_url / extract_peer_links / load_all_entry_urls
# ---------------------------------------------------------------------------

class TestNormalizeUrl:
    def test_strips_scheme_www_slash_case(self):
        assert normalize_url("HTTPS://WWW.GitHub.com/Org/Repo/") == "github.com/org/repo"

    def test_strips_query_and_fragment(self):
        assert normalize_url("https://a.dev/x?utm=1#top") == "a.dev/x"

    def test_http_https_equal(self):
        assert normalize_url("http://a.dev/x") == normalize_url("https://a.dev/x")


class TestExtractPeerLinks:
    def test_github_repo_link(self):
        repos, other = extract_peer_links("[x](https://github.com/org/repo)")
        assert repos == {"https://github.com/org/repo"}
        assert other == set()

    def test_deep_github_link_canonicalized(self):
        repos, _ = extract_peer_links("[x](https://github.com/org/repo/blob/main/README.md)")
        assert repos == {"https://github.com/org/repo"}

    def test_non_repo_github_paths_skipped(self):
        repos, _ = extract_peer_links(
            "[a](https://github.com/topics/sandbox) [b](https://github.com/orgs/foo)"
        )
        assert repos == set()

    def test_badge_domains_skipped(self):
        repos, other = extract_peer_links(
            "[a](https://img.shields.io/badge/x) [b](https://awesome.re/badge.svg)"
        )
        assert repos == set() and other == set()

    def test_image_links_skipped(self):
        repos, other = extract_peer_links("![logo](https://example.com/logo.png)")
        assert repos == set() and other == set()

    def test_product_site_captured(self):
        _, other = extract_peer_links("[Leap0](https://leap0.dev)")
        assert other == {"https://leap0.dev"}


class TestLoadAllEntryUrls:
    def test_collects_both_files_and_fields(self, tmp_path):
        main = tmp_path / "sandboxes.yaml"
        main.write_text(
            "- name: a\n  url: https://a.dev/\n  repo_url: https://github.com/org/a\n"
        )
        excl = tmp_path / "excluded.yaml"
        excl.write_text("- url: https://github.com/org/b\n  reason: x\n")
        urls = load_all_entry_urls(main, excl)
        assert urls == {"a.dev", "host:a.dev", "github.com/org/a", "github.com/org/b"}

    def test_missing_files_return_empty(self, tmp_path):
        assert load_all_entry_urls(tmp_path / "x.yaml", tmp_path / "y.yaml") == set()

    def test_product_path_also_indexes_bare_host(self, tmp_path):
        main = tmp_path / "sandboxes.yaml"
        main.write_text("- name: m\n  url: https://modal.com/products/sandboxes\n")
        excl = tmp_path / "excluded.yaml"
        excl.write_text("[]\n")
        urls = load_all_entry_urls(main, excl)
        assert "modal.com/products/sandboxes" in urls
        assert "host:modal.com" in urls

    def test_github_repo_url_does_not_index_host(self, tmp_path):
        main = tmp_path / "sandboxes.yaml"
        main.write_text("- name: g\n  repo_url: https://github.com/org/a\n")
        excl = tmp_path / "excluded.yaml"
        excl.write_text("[]\n")
        assert "host:github.com" not in load_all_entry_urls(main, excl)


class TestIsKnownUrl:
    known = {"modal.com/products/sandboxes", "host:modal.com", "github.com/org/a"}

    def test_exact_match(self):
        assert is_known_url("https://modal.com/products/sandboxes", self.known)

    def test_bare_home_page_matches_listed_product_path(self):
        assert is_known_url("https://modal.com", self.known)
        assert is_known_url("https://www.modal.com/", self.known)

    def test_other_product_under_known_host_still_surfaces(self):
        assert not is_known_url("https://modal.com/products/something-else", self.known)

    def test_unknown_host(self):
        assert not is_known_url("https://brand-new-vendor.dev", self.known)

    def test_deep_link_under_known_path(self):
        known = {"kvcache-ai.github.io/agentenv/latest"}
        assert is_known_url(
            "https://kvcache-ai.github.io/AgentENV/latest/concepts/sandboxes.html", known
        )

    def test_sibling_path_is_not_a_prefix_match(self):
        known = {"a.dev/product/sandbox"}
        assert not is_known_url("https://a.dev/product/sandbox-v2", known)


# ---------------------------------------------------------------------------
# format_staleness_md
# ---------------------------------------------------------------------------

class TestFormatStalenessMd:
    def test_empty_stale(self):
        result = format_staleness_md([])
        assert "All existing entries are healthy" in result

    def test_renders_table(self):
        stale = [{"name": "OldTool", "url": "https://github.com/x/y", "reason": "404"}]
        result = format_staleness_md(stale)
        assert "| Entry |" in result
        assert "OldTool" in result
        assert "404" in result

    def test_includes_count(self):
        stale = [
            {"name": "A", "url": "https://a.com", "reason": "stale"},
            {"name": "B", "url": "https://b.com", "reason": "archived"},
        ]
        result = format_staleness_md(stale)
        assert "Found 2 issue(s)" in result


# ---------------------------------------------------------------------------
# Integration: validate real YAML
# ---------------------------------------------------------------------------

class TestRealYaml:
    def test_real_yaml_validates(self):
        """The actual sandboxes.yaml should pass validation."""
        from generate_readme import validate_all
        yaml_path = Path(__file__).resolve().parent.parent / "data" / "sandboxes.yaml"
        with open(yaml_path) as f:
            entries = yaml.safe_load(f)
        errors = validate_all(entries)
        assert errors == [], f"Validation errors in sandboxes.yaml:\n" + "\n".join(errors)

    def test_real_yaml_has_entries(self):
        yaml_path = Path(__file__).resolve().parent.parent / "data" / "sandboxes.yaml"
        with open(yaml_path) as f:
            entries = yaml.safe_load(f)
        assert len(entries) >= 40, f"Expected at least 40 entries, got {len(entries)}"

    def test_real_yaml_all_categories_used(self):
        """Every category in the vocabulary should have at least one entry."""
        from generate_readme import VALID_CATEGORIES
        yaml_path = Path(__file__).resolve().parent.parent / "data" / "sandboxes.yaml"
        with open(yaml_path) as f:
            entries = yaml.safe_load(f)
        used_categories = {e["category"] for e in entries}
        for cat in VALID_CATEGORIES:
            assert cat in used_categories, f"Category '{cat}' has no entries"

    def test_real_yaml_no_duplicate_names(self):
        yaml_path = Path(__file__).resolve().parent.parent / "data" / "sandboxes.yaml"
        with open(yaml_path) as f:
            entries = yaml.safe_load(f)
        names = [e["name"] for e in entries]
        assert len(names) == len(set(names)), f"Duplicate names: {[n for n in names if names.count(n) > 1]}"

    def test_real_yaml_load_existing_repos(self):
        """load_existing_repos should parse the real YAML without errors."""
        yaml_path = Path(__file__).resolve().parent.parent / "data" / "sandboxes.yaml"
        repos = load_existing_repos(yaml_path)
        assert len(repos) > 0, "Expected at least some GitHub URLs in entries"
