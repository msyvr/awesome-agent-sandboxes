#!/usr/bin/env python3
"""Generate README.md from docs/getting-started.md + data/sandboxes.yaml.

Validates the YAML schema (required fields, controlled vocabularies),
generates lens tables and category sections, and concatenates everything
into the final README.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = ROOT / "data" / "sandboxes.yaml"
ADDITIONS_PATH = ROOT / "data" / "additions.yaml"
GETTING_STARTED_PATH = ROOT / "docs" / "getting-started.md"
README_PATH = ROOT / "README.md"
REFERENCE_PATH = ROOT / "docs" / "sandboxes-reference.md"
# Relative path used in markdown links from README to the reference doc
REFERENCE_REL_PATH = "docs/sandboxes-reference.md"

# ---------------------------------------------------------------------------
# Schema: controlled vocabularies
# ---------------------------------------------------------------------------

VALID_CATEGORIES = {
    "cloud-managed",
    "agent-integrated",
    "standalone",
    "kubernetes",
    "dev-environment",
    "abstraction",
    "vm-runtime",
    "os-primitive",
    "wasm-runtime",
}

VALID_ISOLATION_TYPES = {
    "kvm",
    "microvm",
    "container",
    "gvisor",
    "kata",
    "v8-isolate",
    "user-namespace",
    "seatbelt",
    "landlock",
    "seccomp",
    "wasm",
    "process",
}

VALID_ISOLATION_TIERS = {
    "hardware-vm",
    "microvm",
    "container",
    "process",
    "wasm",
}

VALID_ADOPTION_EFFORTS = {
    "zero-config",
    "sign-up",
    "install",
    "compose",
}

VALID_DEPLOYMENT_MODELS = {
    "cloud",
    "local",
    "built-in",
    "self-hosted",
    "kubernetes",
}

# Display names and ordering for categories
CATEGORY_ORDER = [
    # Products & services
    ("cloud-managed", "Cloud Managed Sandboxes"),
    ("agent-integrated", "Agent-Integrated Sandboxes"),
    ("standalone", "Standalone / Self-Hosted Tools"),
    ("kubernetes", "Kubernetes-Native"),
    ("dev-environment", "Development Environments"),
    ("abstraction", "Abstraction Layers"),
    # Building blocks
    ("vm-runtime", "VM & Container Runtimes"),
    ("os-primitive", "OS-Level Sandboxing"),
    ("wasm-runtime", "WebAssembly Runtimes"),
]

BUILDING_BLOCK_CATEGORIES = {"vm-runtime", "os-primitive", "wasm-runtime"}

CATEGORY_INTROS = {
    "cloud-managed": "Managed cloud services that provide sandbox environments via API/SDK. You sign up and get isolated environments on demand.",
    "agent-integrated": "Sandboxing built directly into AI agent products. These activate automatically or with minimal configuration.",
    "standalone": "Tools you install and run yourself to sandbox any agent or process on your own machine.",
    "kubernetes": "Sandbox solutions designed for Kubernetes clusters.",
    "dev-environment": "Development environment platforms that can be repurposed for agent isolation. These aren't agent-specific but provide usable isolation out of the box.",
    "abstraction": "SDKs and frameworks that abstract across multiple sandbox providers.",
    "vm-runtime": "The underlying VM and container runtimes that sandbox products are built on. Use these if you're building your own sandbox infrastructure.",
    "os-primitive": "OS-level isolation primitives. These are building blocks — most users interact with them indirectly through higher-level tools.",
    "wasm-runtime": "WebAssembly runtimes providing language-level sandboxing. Architecturally elegant but require compiling tools to Wasm.",
}

# Lens definitions: (value, label, description, trade_off)
ISOLATION_TIER_ORDER = [
    ("hardware-vm", "Hardware VM (KVM)", "Full hardware virtualization with separate kernel per sandbox.", "Higher overhead and resource use; requires KVM/hypervisor."),
    ("microvm", "MicroVM", "Lightweight VMs (e.g., Firecracker) with fast startup and low overhead.", "Slightly weaker than full VMs; Linux-only for most options."),
    ("container", "Container / User-space Kernel", "Shared kernel with namespace or syscall isolation (Docker, gVisor).", "Shared kernel means a kernel exploit can bypass isolation."),
    ("process", "Process-level", "OS-level restrictions on a process (namespaces, LSMs, Seatbelt).", "Weakest containment boundary; not for adversarial workloads."),
    ("wasm", "Wasm / Language Runtime", "WebAssembly or V8 isolate sandboxing.", "Limited to specific runtimes; can't run arbitrary binaries."),
]

ADOPTION_EFFORT_ORDER = [
    ("zero-config", "Zero-config", "Built into the agent — sandboxing is on by default with no setup."),
    ("sign-up", "Sign up for a service", "Create an account and use a cloud API/SDK. No local infrastructure."),
    ("install", "Install a tool", "Install a standalone tool or runtime on your machine."),
    ("compose", "Compose building blocks", "Assemble from OS primitives or VM runtimes. Requires systems knowledge."),
]

DEPLOYMENT_MODEL_ORDER = [
    ("built-in", "Built into agent", "Sandboxing ships with the agent itself."),
    ("cloud", "Cloud managed", "Runs on someone else's infrastructure."),
    ("local", "Local", "Runs on your machine, data stays local."),
    ("self-hosted", "Self-hosted", "You host and manage the infrastructure."),
    ("kubernetes", "Kubernetes", "Runs on a Kubernetes cluster."),
]

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = [
    "name",
    "category",
    "maintainer",
    "open_source",
    "description",
    "isolation_type",
    "capabilities",
    "requirements",
    "limitations",
    "isolation_tier",
    "adoption_effort",
    "deployment_model",
]


def validate_entry(entry: dict, index: int) -> list[str]:
    """Return a list of validation errors for a single entry."""
    errors = []
    name = entry.get("name", f"entry #{index}")

    for field in REQUIRED_FIELDS:
        if field not in entry or entry[field] is None:
            errors.append(f"{name}: missing required field '{field}'")

    if "category" in entry and entry["category"] not in VALID_CATEGORIES:
        errors.append(f"{name}: invalid category '{entry['category']}' — valid: {sorted(VALID_CATEGORIES)}")

    if "isolation_type" in entry and entry["isolation_type"] is not None:
        if not isinstance(entry["isolation_type"], list):
            errors.append(f"{name}: isolation_type must be a list")
        else:
            for it in entry["isolation_type"]:
                if it not in VALID_ISOLATION_TYPES:
                    errors.append(f"{name}: invalid isolation_type '{it}' — valid: {sorted(VALID_ISOLATION_TYPES)}")

    if "isolation_tier" in entry and entry["isolation_tier"] not in VALID_ISOLATION_TIERS:
        errors.append(f"{name}: invalid isolation_tier '{entry['isolation_tier']}' — valid: {sorted(VALID_ISOLATION_TIERS)}")

    if "adoption_effort" in entry and entry["adoption_effort"] not in VALID_ADOPTION_EFFORTS:
        errors.append(f"{name}: invalid adoption_effort '{entry['adoption_effort']}' — valid: {sorted(VALID_ADOPTION_EFFORTS)}")

    if "deployment_model" in entry and entry["deployment_model"] not in VALID_DEPLOYMENT_MODELS:
        errors.append(f"{name}: invalid deployment_model '{entry['deployment_model']}' — valid: {sorted(VALID_DEPLOYMENT_MODELS)}")

    for list_field in ("capabilities", "requirements", "limitations"):
        val = entry.get(list_field)
        if val is not None and not isinstance(val, list):
            errors.append(f"{name}: '{list_field}' must be a list")

    return errors


def validate_all(entries: list[dict]) -> list[str]:
    """Validate all entries. Returns list of error strings."""
    errors = []
    for i, entry in enumerate(entries):
        errors.extend(validate_entry(entry, i))
    return errors


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def escape_md(text: str) -> str:
    """Escape pipe characters for markdown table cells."""
    if text is None:
        return ""
    return str(text).replace("|", "\\|").replace("\n", " ")


def format_list_short(items: list[str], max_items: int = 3) -> str:
    """Format a list into a short comma-separated string, truncating if needed."""
    if not items:
        return ""
    shown = items[:max_items]
    result = ", ".join(escape_md(item) for item in shown)
    if len(items) > max_items:
        result += f", +{len(items) - max_items} more"
    return result


def generate_lens_table(entries: list[dict], tier_order: list[tuple], tag_field: str) -> str:
    """Generate a lens table grouping entries by a tag field."""
    lines = []

    if tag_field == "isolation_tier":
        lines.append("| Tier | Mechanism | Examples | Trade-off |")
        lines.append("|------|-----------|----------|-----------|")
        for value, label, description, trade_off in tier_order:
            matching = [e["name"] for e in entries if e.get(tag_field) == value]
            if matching:
                examples = ", ".join(matching[:5])
                if len(matching) > 5:
                    examples += f", +{len(matching) - 5} more"
                lines.append(f"| **{label}** | {escape_md(description)} | {examples} | {escape_md(trade_off)} |")
    elif tag_field == "adoption_effort":
        lines.append("| Effort | What it means | Examples |")
        lines.append("|--------|---------------|----------|")
        for value, label, description in tier_order:
            matching = [e["name"] for e in entries if e.get(tag_field) == value]
            if matching:
                examples = ", ".join(matching[:5])
                if len(matching) > 5:
                    examples += f", +{len(matching) - 5} more"
                lines.append(f"| **{label}** | {escape_md(description)} | {examples} |")
    elif tag_field == "deployment_model":
        lines.append("| Model | What it means | Examples |")
        lines.append("|-------|---------------|----------|")
        for value, label, description in tier_order:
            matching = [e["name"] for e in entries if e.get(tag_field) == value]
            if matching:
                examples = ", ".join(matching[:5])
                if len(matching) > 5:
                    examples += f", +{len(matching) - 5} more"
                lines.append(f"| **{label}** | {escape_md(description)} | {examples} |")

    return "\n".join(lines)


def slugify(name: str) -> str:
    """Generate a stable anchor slug for an entry name.

    Used to link from the compact category tables to the detailed
    reference entries below. Same function is used for both anchor
    generation and link target so they always match.
    """
    import re
    s = name.lower()
    # Replace non-alphanumeric (except hyphens) with hyphens
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    # Collapse multiple hyphens
    s = re.sub(r"-+", "-", s)
    # Trim leading/trailing hyphens
    s = s.strip("-")
    return f"ref-{s}"


def generate_category_table(entries: list[dict], anchor_prefix: str = "") -> str:
    """Generate a compact 4-column table for a category's entries.

    Columns: Name (linked to detailed reference) | OSS? | Isolation | Notes

    `anchor_prefix` is prepended to entry anchor links. Pass an empty
    string for in-document links (e.g., "#ref-foo"), or a file path to
    link out to a separate reference doc (e.g., "docs/sandboxes-reference.md#ref-foo").

    Maintainer, capabilities, requirements, and limitations live in the
    detailed reference doc that the table links to.
    """
    lines = []
    lines.append("| Name | OSS? | Isolation | Notes |")
    lines.append("|------|------|-----------|-------|")

    for e in sorted(entries, key=lambda x: x["name"].lower()):
        name = e["name"]
        anchor = slugify(name)
        name_cell = f"[{escape_md(name)}]({anchor_prefix}#{anchor})"

        oss = "Yes" if e.get("open_source") else "No"
        license_str = e.get("license")
        if license_str:
            oss += f" ({license_str})"

        isolation = ", ".join(e.get("isolation_type", []))
        notes = escape_md(e.get("notes", "")) or ""

        lines.append(f"| {name_cell} | {oss} | {isolation} | {notes} |")

    return "\n".join(lines)


def generate_definition_entry(entry: dict, heading_level: int = 4) -> str:
    """Generate a detailed reference entry for a single sandbox.

    Format: anchor + heading + metadata line + description + structured
    fields. Designed to be readable at any width and self-contained.

    `heading_level` controls the markdown heading depth for the entry
    name. Default 4 (####) matches the in-README detailed reference
    section. Use 3 (###) for the standalone reference doc which has
    its own H1.
    """
    lines = []
    name = entry["name"]
    anchor = slugify(name)
    hashes = "#" * heading_level

    lines.append(f'<a id="{anchor}"></a>')
    lines.append(f"{hashes} {name}")
    lines.append("")

    # Metadata line: maintainer, license, links
    meta_parts = []
    maintainer = entry.get("maintainer")
    if maintainer:
        meta_parts.append(f"**Maintainer:** {maintainer}")
    if entry.get("open_source"):
        license_str = entry.get("license") or "OSS"
        meta_parts.append(f"**License:** {license_str}")
    else:
        meta_parts.append("**License:** Closed source")
    url = entry.get("url")
    if url:
        meta_parts.append(f"[Home]({url})")
    repo_url = entry.get("repo_url")
    if repo_url and repo_url != url:
        meta_parts.append(f"[Repo]({repo_url})")
    if meta_parts:
        lines.append(" · ".join(meta_parts))
        lines.append("")

    # Description
    description = entry.get("description", "")
    if description:
        lines.append(description)
        lines.append("")

    # Structured fields
    isolation = ", ".join(entry.get("isolation_type", []))
    if isolation:
        lines.append(f"- **Isolation:** {isolation}")

    for label, field in [
        ("Capabilities", "capabilities"),
        ("Requirements", "requirements"),
        ("Limitations", "limitations"),
    ]:
        items = entry.get(field, [])
        if items:
            lines.append(f"- **{label}:** {'; '.join(items)}")

    notes = entry.get("notes")
    if notes:
        lines.append("")
        lines.append(f"_Notes: {notes}_")

    return "\n".join(lines)


def generate_reference_doc(entries: list[dict]) -> str:
    """Generate the standalone Detailed Sandboxes Reference doc.

    Has its own H1, intro, and uses heading levels appropriate for a
    standalone document (H1 title, H2 categories, H3 entries, with
    Building Blocks as a sibling H2).
    """
    lines = []
    lines.append("# Detailed Sandboxes Reference")
    lines.append("")
    lines.append(
        "Full information for every sandbox tracked in "
        "[awesome-agent-sandboxes](../README.md), grouped by category. "
        "Use your browser's back button or the link above to return to "
        "the main guide."
    )
    lines.append("")

    product_cats = [c for c in CATEGORY_ORDER if c[0] not in BUILDING_BLOCK_CATEGORIES]
    building_cats = [c for c in CATEGORY_ORDER if c[0] in BUILDING_BLOCK_CATEGORIES]

    for cat_key, cat_name in product_cats:
        cat_entries = [e for e in entries if e.get("category") == cat_key]
        if not cat_entries:
            continue
        lines.append(f"## {cat_name}")
        lines.append("")
        for e in sorted(cat_entries, key=lambda x: x["name"].lower()):
            lines.append(generate_definition_entry(e, heading_level=3))
            lines.append("")

    lines.append("## Building Blocks")
    lines.append("")
    for cat_key, cat_name in building_cats:
        cat_entries = [e for e in entries if e.get("category") == cat_key]
        if not cat_entries:
            continue
        lines.append(f"### {cat_name}")
        lines.append("")
        for e in sorted(cat_entries, key=lambda x: x["name"].lower()):
            lines.append(generate_definition_entry(e, heading_level=4))
            lines.append("")

    return "\n".join(lines)


def generate_additions_section(additions: list[dict]) -> str:
    """Generate the additions chart and collapsible breakdown.

    No section heading — this sits at the very top of the README as a
    visual summary. The chart excludes the initial seed to keep the
    scale readable; seed info is in the chart title.
    """
    if not additions:
        return ""

    lines = []
    lines.append('<a id="sec-additions"></a>')

    # Separate the initial seed from discovery additions
    seed = additions[0] if additions else None
    discovery = additions[1:] if len(additions) > 1 else []

    seed_count = len(seed["entries"]) if seed else 0
    seed_date = seed["date"] if seed else "unknown"

    # --- Mermaid bar chart (discovery only, compact) ---
    if discovery:
        short_dates = [a["date"][5:] for a in discovery]
        counts = [len(a["entries"]) for a in discovery]
        max_count = max(counts)

        lines.append("```mermaid")
        lines.append("---")
        lines.append("config:")
        lines.append("    xyChart:")
        lines.append("        height: 200")
        lines.append("        width: 700")
        lines.append("        xAxis:")
        lines.append("            labelFontSize: 10")
        lines.append("        yAxis:")
        lines.append("            labelFontSize: 10")
        lines.append("---")
        lines.append("xychart-beta")
        lines.append(
            f'    title "Additions by date after initial seed'
            f' ({seed_count} items {seed_date})"'
        )
        x_labels = ", ".join(f'"{d}"' for d in short_dates)
        lines.append(f"    x-axis [{x_labels}]")
        lines.append(f'    y-axis "Entries added" 0 --> {max_count + 2}')
        bar_data = ", ".join(str(c) for c in counts)
        lines.append(f"    bar [{bar_data}]")
        lines.append("```\n")

    # --- Collapsible daily breakdown with links (reverse-chron) ---
    lines.append("<details>")
    lines.append("<summary>Daily breakdown (click to expand)</summary>\n")

    for addition in reversed(additions):
        date = addition["date"]
        entry_names = addition["entries"]
        label = f"**{date}** ({len(entry_names)} entries)"
        if addition is seed:
            label += " — initial seed"
        lines.append(label)
        for name in entry_names:
            anchor = slugify(name)
            lines.append(f"- [{name}]({REFERENCE_REL_PATH}#{anchor})")
        lines.append("")

    lines.append("</details>\n")

    return "\n".join(lines)


def generate_part2(entries: list[dict]) -> str:
    """Generate the full Part 2: landscape content."""
    sections = []

    # --- Detailed Sandboxes Reference (link section) ---
    sections.append('<a id="sec-detailed-reference"></a>')
    sections.append("## Detailed Sandboxes Reference\n")
    sections.append(
        f"Full per-entry information for every sandbox lives in "
        f"[{REFERENCE_REL_PATH}]({REFERENCE_REL_PATH}). "
        f"The category tables below also link directly to relevant entries.\n"
    )

    # --- Quick Triage (lenses) ---
    sections.append('<a id="sec-quick-triage"></a>')
    sections.append("## Quick Triage\n")
    sections.append("Three views of the same landscape to help you find what fits.\n")

    sections.append("### How strong is the isolation?\n")
    sections.append(generate_lens_table(entries, ISOLATION_TIER_ORDER, "isolation_tier"))
    sections.append("")

    sections.append("### How do I get started?\n")
    sections.append(generate_lens_table(entries, ADOPTION_EFFORT_ORDER, "adoption_effort"))
    sections.append("")

    sections.append("### Where does it run?\n")
    sections.append(generate_lens_table(entries, DEPLOYMENT_MODEL_ORDER, "deployment_model"))
    sections.append("")

    # --- Category sections ---
    sections.append("---\n")

    # Products & services first, then building blocks
    product_cats = [c for c in CATEGORY_ORDER if c[0] not in BUILDING_BLOCK_CATEGORIES]
    building_cats = [c for c in CATEGORY_ORDER if c[0] in BUILDING_BLOCK_CATEGORIES]

    for cat_key, cat_name in product_cats:
        cat_entries = [e for e in entries if e.get("category") == cat_key]
        if not cat_entries:
            continue
        sections.append(f'<a id="sec-{cat_key}"></a>')
        sections.append(f"## {cat_name}\n")
        intro = CATEGORY_INTROS.get(cat_key, "")
        if intro:
            sections.append(f"{intro}\n")
        sections.append(generate_category_table(cat_entries, anchor_prefix=REFERENCE_REL_PATH))
        sections.append("")

    sections.append("---\n")
    sections.append('<a id="sec-building-blocks"></a>')
    sections.append("## Building Blocks\n")
    sections.append(
        "The underlying technologies that sandbox products are built on. "
        "Most users interact with these indirectly — this section is for "
        "people building their own sandbox infrastructure or evaluating "
        "isolation claims.\n"
    )

    for cat_key, cat_name in building_cats:
        cat_entries = [e for e in entries if e.get("category") == cat_key]
        if not cat_entries:
            continue
        sections.append(f'<a id="sec-{cat_key}"></a>')
        sections.append(f"### {cat_name}\n")
        intro = CATEGORY_INTROS.get(cat_key, "")
        if intro:
            sections.append(f"{intro}\n")
        sections.append(generate_category_table(cat_entries, anchor_prefix=REFERENCE_REL_PATH))
        sections.append("")

    # --- References ---
    sections.append('<a id="sec-references"></a>')
    sections.append("## References\n")
    sections.append("See [references/reading-list.md](references/reading-list.md) for blog posts, papers, and discussions on agent sandboxing.\n")

    # --- Contributing ---
    sections.append('<a id="sec-contributing"></a>')
    sections.append("## Contributing\n")
    sections.append("To add or update a sandbox entry:\n")
    sections.append("1. Edit `data/sandboxes.yaml` — follow the existing schema (all fields documented in the file header)")
    sections.append("2. Run `python scripts/generate_readme.py` to regenerate the README")
    sections.append("3. Open a PR\n")
    sections.append("The generate script validates the YAML schema and will fail fast on missing required fields or invalid vocabulary values.\n")

    return "\n".join(sections)


def generate_toc(entries: list[dict]) -> str:
    """Generate the table of contents.

    Part 1 entries are hardcoded to mirror docs/getting-started.md headings.
    If you add or rename a section in getting-started.md, update this list.
    Part 2 entries are derived from CATEGORY_ORDER and the YAML data.
    """
    lines = ["## Table of Contents\n"]

    # --- Part 1: hand-written sections ---
    lines.append("- [What is sandboxing and why should you care?](#sec-what-is-sandboxing)")
    lines.append("- [Quick Start: sandbox your agent in 5 minutes](#sec-quick-start)")
    lines.append("  - [If you're using Claude Code](#sec-qs-claude-code)")
    lines.append("  - [If you're using OpenAI Codex](#sec-qs-codex)")
    lines.append("  - [If you want stronger isolation](#sec-qs-stronger)")
    lines.append("- [Choosing a sandbox](#sec-choosing)")
    lines.append("  - [Safety & Alignment Research](#sec-safety-research)")

    # --- Part 2: lenses + categories ---
    lines.append("- [Detailed Sandboxes Reference](#sec-detailed-reference)")
    lines.append("- [Quick Triage](#sec-quick-triage)")

    product_cats = [c for c in CATEGORY_ORDER if c[0] not in BUILDING_BLOCK_CATEGORIES]
    building_cats = [c for c in CATEGORY_ORDER if c[0] in BUILDING_BLOCK_CATEGORIES]

    for cat_key, cat_name in product_cats:
        if any(e.get("category") == cat_key for e in entries):
            lines.append(f"- [{cat_name}](#sec-{cat_key})")

    if any(e.get("category") in BUILDING_BLOCK_CATEGORIES for e in entries):
        lines.append("- [Building Blocks](#sec-building-blocks)")
        for cat_key, cat_name in building_cats:
            if any(e.get("category") == cat_key for e in entries):
                lines.append(f"  - [{cat_name}](#sec-{cat_key})")

    lines.append("- [References](#sec-references)")
    lines.append("- [Contributing](#sec-contributing)")

    return "\n".join(lines)


def main():
    # Load YAML
    if not YAML_PATH.exists():
        print(f"Error: {YAML_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(YAML_PATH) as f:
        entries = yaml.safe_load(f)

    if not isinstance(entries, list):
        print(f"Error: {YAML_PATH} must be a YAML list of entries", file=sys.stderr)
        sys.exit(1)

    # Validate
    errors = validate_all(entries)
    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"Validated {len(entries)} entries, all OK.")

    # Load Part 1
    if not GETTING_STARTED_PATH.exists():
        print(f"Error: {GETTING_STARTED_PATH} not found", file=sys.stderr)
        sys.exit(1)

    part1 = GETTING_STARTED_PATH.read_text().rstrip()

    # Inject the table of contents at the placeholder
    toc = generate_toc(entries)
    if "<!-- TOC -->" not in part1:
        print(
            f"Error: {GETTING_STARTED_PATH} is missing the <!-- TOC --> placeholder",
            file=sys.stderr,
        )
        sys.exit(1)
    part1 = part1.replace("<!-- TOC -->", toc)

    # Load additions history
    additions = None
    if ADDITIONS_PATH.exists():
        with open(ADDITIONS_PATH) as f:
            additions = yaml.safe_load(f) or []
        print(f"Loaded {len(additions)} addition dates from {ADDITIONS_PATH}.")

    # Generate additions chart (sits at the very top, before Part 1)
    additions_section = ""
    if additions:
        additions_section = generate_additions_section(additions) + "\n"

    # Generate Part 2
    part2 = generate_part2(entries)

    # Concatenate: chart at top, then Part 1, then Part 2
    readme = f"{additions_section}{part1}\n\n{part2}\n"

    # Write README
    README_PATH.write_text(readme)
    print(f"Generated {README_PATH} ({len(entries)} entries, {len(readme)} chars)")

    # Write standalone Detailed Sandboxes Reference
    reference_doc = generate_reference_doc(entries) + "\n"
    REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_PATH.write_text(reference_doc)
    print(f"Generated {REFERENCE_PATH} ({len(reference_doc)} chars)")


if __name__ == "__main__":
    main()
