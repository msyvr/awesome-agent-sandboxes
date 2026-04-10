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
GETTING_STARTED_PATH = ROOT / "docs" / "getting-started.md"
README_PATH = ROOT / "README.md"

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


def generate_category_table(entries: list[dict]) -> str:
    """Generate a detailed table for a category's entries."""
    lines = []
    lines.append("| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |")
    lines.append("|------|------------|------|-----------|------------------|--------------|-------------|-------|")

    for e in sorted(entries, key=lambda x: x["name"].lower()):
        name = e["name"]
        url = e.get("url")
        repo_url = e.get("repo_url")
        if url:
            name_cell = f"[{escape_md(name)}]({url})"
        elif repo_url:
            name_cell = f"[{escape_md(name)}]({repo_url})"
        else:
            name_cell = escape_md(name)

        maintainer = escape_md(e.get("maintainer", ""))
        oss = "Yes" if e.get("open_source") else "No"
        license_str = e.get("license")
        if license_str:
            oss += f" ({license_str})"

        isolation = ", ".join(e.get("isolation_type", []))
        capabilities = format_list_short(e.get("capabilities", []))
        requirements = format_list_short(e.get("requirements", []))
        limitations = format_list_short(e.get("limitations", []))
        notes = escape_md(e.get("notes", "")) or ""

        lines.append(
            f"| {name_cell} | {maintainer} | {oss} | {isolation} "
            f"| {capabilities} | {requirements} | {limitations} | {notes} |"
        )

    return "\n".join(lines)


def generate_part2(entries: list[dict]) -> str:
    """Generate the full Part 2: landscape content."""
    sections = []

    # --- Quick Triage (lenses) ---
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
        sections.append(f"## {cat_name}\n")
        intro = CATEGORY_INTROS.get(cat_key, "")
        if intro:
            sections.append(f"{intro}\n")
        sections.append(generate_category_table(cat_entries))
        sections.append("")

    sections.append("---\n")
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
        sections.append(f"### {cat_name}\n")
        intro = CATEGORY_INTROS.get(cat_key, "")
        if intro:
            sections.append(f"{intro}\n")
        sections.append(generate_category_table(cat_entries))
        sections.append("")

    # --- References ---
    sections.append("## References\n")
    sections.append("See [references/reading-list.md](references/reading-list.md) for blog posts, papers, and discussions on agent sandboxing.\n")

    # --- Contributing ---
    sections.append("## Contributing\n")
    sections.append("To add or update a sandbox entry:\n")
    sections.append("1. Edit `data/sandboxes.yaml` — follow the existing schema (all fields documented in the file header)")
    sections.append("2. Run `python scripts/generate_readme.py` to regenerate the README")
    sections.append("3. Open a PR\n")
    sections.append("The generate script validates the YAML schema and will fail fast on missing required fields or invalid vocabulary values.\n")

    return "\n".join(sections)


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

    # Generate Part 2
    part2 = generate_part2(entries)

    # Concatenate
    readme = f"{part1}\n\n{part2}\n"

    # Write
    README_PATH.write_text(readme)
    print(f"Generated {README_PATH} ({len(entries)} entries, {len(readme)} chars)")


if __name__ == "__main__":
    main()
