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
    slugify,
    generate_definition_entry,
    generate_reference_docs,
    generate_toc,
    ref_path_for_category,
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
        entries = [make_entry(name="MySandbox")]
        table = generate_category_table(entries)
        assert "MySandbox" in table

    def test_links_to_local_anchor_by_default(self):
        entries = [make_entry(name="Tool")]
        table = generate_category_table(entries)
        # No cat_key → in-document anchor link
        assert "[Tool](#ref-tool)" in table

    def test_links_to_category_ref_file(self):
        entries = [make_entry(name="Tool")]
        table = generate_category_table(entries, cat_key="standalone")
        assert "[Tool](docs/ref-standalone.md#ref-tool)" in table

    def test_links_to_building_blocks_ref_file(self):
        entries = [make_entry(name="Tool")]
        table = generate_category_table(entries, cat_key="vm-runtime")
        assert "[Tool](docs/ref-building-blocks.md#ref-tool)" in table

    def test_anchor_link_for_complex_name(self):
        entries = [make_entry(name="agent-infra/sandbox")]
        table = generate_category_table(entries, cat_key="standalone")
        assert "[agent-infra/sandbox](docs/ref-standalone.md#ref-agent-infra-sandbox)" in table

    def test_oss_yes_with_license(self):
        entries = [make_entry(open_source=True, license="MIT")]
        table = generate_category_table(entries)
        assert "Yes (MIT)" in table

    def test_oss_no(self):
        entries = [make_entry(open_source=False, license=None)]
        table = generate_category_table(entries)
        assert "| No |" in table

    def test_includes_isolation(self):
        entries = [make_entry(isolation_type=["microvm", "container"])]
        table = generate_category_table(entries)
        assert "microvm, container" in table

    def test_includes_notes(self):
        entries = [make_entry(notes="Important context here.")]
        table = generate_category_table(entries)
        assert "Important context here." in table

    def test_excludes_maintainer(self):
        """Maintainer was moved to the detailed reference."""
        entries = [make_entry(maintainer="ShouldNotAppear Inc")]
        table = generate_category_table(entries)
        assert "ShouldNotAppear" not in table

    def test_excludes_capabilities(self):
        """Capabilities were moved to the detailed reference."""
        entries = [make_entry(capabilities=["should-not-appear"])]
        table = generate_category_table(entries)
        assert "should-not-appear" not in table

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

    def test_has_4_column_header(self):
        entries = [make_entry()]
        table = generate_category_table(entries)
        assert "| Name | OSS? | Isolation | Notes |" in table


# ---------------------------------------------------------------------------
# Slugify
# ---------------------------------------------------------------------------

class TestSlugify:
    def test_simple_name(self):
        assert slugify("E2B") == "ref-e2b"

    def test_lowercase(self):
        assert slugify("Modal") == "ref-modal"

    def test_spaces_to_hyphens(self):
        assert slugify("Fly Sprites") == "ref-fly-sprites"

    def test_strips_punctuation(self):
        assert slugify("Anthropic sandbox-runtime (srt)") == "ref-anthropic-sandbox-runtime-srt"

    def test_slash_becomes_hyphen(self):
        assert slugify("agent-infra/sandbox") == "ref-agent-infra-sandbox"

    def test_collapses_multiple_hyphens(self):
        assert slugify("Linux Namespaces + cgroups") == "ref-linux-namespaces-cgroups"

    def test_strips_trailing_punctuation(self):
        assert slugify("nono") == "ref-nono"

    def test_unique_for_distinct_entries(self):
        """All real entry names should produce unique slugs."""
        names = [
            "E2B", "nono", "scode", "microsandbox",
            "Anthropic sandbox-runtime (srt)",
            "agent-infra/sandbox",
            "Agent Sandbox (kubernetes-sigs)",
            "GKE Agent Sandbox",
            "macOS Seatbelt / sandbox-exec",
            "seccomp-BPF",
            "Linux Namespaces + cgroups",
            "bubblewrap (bwrap)",
        ]
        slugs = [slugify(n) for n in names]
        assert len(slugs) == len(set(slugs)), f"Duplicate slugs: {slugs}"


# ---------------------------------------------------------------------------
# Definition entry generation
# ---------------------------------------------------------------------------

class TestGenerateDefinitionEntry:
    def test_includes_anchor(self):
        entry = make_entry(name="MySandbox")
        result = generate_definition_entry(entry)
        assert '<a id="ref-mysandbox"></a>' in result

    def test_includes_heading(self):
        entry = make_entry(name="MySandbox")
        result = generate_definition_entry(entry)
        assert "#### MySandbox" in result

    def test_includes_maintainer(self):
        entry = make_entry(maintainer="TestCo")
        result = generate_definition_entry(entry)
        assert "TestCo" in result

    def test_includes_license_when_oss(self):
        entry = make_entry(open_source=True, license="Apache-2.0")
        result = generate_definition_entry(entry)
        assert "Apache-2.0" in result

    def test_closed_source_marked(self):
        entry = make_entry(open_source=False, license=None)
        result = generate_definition_entry(entry)
        assert "Closed source" in result

    def test_includes_homepage_link(self):
        entry = make_entry(url="https://example.com")
        result = generate_definition_entry(entry)
        assert "[Home](https://example.com)" in result

    def test_includes_repo_link_when_different(self):
        entry = make_entry(url="https://example.com", repo_url="https://github.com/x/y")
        result = generate_definition_entry(entry)
        assert "[Repo](https://github.com/x/y)" in result

    def test_omits_repo_link_when_same_as_url(self):
        entry = make_entry(url="https://github.com/x/y", repo_url="https://github.com/x/y")
        result = generate_definition_entry(entry)
        # Only the Home link should be present
        assert result.count("https://github.com/x/y") == 1

    def test_includes_description(self):
        entry = make_entry(description="A unique description string.")
        result = generate_definition_entry(entry)
        assert "A unique description string." in result

    def test_includes_capabilities(self):
        entry = make_entry(capabilities=["cap1", "cap2", "cap3"])
        result = generate_definition_entry(entry)
        assert "cap1; cap2; cap3" in result

    def test_includes_requirements(self):
        entry = make_entry(requirements=["req1", "req2"])
        result = generate_definition_entry(entry)
        assert "req1; req2" in result

    def test_includes_limitations(self):
        entry = make_entry(limitations=["lim1"])
        result = generate_definition_entry(entry)
        assert "lim1" in result

    def test_includes_notes(self):
        entry = make_entry(notes="Important context")
        result = generate_definition_entry(entry)
        assert "Important context" in result

    def test_omits_empty_optional_fields(self):
        entry = make_entry(notes=None, repo_url=None)
        result = generate_definition_entry(entry)
        assert "_Notes:" not in result
        assert "[Repo]" not in result

    def test_default_heading_level(self):
        entry = make_entry(name="MySandbox")
        result = generate_definition_entry(entry)
        assert "#### MySandbox" in result

    def test_custom_heading_level(self):
        entry = make_entry(name="MySandbox")
        result = generate_definition_entry(entry, heading_level=3)
        assert "### MySandbox" in result
        assert "#### MySandbox" not in result


# ---------------------------------------------------------------------------
# Standalone reference doc generation
# ---------------------------------------------------------------------------

class TestGenerateReferenceDocs:
    def test_returns_dict_of_files(self):
        entries = [make_entry(category="standalone")]
        docs = generate_reference_docs(entries)
        assert isinstance(docs, dict)
        assert "ref-standalone.md" in docs

    def test_product_categories_get_own_files(self):
        entries = [
            make_entry(name="Tool A", category="standalone"),
            make_entry(name="Tool B", category="cloud-managed"),
        ]
        docs = generate_reference_docs(entries)
        assert "ref-standalone.md" in docs
        assert "ref-cloud-managed.md" in docs

    def test_building_blocks_share_one_file(self):
        entries = [
            make_entry(name="A", category="vm-runtime"),
            make_entry(name="B", category="os-primitive"),
        ]
        docs = generate_reference_docs(entries)
        assert "ref-building-blocks.md" in docs
        assert "## VM & Container Runtimes" in docs["ref-building-blocks.md"]
        assert "## OS-Level Sandboxing" in docs["ref-building-blocks.md"]

    def test_each_file_has_back_link(self):
        entries = [make_entry(category="standalone")]
        docs = generate_reference_docs(entries)
        assert "[Back to main guide](../README.md)" in docs["ref-standalone.md"]

    def test_product_entries_at_h2(self):
        entries = [make_entry(name="Tool", category="standalone")]
        docs = generate_reference_docs(entries)
        assert "## Tool" in docs["ref-standalone.md"]

    def test_anchors_match_table_links(self):
        """Reference doc anchors must match what README category tables link to."""
        entries = [make_entry(name="Tool", category="standalone")]
        table = generate_category_table(entries, cat_key="standalone")
        docs = generate_reference_docs(entries)
        ref_path = ref_path_for_category("standalone")
        assert f"({ref_path}#ref-tool)" in table
        assert '<a id="ref-tool"></a>' in docs["ref-standalone.md"]

    def test_alphabetical_within_category(self):
        entries = [
            make_entry(name="Zebra", category="standalone"),
            make_entry(name="Alpha", category="standalone"),
        ]
        docs = generate_reference_docs(entries)
        content = docs["ref-standalone.md"]
        alpha_pos = content.find("## Alpha")
        zebra_pos = content.find("## Zebra")
        assert alpha_pos < zebra_pos

    def test_empty_categories_excluded(self):
        entries = [make_entry(category="standalone")]
        docs = generate_reference_docs(entries)
        assert "ref-cloud-managed.md" not in docs


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


# ---------------------------------------------------------------------------
# Table of Contents
# ---------------------------------------------------------------------------

class TestGenerateToc:
    def test_includes_heading(self):
        result = generate_toc([make_entry()])
        assert "## Table of Contents" in result

    def test_includes_part1_sections(self):
        result = generate_toc([make_entry()])
        assert "(#sec-what-is-sandboxing)" in result
        assert "(#sec-quick-start)" in result
        assert "(#sec-choosing)" in result
        assert "(#sec-safety-research)" in result

    def test_includes_quick_triage(self):
        result = generate_toc([make_entry()])
        assert "(#sec-quick-triage)" in result

    def test_includes_categories_with_entries(self):
        entries = [
            make_entry(name="A", category="cloud-managed"),
            make_entry(name="B", category="standalone"),
        ]
        result = generate_toc(entries)
        assert "(#sec-cloud-managed)" in result
        assert "(#sec-standalone)" in result

    def test_omits_categories_without_entries(self):
        entries = [make_entry(category="cloud-managed")]
        result = generate_toc(entries)
        assert "(#sec-cloud-managed)" in result
        # No standalone entries, so no link
        assert "(#sec-kubernetes)" not in result

    def test_building_blocks_nested(self):
        entries = [make_entry(category="vm-runtime")]
        result = generate_toc(entries)
        assert "(#sec-building-blocks)" in result
        assert "  - [VM & Container Runtimes](#sec-vm-runtime)" in result

    def test_no_building_blocks_when_no_entries(self):
        entries = [make_entry(category="cloud-managed")]
        result = generate_toc(entries)
        assert "(#sec-building-blocks)" not in result

    def test_includes_detailed_reference(self):
        result = generate_toc([make_entry()])
        # Links to in-document section that itself links out to the file
        assert "[Detailed Sandboxes Reference](#sec-detailed-reference)" in result

    def test_detailed_reference_precedes_quick_triage(self):
        result = generate_toc([make_entry()])
        ref_pos = result.find("Detailed Sandboxes Reference")
        triage_pos = result.find("Quick Triage")
        assert ref_pos < triage_pos

    def test_includes_references_and_contributing(self):
        result = generate_toc([make_entry()])
        assert "(#sec-references)" in result
        assert "(#sec-contributing)" in result
