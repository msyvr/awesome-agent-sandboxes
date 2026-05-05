# Strategy Update: 2026-05-05

Follow-up to [strategy-update-2026-04-25.md](strategy-update-2026-04-25.md). Ten more days of daily discovery (issues #22–#32), 4 entries added (cua, pi-sandbox, LINCE, pixels) from ~55 candidates — ~7% acceptance rate, consistent with the saturation thesis.

## What changed since 2026-04-25

### A new dominant noise pattern: governance-flavored orchestrators

Seven rejections in 2 weeks (bernstein, kukeon, egg, vnx-orchestration, cadis, agentic-org, OmoiOS) all share the same shape:

- Orchestrate multiple agents/CLIs in parallel (Claude Code, Codex, Gemini, etc.)
- Layer audit chains, receipts, deterministic dispatch, or cryptographic provenance over commodity isolation
- Underlying isolation is git worktree, Docker, or k3s — no novel kernel enforcement
- Often shipped with explicit governance/compliance language ("zero-trust", "deterministic", "receipts", "auditable")

The most telling artifact: **vnx-orchestration ships with `--dangerously-bypass-approvals-and-sandbox` on its codex gate**. Audit chain on, real sandbox off. That isn't a bug; it's the product. The audit chain is the deliverable.

### What's driving it

External research (May 2026) surfaced a clean explanation: the **EU AI Act becomes enforceable August 2026**, classifying multi-agent orchestration in high-impact sectors as "high-risk" and demanding immutable audit trails, human-in-the-loop, persistent identity, and incident testing. Compliance is reportedly adding 20–50% to enterprise orchestration budgets. The market response is a wave of compliance-signaling projects that pair audit primitives with whatever isolation is cheapest to ship.

These projects are real and useful for compliance. They are not sandboxes by our definition.

### The frontier-agent layer is closed

Claude Code (macOS Seatbelt + Linux bubblewrap) and OpenAI Codex (Seatbelt/Landlock/seccomp + cloud-isolated repo clones) have effectively absorbed the agent-integrated category for coding. Third-party tools targeting the AI coding loop have very little oxygen — the frontier vendors made it free and built-in. The `agent-integrated` category has been frozen at 3 entries since the seed; pi-sandbox (added 2026-04-27) is the only post-seed addition, and it's a thin agent-specific layer over Anthropic's sandbox-runtime.

### Cloud sandbox vendors fragmenting, not consolidating

No M&A among E2B / Daytona / Modal / Runloop. Daytona raised a $24M Series A in February 2026. The Superagent benchmark characterizes the space as "fragmenting strategically — each provider carving out distinct niches": Blaxel on cold-start, E2B/Daytona on price, Modal on Python/ML+GPU, Cloudflare/Vercel ecosystem-locked. The most consequential event is **Cloudflare's Sandboxes GA + Mesh + Dynamic Workers + Agent Memory rollout in April 2026** (following the Replicate acquisition in November 2025) — a vertically-integrated stack that moved sandbox execution from "framework code" to "network primitive."

When primitives migrate down the stack, the standalone tier shrinks.

## Implications for the repo

### 1. Auto-reject the governance-orchestrator pattern

Investigating each new bernstein-clone is wasted effort. The pattern is now well-defined and the rejection is mechanical. Added to `review-candidates` skill: auto-reject if the candidate orchestrates multiple agents/CLIs, prominently names governance/audit/receipts features, and delegates isolation to git worktrees / Docker / k3s.

Note the rejection as: *"Governance-orchestrator pattern (audit chain over delegated isolation) — same as bernstein/kukeon/egg/vnx."*

### 2. Discovery cadence: daily → weekly

The `2026-04-25` strategy doc already suggested this. The data since strongly supports it: 7 daily discovery runs in the last 9 days produced 4 entries. Weekly runs (Mondays 9am UTC) would produce the same yield with 7× less noise and 7× fewer false-positive duplicates from filter-timing misses (we hit this 3 times — pi-sandbox, beads_rust, agentic-org all resurfaced after being added/excluded the previous day).

GitHub Actions workflow updated: `cron: "0 9 * * 1"`.

### 3. What remains worth tracking

The narrowing standalone-sandbox surface area still has live niches:

- **Novel substrates** — Incus (pixels, code-on-incus), Apple Container (gocker), microVM (Firecracker derivatives)
- **Novel security properties** — credential proxy (nono, cleanroom, gondolin, agent-vault), threat detection (code-on-incus), formal verification (hazmat), cryptographic audit chain *paired with real isolation* (nono)
- **Novel deployment models** — multi-OS GUI (cua), MCP-as-sandbox-server (pixels)
- **macOS isolation** — still active, no container-native option exists (alcless, hazmat, Agent Safehouse, sand, gocker, fence)

Discovery queries don't need to change; the bar for inclusion does.

## Adjacent tracking still relevant

The `2026-04-25` doc identified three adjacent domains (harness engineering, governance/policy, credential/trust). The governance-orchestrator wave validates the second — there's clearly enough activity to justify a separate scout repo for "agent governance & policy" tracking, if the operator wants. The vnx/bernstein/kukeon class would be in-scope there, even though they're out-of-scope here.
