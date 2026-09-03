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

**Get the cheap facts from the API first, before spawning anything.** License, last push, stars, archived status and homepage all come from one batched shell loop that costs no model tokens:

```bash
for r in owner/repo owner/repo2 ...; do
  gh api repos/$r --jq '"\(.full_name)|\(.license.spdx_id // "NONE")|\(.pushed_at[0:10])|\(.stargazers_count)|\(.archived)"'
done
```

Agents are for reading prose an API cannot answer: what the tool actually does, which mechanism enforces isolation, whether the README's claims match its own caveats. Never spend an agent fetch on a field `gh api` returns. A backlog review that fans out agents for metadata *and* again for entry-writing can exhaust a session limit — that happened on 2026-09-03 with ~110 fetches across twelve agents.

Two caveats on the API data:
- `license.spdx_id` reports a single id and returns `NOASSERTION` for anything it cannot classify. It was wrong or incomplete on six of 2026-09-03's entries (dual `MIT OR Apache-2.0`, `AGPL-3.0-or-later`, `Apache-2.0 AND BSD-3-Clause` via REUSE, and a GPL stated only in `COPYING.md`). When an agent reads the actual LICENSE file, prefer the agent's compound expression over the API's single id.
- `pushed_at` moves on any branch push. Cross-check against the default branch's last commit before writing a staleness limitation.

For each candidate that survives, use an Agent to fetch the README and evaluate. The agent prompt should:

- State the inclusion test clearly
- Ask for: (a) one-sentence summary, (b) is it a sandbox by our criteria? (c) category, (d) isolation mechanism, (e) maturity flags, (f) one differentiator
- Request direct rejection assessments, not hedging
- Cap the response length (under 600-700 words total)

**Evaluation criteria** (from the critique checklist):
- **Is it actually a sandbox?** Not an agent that runs in a container, not an orchestration tool that calls a sandbox API, not a policy layer without kernel enforcement.
- **Does it fit a category definition?** Test against the definition, not the category name. Valid categories: `cloud-managed`, `agent-integrated`, `standalone`, `self-hosted-platform`, `kubernetes`, `dev-environment`, `abstraction`, `vm-runtime`, `os-primitive`, `wasm-runtime`.
  - `standalone` vs `self-hosted-platform`: a tool you install to wrap one agent on one machine is standalone; a control plane you run to serve many sandboxes over an API or SDK is a self-hosted platform. If it ships a daemon, an API, SDKs, and warm pools, it is the latter. `kubernetes` is for anything requiring a cluster; self-hosted platforms bring their own scheduler or run on bare metal.
- **Categories are not fixed.** When a batch shows several entries that share a shape no existing category names, add one rather than forcing them into the nearest fit. `self-hosted-platform` was added on 2026-09-03 for this reason. Adding one means: extend `VALID_CATEGORIES`, `CATEGORY_ORDER` and `CATEGORY_INTROS` in `scripts/generate_readme.py`, add a section banner in the YAML, add a `generate_reference_doc` test, and note it in a strategy update.
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
- A list item containing `: ` silently parses as a **dict**, not a string. `- Free tier: 300 credits` becomes `{'Free tier': '300 credits'}`, passes `yaml.safe_load` without complaint, and only fails later inside the generator's `'; '.join(items)` with `TypeError: expected str instance, dict found`. Quote any item with a colon.
- Use `>-` for multi-line notes (folds lines, strips trailing newline)

Both failure modes above survive a parse of the fragment in isolation, so validate the shape rather than just the syntax before regenerating:

```bash
uv run python -c "
import yaml
for e in yaml.safe_load(open('data/sandboxes.yaml')):
    for f in ('capabilities','requirements','limitations','isolation_type'):
        for it in e.get(f) or []:
            if not isinstance(it, str): print(e['name'], f, repr(it))"
```

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
- **Site presets**: If tools were added to or removed from the safety-research tables, mirror the change in `data/presets.yaml` (the Pages table site's safety-research filter chips). The generator fails on names that don't match entries, and tests guard the committed JSON.

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

### Raised bar for container-tier additions (as of 2026-04-25)

The standalone sandbox space is maturing. "Runs agents in Docker" is now a commodity feature of agent frameworks, not a standalone product. New container-tier additions should have a clear differentiator not found in existing entries:

- A novel security property (credential proxy, threat detection, audit chain, formal verification)
- A governance model (diff/commit/rollback, human-in-the-loop approval)
- A unique operational feature (GUI desktop, Apple Container integration, multi-backend abstraction)
- A specialized use case (MCP server sandboxing, RL training environments)

A new tool that wraps Docker without adding something beyond what the existing ~20 container-tier entries already cover should be rejected with a note like "no differentiator from existing container-tier entries."

See [docs/strategy-update-2026-04-25.md](docs/strategy-update-2026-04-25.md) for the full analysis behind this guidance.

### Author-submitted PRs: read the source before listing (as of 2026-09-03)

Self-submission is now a regular inbound channel, and it is adversarially selected — the submitter wants in, and writes the YAML themselves. Neither vetto nor SandBase Harness was surfaced by keyword discovery; both arrived as issue comments and PRs.

Before accepting an author-submitted entry, read the code that is supposed to enforce isolation and name the files in the review. Both 2026-09-03 submissions claimed a sandbox; one held up and one did not:

- **vetto** — `landlock.rs`, `seccomp_netblock.rs`, `namespaces.rs`, `net_relay.rs` implement what the README describes. Listed, with the submitted YAML corrected (`adoption_effort` install not zero-config, performance adjectives dropped, maturity caveats added).
- **SandBase Harness** — `local-provider.ts` does path-prefix checks and sets `isolatedExecution: false`; `docker-provider.ts` is `docker run` with no hardening flags; the `docs/sandbox.md` cited in the PR does not exist in the repo. Rejected.

Signals that warrant a closer read: the same project arriving through more than one account, a promotion or outreach doc in the repo logging mass list submissions, a README that opens with star requests, and the submitting org forking this list and its peers.

### Credential brokering is table stakes for container tier (as of 2026-09-03)

Keeping secrets out of the sandbox by substituting them at a proxy was a differentiator in April 2026. By August it was in roughly a dozen entries, hosted and local alike. A container-tier candidate whose only distinguishing property is a credential proxy no longer clears the bar; it needs that plus something else — nested-container enforcement (clampdown), request-path egress rules (clawker), or per-push human approval (agentbox). See [docs/strategy-update-2026-09-03.md](docs/strategy-update-2026-09-03.md).

### Reject governance-orchestrator pattern without investigation (as of 2026-05-05)

The EU AI Act becomes enforceable in August 2026, classifying multi-agent orchestration in high-impact sectors as "high-risk" and demanding immutable audit trails, human-in-the-loop, and incident testing. This has produced a wave of compliance-flavored orchestrators. Already rejected with this exact pattern: bernstein, kukeon, egg, vnx-orchestration, cadis, agentic-org.

**Auto-reject** without investigation if the candidate description includes ALL of:
- Orchestrates multiple agents/CLIs (Claude Code, Codex, Gemini, etc.) in parallel
- Names governance/audit/receipts/dispatch-chain features prominently
- Isolation is git worktree, Docker, or k3s (not novel kernel enforcement)

These layer audit chains over commodity isolation; they're chasing compliance signaling, not security primitives. The audit chain is a governance feature that does not qualify as a sandbox unless paired with a novel isolation property the existing entries lack. vnx-orchestration even shipped with `--dangerously-bypass-approvals-and-sandbox` on its codex gate, demonstrating the pattern: governance receipts on, real sandbox off.

Note in the rejection: "Governance-orchestrator pattern (audit chain over delegated isolation) — same as bernstein/kukeon/egg/vnx."
