# Strategy Update: 2026-04-25

After 16 days of daily discovery reviews (issues #2–#21), adding 27 entries beyond the initial 48-entry seed and rejecting ~150 candidates.

## What the data shows

### Rejection patterns

The rejection pile is overwhelmingly agent frameworks and orchestrators that include sandboxing as a feature — not standalone sandbox tools. Examples from recent reviews: agentscope-runtime, flue, Cognition, eva, sympozium, OpenCapyBox, suna, springdrift. These are "run agents" products where sandboxing is one bullet point among many.

### Addition patterns

Standalone sandbox tools we're adding have gotten increasingly specialized:

- **Week 1** (initial discovery): general-purpose isolation tools — nono, fence, Docker wrappers, container sandboxes
- **Weeks 2–3**: tools with a specific thesis — credential proxying (gondolin, cleanroom), threat detection (code-on-incus), GUI computer-use (EdgeBox), diff/commit/rollback governance (envpod-ce), formal verification (hazmat), Apple Container integration (gocker)
- **Yield curve**: 6 → 5 → 2 → 1 → 0 adds/day over the period. The standalone sandbox tool space is approaching coverage saturation for our current search queries.

## Key observations

### 1. The standalone sandbox category is splitting

General-purpose "put your agent in a box" isolation is being absorbed into agent frameworks. What remains as standalone tools are *opinionated security primitives* with specific properties that frameworks don't offer:

- Credential isolation (nono, cleanroom, gondolin, agent-vault)
- Audit chains and attestation (nono, signet)
- Active threat detection (code-on-incus)
- Formal verification of security policies (hazmat)
- Diff/commit/rollback governance (envpod-ce)

The commodity isolation layer (Docker container, run agent inside it) is becoming a framework feature, not a standalone product.

### 2. Credential isolation is the frontier

nono, cleanroom, gondolin, and agent-vault all independently arrived at "the agent should never see real credentials." This wasn't in the original 48-entry seed — it emerged from discovery. The field is learning that filesystem/network isolation isn't enough; what the agent is *authorized to do* with credentials matters as much as where it runs.

### 3. macOS is disproportionately active

alcless, hazmat, Agent Safehouse, sand, gocker, fence — macOS-specific or macOS-first tools keep appearing. Developers run agents locally on Macs, and macOS has no containers natively (just VMs via Apple Virtualization.framework). The space is solving "how do I sandbox on macOS without Docker?"

### 4. Complementary defenses are a real category

We started tracking complementary tools (pmg, extrasuite, signet, cloak, agent-vault) as mentions in the getting-started.md. These aren't sandboxes but address real threat vectors sandboxes don't cover: supply chain attacks, credential exfiltration at rest, action provenance. This category is growing faster than the sandbox category itself.

## Implications for the repo

### Raise the bar for container-tier additions

New tools that simply wrap Docker for agent execution should require a clear differentiator from existing entries. "Runs agents in Docker" is now a feature of agent frameworks, not a standalone product. The differentiator should be a security property, governance model, or operational feature not found in existing entries.

### Shift discovery focus

The most valuable future contributions are likely:
- Tools with novel security properties (not "another Docker wrapper")
- Complementary defenses (credential proxying, supply chain, action verification)
- Research/analysis content (blog posts, papers on sandbox escapes, isolation evaluation)
- The macOS isolation space (still active, no container-native option exists)

### Consider switching discovery to weekly

The daily cadence was appropriate for initial coverage. With 75 entries and declining yield (0–1 adds/day), weekly discovery is sufficient. This reduces noise from repeat false positives between excluded.yaml updates.

## Adjacent tracking opportunities

This repo tracks *isolation and containment* for agents. Related but distinct domains that could warrant their own tracking projects:

### Agent Harness Engineering
What the rejection pile is actually about. Agent harnesses are the runtime environments that *orchestrate* agent execution — session management, tool routing, state persistence, multi-agent coordination. Frameworks like suna, flue, deer-flow, OpenClaw, NanoClaw. The sandbox is one component; the harness is the larger system. A tracking project here would focus on: orchestration patterns, tool protocol standards (MCP, A2A), state management approaches, multi-agent coordination models, deployment architectures.

### Agent Governance & Policy
Tools like lanekeep, SaneProcess, runok, and SkillWard that operate at the policy layer — what agents are *allowed to do*, enforced via hooks, rules, or application-level controls rather than kernel enforcement. These don't meet our sandbox bar (no OS-level isolation) but solve a real problem: ensuring agents follow organizational policies. A tracking project would focus on: policy specification languages, hook architectures, compliance mapping (NIST/OWASP/CWE), human-in-the-loop approval workflows, audit and observability.

### Agent Credential & Trust Infrastructure
The complementary defenses we track in passing — credential proxies (agent-vault, nono's proxy), secret encryption (cloak), action verification (signet), supply chain defense (pmg). These are becoming a coherent category: "how do you trust an agent with access to real systems?" A tracking project would focus on: credential injection patterns, secret-zero problems, action provenance and non-repudiation, capability-based authorization models, audit trail standards.
