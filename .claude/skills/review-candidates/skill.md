---
name: review-candidates
description: Review discovery issues for new sandbox candidates. Triage, investigate, add approved entries to YAML, regenerate README and reference doc, update safety research doc if applicable, and close the issues.
---

# Review Discovery Candidates

Review open discovery issues, investigate candidates, add approved entries to the repo, and close the issues.

## Usage

- `/review-candidates` — Review all open discovery issues
- `/review-candidates 8` — Review a specific issue number

## Process

### 1. Gather open issues

```bash
gh issue list --repo <owner>/<repo> --label discovery --state open
```

If `$ARGUMENTS` specifies an issue number, review only that issue. Otherwise review all open discovery issues.

Read each issue body to get the candidate table.

### 2. Quick triage

For each candidate, determine from the description alone whether it could plausibly be a sandbox. Apply the **inclusion test**: does this tool provide actual isolation (filesystem, network, process, or stronger) for running an AI agent or untrusted code?

**Immediate rejects** (no investigation needed):
- Agent frameworks or coding agents ("AI coding agent", "agent harness", "pair programmer")
- Awesome-lists, curated lists, star lists, resource collections
- CI/CD tools, automation engines, IDE plugins
- Chat gateways, messaging integrations, desktop apps
- SDK wrappers, orchestration platforms, collaboration layers
- Eval suites, benchmark frameworks, survey papers
- Anything that mentions "sandbox" only in passing or as marketing

**Candidates for investigation** (need README check):
- Explicit sandbox or containment claims ("sandbox", "containment", "isolation", "jail")
- Credential isolation or proxy claims
- VM, container, or process-level enforcement claims
- Policy-enforced execution claims

### 3. Investigate candidates

For each candidate that passed quick triage, use an Agent to fetch the README and evaluate. The agent prompt should:

- State the inclusion test clearly
- Ask for: (a) one-sentence summary, (b) is it a sandbox by our criteria? (c) category, (d) isolation mechanism, (e) maturity flags, (f) one differentiator
- Request direct rejection assessments, not hedging
- Cap the response length (under 600-700 words total)

**Evaluation criteria** (from the critique checklist):
- **Is it actually a sandbox?** Not an agent that runs in a container, not an orchestration tool that calls a sandbox API, not a policy layer without kernel enforcement.
- **Does it fit a category definition?** Test against the definition, not the category name. Valid categories: `cloud-managed`, `agent-integrated`, `standalone`, `kubernetes`, `dev-environment`, `abstraction`, `vm-runtime`, `os-primitive`, `wasm-runtime`.
- **Is it distinct from existing entries?** Check `data/sandboxes.yaml` for duplicates, forks, or thin wrappers of tools already listed.
- **Avoid brand-recognition bias.** Low star count or solo maintainer is NOT a reason to reject. In an early field, adoption reflects marketing, not quality.
- **No LICENSE file is a flag, not a rejection.** Note it in limitations and notes.

### 4. Present recommendations

Present a summary table to the user:

| Repo | Verdict | Reason |
|---|---|---|
| name | Add / Reject / Borderline | One-sentence reasoning |

For borderline cases, state the argument both ways and make a recommendation. Let the user override.

Wait for user approval before proceeding.

### 5. Add approved entries

For each approved entry, add to `data/sandboxes.yaml` with the full schema:

```yaml
- name: ...
  category: ...       # from controlled vocabulary
  maintainer: ...
  open_source: ...
  license: ...        # null if unknown
  url: ...
  repo_url: ...
  description: ...    # one sentence
  isolation_type: ... # list, from controlled vocabulary
  capabilities: ...   # list
  requirements: ...   # list
  limitations: ...    # list
  notes: >-           # free-text editorial context — what makes this
    ...               # worth knowing about, not just field repetition
  isolation_tier: ... # from controlled vocabulary
  adoption_effort: ... # from controlled vocabulary
  deployment_model: ... # from controlled vocabulary
```

**YAML quoting rules** (common pitfalls):
- Strings starting with `"` need single-quote wrapping: `'"Lite" edition'`
- Strings with `<` should be quoted: `"Claims <20ms latency"`
- Use `>-` for multi-line notes (folds lines, strips trailing newline)

If any candidate would fit in the reading list instead of the YAML (e.g., survey papers with a relevant security section), add to `references/reading-list.md` under the appropriate heading.

### 6. Regenerate and test

```bash
uv run python scripts/generate_readme.py
uv run pytest tests/ -q
```

Both must pass before committing.

### 7. Check for introductory content impact

After adding entries, check whether the new additions affect claims made in `docs/getting-started.md` or `docs/safety-research.md`:

**Getting Started checks:**
- Does the nono "only sandbox that combines..." claim still hold? Check if any new entry has ALL FOUR: kernel enforcement + credential isolation + atomic rollback + cryptographic audit chain.
- Does the decision tree need updating? New entries with credential proxy, microVM isolation, or novel properties may deserve a branch.
- Does the Quick Start section need a new option? Only if the new entry is both easy to set up AND offers properties the existing Quick Start options don't cover.

**Safety Research checks:**
- **RL training table**: Does any new entry offer GPU support, fast resets, or self-hosted scale?
- **Capability evaluation table**: Does any new entry offer credential isolation, observability, or reproducibility?
- **Adversarial red-teaming table**: Does any new entry offer hardware VM containment, escape detection, or network monitoring?
- **Maturity table**: Should any new entry be added with maturity caveats?
- **"What's missing" section**: Do any new entries change what's missing from the landscape?

Present findings to the user and update if approved.

### 8. Commit and push

Commit with a message that lists:
- What was added (entry names + one-line descriptions)
- What was rejected (count + any notable specific rejections with reasons)
- Any updates to getting-started.md or safety-research.md

```bash
git add data/sandboxes.yaml README.md docs/ [other changed files]
git commit -m "..."
git push upstream main
```

### 9. Update additions log

Append newly added entries to `data/additions.yaml` so the additions histogram stays current. Group by the issue date, not the review date — if reviewing multiple days' issues, create one entry per day:

```yaml
- date: "2026-04-19"
  entries:
    - new-sandbox-name
    - another-sandbox-name
```

Keep entries in chronological order. The generate script reads this to build the Mermaid bar chart and collapsible daily breakdown in the README.

### 10. Update excluded list

Append all rejected repos to `data/excluded.yaml` so they don't resurface in future discovery runs:

```yaml
- url: https://github.com/org/rejected-repo
  reason: Brief reason for rejection
```

`discover.py` filters these alongside entries in `sandboxes.yaml`. Group new additions by review date with a comment header.

### 11. Close issues

Close each reviewed issue with a comment summarizing what was added and rejected:

```bash
gh issue close <N> --repo <owner>/<repo> --comment "Reviewed in <sha>. Added: ... Rejected: ..."
```

### 12. Check for staleness issues

After closing discovery issues, check for open staleness issues:

```bash
gh issue list --repo <owner>/<repo> --label staleness --state open
```

If any exist, investigate each flagged entry:
- 404 → check if the URL moved or the project was deleted
- Stale commits → check if the project is abandoned or just stable
- HTTP errors → test with a browser-like User-Agent (some sites reject bots)

For false positives (URL works in browser but fails automated check), close with explanation. For real staleness, present to the user and update or remove entries if approved.

## Guidelines

- Be direct about rejections. Most discovery candidates are false positives — that's expected and by design.
- Never add an entry without the user seeing the recommendation first.
- The notes field must add context not already obvious from other fields. "Good sandbox" is not a note. "Uses eBPF syscall interception similar to gVisor but outside the sandbox kernel" is.
- When in doubt about a borderline case, include it. The repo's ethos is comprehensive coverage with honest notes, not gatekeeping.
- Don't batch multiple reviews silently. Present each batch of recommendations, get approval, then proceed.
