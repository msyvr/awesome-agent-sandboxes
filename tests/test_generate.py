"""Tests for scripts/generate_readme.py"""

import sys
from pathlib import Path

import pytest

# Add scripts/ to path so we can import the module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from generate_readme import (
    VALID_CATEGORIES,
    VALID_ISOLATION_TYPES,
    VALID_ISOLATION_TIERS,
    VALID_ADOPTION_EFFORTS,
    VALID_DEPLOYMENT_MODELS,
    ADOPTION_EFFORT_ORDER,
    CATEGORY_ORDER,
    validate_entry,
    validate_all,
    escape_md,
    format_list_short,
    generate_lens_table,
    generate_category_table,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_entry(**overrides):
    """Create a minimal valid entry, with overrides."""
    base = {
        "name": "TestSandbox",
        "category": "standalone",
        "maintainer": "Test Corp",
        "open_source": True,
        "license": "MIT",
        "url": "https://example.com",
        "repo_url": "https://github.com/test/sandbox",
        "description": "A test sandbox.",
        "isolation_type": ["container"],
        "capabilities": ["cap1", "cap2"],
        "requirements": ["req1"],
        "limitations": ["lim1"],
        "notes": "Some notes.",
        "isolation_tier": "container",
        "adoption_effort": "install",
        "deployment_model": "local",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Validation: valid entries
# ---------------------------------------------------------------------------

class TestValidateEntry:
    def test_valid_entry_passes(self):
        assert validate_entry(make_entry(), 0) == []

    def test_valid_entry_with_null_optional_fields(self):
        entry = make_entry(license=None, url=None, repo_url=None, notes=None)
        assert validate_entry(entry, 0) == []

    def test_valid_entry_multiple_isolation_types(self):
        entry = make_entry(isolation_type=["kvm", "microvm", "seccomp"])
        assert validate_entry(entry, 0) == []

    # ---------------------------------------------------------------------------
    # Validation: missing required fields
    # ---------------------------------------------------------------------------

    def test_missing_name(self):
        entry = make_entry()
        del entry["name"]
        errors = validate_entry(entry, 0)
        assert any("missing required field 'name'" in e for e in errors)

    def test_missing_category(self):
        entry = make_entry()
        del entry["category"]
        errors = validate_entry(entry, 0)
        assert any("missing required field 'category'" in e for e in errors)

    def test_missing_isolation_type(self):
        entry = make_entry()
        del entry["isolation_type"]
        errors = validate_entry(entry, 0)
        assert any("missing required field 'isolation_type'" in e for e in errors)

    def test_missing_lens_tags(self):
        entry = make_entry()
        del entry["isolation_tier"]
        del entry["adoption_effort"]
        del entry["deployment_model"]
        errors = validate_entry(entry, 0)
        assert len(errors) == 3
        assert any("isolation_tier" in e for e in errors)
        assert any("adoption_effort" in e for e in errors)
        assert any("deployment_model" in e for e in errors)

    def test_null_required_field(self):
        entry = make_entry(category=None)
        errors = validate_entry(entry, 0)
        assert any("missing required field 'category'" in e for e in errors)

    # ---------------------------------------------------------------------------
    # Validation: controlled vocabularies
    # ---------------------------------------------------------------------------

    def test_invalid_category(self):
        entry = make_entry(category="invalid-cat")
        errors = validate_entry(entry, 0)
        assert any("invalid category 'invalid-cat'" in e for e in errors)

    def test_invalid_isolation_type(self):
        entry = make_entry(isolation_type=["invalid"])
        errors = validate_entry(entry, 0)
        assert any("invalid isolation_type 'invalid'" in e for e in errors)

    def test_invalid_isolation_tier(self):
        entry = make_entry(isolation_tier="invalid")
        errors = validate_entry(entry, 0)
        assert any("invalid isolation_tier 'invalid'" in e for e in errors)

    def test_invalid_adoption_effort(self):
        entry = make_entry(adoption_effort="invalid")
        errors = validate_entry(entry, 0)
        assert any("invalid adoption_effort 'invalid'" in e for e in errors)

    def test_invalid_deployment_model(self):
        entry = make_entry(deployment_model="invalid")
        errors = validate_entry(entry, 0)
        assert any("invalid deployment_model 'invalid'" in e for e in errors)

    def test_all_valid_categories_accepted(self):
        for cat in VALID_CATEGORIES:
            assert validate_entry(make_entry(category=cat), 0) == []

    def test_all_valid_isolation_types_accepted(self):
        for it in VALID_ISOLATION_TYPES:
            assert validate_entry(make_entry(isolation_type=[it]), 0) == []

    def test_all_valid_isolation_tiers_accepted(self):
        for tier in VALID_ISOLATION_TIERS:
            assert validate_entry(make_entry(isolation_tier=tier), 0) == []

    # ---------------------------------------------------------------------------
    # Validation: type checks
    # ---------------------------------------------------------------------------

    def test_isolation_type_must_be_list(self):
        entry = make_entry(isolation_type="container")
        errors = validate_entry(entry, 0)
        assert any("isolation_type must be a list" in e for e in errors)

    def test_capabilities_must_be_list(self):
        entry = make_entry(capabilities="not a list")
        errors = validate_entry(entry, 0)
        assert any("'capabilities' must be a list" in e for e in errors)

    def test_requirements_must_be_list(self):
        entry = make_entry(requirements="not a list")
        errors = validate_entry(entry, 0)
        assert any("'requirements' must be a list" in e for e in errors)

    def test_limitations_must_be_list(self):
        entry = make_entry(limitations="not a list")
        errors = validate_entry(entry, 0)
        assert any("'limitations' must be a list" in e for e in errors)

    # ---------------------------------------------------------------------------
    # Validation: multiple errors
    # ---------------------------------------------------------------------------

    def test_multiple_errors_reported(self):
        entry = make_entry(category="bad", isolation_tier="bad", adoption_effort="bad")
        errors = validate_entry(entry, 0)
        assert len(errors) == 3

    def test_error_includes_entry_name(self):
        entry = make_entry(name="MyTool", category="bad")
        errors = validate_entry(entry, 0)
        assert all("MyTool" in e for e in errors)


class TestValidateAll:
    def test_empty_list(self):
        assert validate_all([]) == []

    def test_all_valid(self):
        entries = [make_entry(name="A"), make_entry(name="B")]
        assert validate_all(entries) == []

    def test_mixed_valid_and_invalid(self):
        entries = [make_entry(name="Good"), make_entry(name="Bad", category="invalid")]
        errors = validate_all(entries)
        assert len(errors) == 1
        assert "Bad" in errors[0]


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

class TestEscapeMd:
    def test_escapes_pipe(self):
        assert escape_md("foo | bar") == "foo \\| bar"

    def test_escapes_newline(self):
        assert escape_md("line1\nline2") == "line1 line2"

    def test_none_returns_empty(self):
        assert escape_md(None) == ""

    def test_plain_text_unchanged(self):
        assert escape_md("hello world") == "hello world"

    def test_multiple_pipes(self):
        assert escape_md("a|b|c") == "a\\|b\\|c"


class TestFormatListShort:
    def test_empty_list(self):
        assert format_list_short([]) == ""

    def test_under_max(self):
        assert format_list_short(["a", "b"]) == "a, b"

    def test_at_max(self):
        assert format_list_short(["a", "b", "c"]) == "a, b, c"

    def test_over_max(self):
        result = format_list_short(["a", "b", "c", "d", "e"])
        assert result == "a, b, c, +2 more"

    def test_custom_max(self):
        result = format_list_short(["a", "b", "c"], max_items=2)
        assert result == "a, b, +1 more"

    def test_escapes_pipes_in_items(self):
        result = format_list_short(["a|b", "c"])
        assert "\\|" in result


# ---------------------------------------------------------------------------
# Lens table generation
# ---------------------------------------------------------------------------

class TestGenerateLensTable:
    def test_groups_by_tag(self):
        entries = [
            make_entry(name="A", adoption_effort="install"),
            make_entry(name="B", adoption_effort="install"),
            make_entry(name="C", adoption_effort="sign-up"),
        ]
        table = generate_lens_table(entries, ADOPTION_EFFORT_ORDER, "adoption_effort")
        assert "A, B" in table
        assert "C" in table
        assert "**Install a tool**" in table
        assert "**Sign up for a service**" in table

    def test_skips_empty_tiers(self):
        entries = [make_entry(name="A", adoption_effort="install")]
        table = generate_lens_table(entries, ADOPTION_EFFORT_ORDER, "adoption_effort")
        assert "Zero-config" not in table

    def test_truncates_at_five(self):
        entries = [make_entry(name=f"Tool{i}", adoption_effort="install") for i in range(7)]
        table = generate_lens_table(entries, ADOPTION_EFFORT_ORDER, "adoption_effort")
        assert "+2 more" in table

    def test_has_header_row(self):
        entries = [make_entry()]
        table = generate_lens_table(entries, ADOPTION_EFFORT_ORDER, "adoption_effort")
        assert "| Effort |" in table
        assert "|--------|" in table


# ---------------------------------------------------------------------------
# Category table generation
# ---------------------------------------------------------------------------

class TestGenerateCategoryTable:
    def test_renders_entry(self):
        entries = [make_entry(name="MySandbox", maintainer="TestCo")]
        table = generate_category_table(entries)
        assert "MySandbox" in table
        assert "TestCo" in table

    def test_links_url(self):
        entries = [make_entry(name="Tool", url="https://example.com")]
        table = generate_category_table(entries)
        assert "[Tool](https://example.com)" in table

    def test_falls_back_to_repo_url(self):
        entries = [make_entry(name="Tool", url=None, repo_url="https://github.com/t/t")]
        table = generate_category_table(entries)
        assert "[Tool](https://github.com/t/t)" in table

    def test_no_link_when_no_urls(self):
        entries = [make_entry(name="Tool", url=None, repo_url=None)]
        table = generate_category_table(entries)
        assert "[Tool]" not in table
        assert "| Tool |" in table

    def test_oss_yes_with_license(self):
        entries = [make_entry(open_source=True, license="MIT")]
        table = generate_category_table(entries)
        assert "Yes (MIT)" in table

    def test_oss_no(self):
        entries = [make_entry(open_source=False, license=None)]
        table = generate_category_table(entries)
        assert "| No |" in table

    def test_sorted_alphabetically(self):
        entries = [
            make_entry(name="Zebra"),
            make_entry(name="Alpha"),
            make_entry(name="Middle"),
        ]
        table = generate_category_table(entries)
        lines = table.split("\n")
        data_lines = [l for l in lines if l.startswith("| ") and "---" not in l and "Name" not in l]
        assert "Alpha" in data_lines[0]
        assert "Middle" in data_lines[1]
        assert "Zebra" in data_lines[2]

    def test_has_header(self):
        entries = [make_entry()]
        table = generate_category_table(entries)
        assert "| Name | Maintainer | OSS? |" in table

    def test_truncates_long_lists(self):
        entries = [make_entry(capabilities=["a", "b", "c", "d", "e"])]
        table = generate_category_table(entries)
        assert "+2 more" in table


# ---------------------------------------------------------------------------
# Vocabulary consistency: CATEGORY_ORDER covers all valid categories
# ---------------------------------------------------------------------------

class TestVocabularyConsistency:
    def test_category_order_covers_all_valid(self):
        ordered_cats = {key for key, _ in CATEGORY_ORDER}
        assert ordered_cats == VALID_CATEGORIES

    def test_no_duplicate_categories_in_order(self):
        keys = [key for key, _ in CATEGORY_ORDER]
        assert len(keys) == len(set(keys))
