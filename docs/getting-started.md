# Awesome Agent Sandboxes

A comprehensive guide to sandboxing options for AI agents — coding agents, browsing agents, automation agents, and general-purpose assistants.

Whether you're a developer building with AI agents or someone using them for personal tasks, this guide helps you understand how to keep your system safe while agents work on your behalf.

<!-- TOC -->

<a id="sec-what-is-sandboxing"></a>
## What is sandboxing and why should you care?

A sandbox limits what your AI agent can do on your computer (or in the cloud). Think of it like giving someone access to one room in your house instead of handing them the keys to the whole building.

Without a sandbox, an AI agent typically has the same access you do: it can read and modify any of your files, make network requests, install software, and run arbitrary commands. Most of the time that's fine. But when things go wrong, they can go wrong fast:

- **Deleted or overwritten files** — an agent misinterprets an instruction and removes important data
- **Leaked credentials** — API keys, tokens, or passwords in environment variables get sent to external services
- **Unwanted network requests** — the agent reaches out to URLs you didn't expect, exfiltrating data or triggering costs
- **Runaway cloud bills** — an agent spins up resources or makes API calls in a loop
- **Supply chain attacks** — the agent installs a malicious package that compromises your system

A sandbox constrains these risks by enforcing boundaries the agent can't cross, no matter what instructions it follows.

### Sandboxing is not all-or-nothing

Different sandboxes protect against different things. Understanding what a sandbox *does and doesn't* cover helps you choose the right one:

- **Filesystem isolation** prevents the agent from reading or writing files outside a designated area. Most sandboxes offer this.
- **Network isolation** controls what the agent can reach over the network. Some sandboxes block all network access; others use allowlists.
- **Credential isolation** keeps API keys, tokens, and secrets out of the sandbox entirely. Few sandboxes do this — most rely on you to not pass secrets in.
- **Rollback** lets you undo what the agent did if something goes wrong. Very few sandboxes offer this.
- **Audit** records what the agent actually did, with cryptographic proof. This is rare but valuable for understanding incidents.

When evaluating a sandbox, ask: *what specific risks does this protect against, and what does it leave exposed?*

<a id="sec-quick-start"></a>
## Quick Start: sandbox your agent in 5 minutes

The fastest path to protection depends on what agent you're using and what OS you're on. Each option below includes what it protects and what it doesn't.

<a id="sec-qs-claude-code"></a>
### If you're using Claude Code

Claude Code has built-in sandboxing enabled by default. It uses OS-level primitives (bubblewrap on Linux, Seatbelt on macOS) to restrict filesystem and network access.

```bash
# Sandboxing is on by default — no setup needed.
# To verify, check that you haven't set dangerouslyDisableSandbox.
```

**Protects against:** Filesystem writes outside your project directory. Unrestricted network access (proxy-based domain allowlisting).

**Known risks:**
- The `dangerouslyDisableSandbox` flag can be triggered by the agent itself — a demonstrated escape vector (Ona, March 2026)
- macOS sandbox-exec is deprecated by Apple — could break in a future macOS update with no announced replacement
- Process-level isolation (shared kernel) — weaker than VM or container isolation. A kernel exploit could bypass it.

<a id="sec-qs-codex"></a>
### If you're using OpenAI Codex

Codex enables sandboxing by default in both cloud and local modes.

- **Cloud mode**: Code runs in an isolated container. Network access is disabled during the agent phase.
- **Local CLI (Linux)**: Uses Landlock + seccomp to restrict the agent to workspace-only writes.

**Protects against:** Filesystem access outside workspace. Network access during execution (cloud mode).

**Known risks:**
- Cloud mode requires GitHub integration — your code is sent to OpenAI's infrastructure
- Local mode is Linux-only (kernel 5.13+) — no macOS or Windows support
- Container isolation (cloud) shares the host kernel

<a id="sec-qs-stronger"></a>
### If you want stronger isolation

The options below provide deeper isolation than built-in agent sandboxing. They're listed in order of what security properties they offer, not brand recognition.

#### nono — kernel-enforced sandbox with credential proxy and audit (macOS, Linux, WSL2)

[nono](https://nono.sh) is the only sandbox that combines kernel enforcement with credential isolation, atomic rollback, and a cryptographic audit chain. Your API keys never enter the sandbox — nono proxies them at the network layer so the agent can use services without seeing credentials.

```bash
brew install nono
nono run -- claude
```

**Protects against:** Filesystem and network access (kernel-enforced). Credential leakage (keys never enter sandbox). Unrecoverable mistakes (atomic rollback). "What happened?" questions (cryptographic audit chain with Sigstore attestation).

**Known risks:**
- Early alpha — not yet security-audited
- Relatively new project, though very actively developed

#### Docker Sandboxes — microVM isolation for multiple agents (macOS, Linux)

[Docker Sandboxes](https://docs.docker.com/ai/sandboxes/) run your agent inside a dedicated microVM with its own Docker daemon, filesystem, and network. Stronger isolation boundary than process-level sandboxing.

```bash
# Requires Docker Desktop 4.58+ (or Docker Engine 29.1.5+)
docker sandbox run --image ubuntu:latest
```

Works with Claude Code, Codex, Copilot, Gemini, and Kiro.

**Protects against:** Filesystem and network access at the VM level. Cross-agent contamination (each sandbox is a separate microVM).

**Known risks:**
- **Experimental** (released March 2026) — not production-hardened, no security guarantees yet
- **Docker daemon attack surface**: Docker has a steady cadence of escape-class CVEs. CVE-2025-9074 (CVSS 9.3) allowed unauthenticated Docker Engine API access. Multiple runc CVEs in 2024-2025 enabled container escape. The daemon runs as root.
- **Isolation gap**: Docker Sandboxes isolate *where* code runs but not *what it's authorized to do*. An agent with an API key inside a sandbox can still merge PRs, delete production data, or exfiltrate via allowed network egress.
- **macOS nesting complexity**: On macOS, you get host → Apple VM → microVM → container → agent. Each layer adds potential attack surface and makes debugging harder.
- **Licensing**: Docker Desktop requires a paid subscription for organizations with >250 employees or >$10M annual revenue. Docker Engine (CLI only) remains free.

#### Anthropic srt — sandbox any process or MCP server (macOS, Linux)

[srt](https://github.com/anthropic-experimental/sandbox-runtime) is a lightweight sandbox for arbitrary processes. Particularly useful for sandboxing MCP servers, which run with your permissions but are often third-party code.

```bash
npm install -g @anthropic-ai/sandbox-runtime
srt "your-command"
```

**Protects against:** Filesystem access outside allowed directories. Network access (proxy-based domain filtering with interactive approval — useful for discovering what a tool actually needs).

**Known risks:**
- Beta research preview — APIs may change
- Same macOS sandbox-exec deprecation risk as Claude Code
- Requires Node.js

#### microsandbox — local microVM isolation (macOS, Linux)

[microsandbox](https://github.com/zerocore-ai/microsandbox) provides microVM isolation using libkrun, with no external server. Your credentials and data never leave your machine.

**Protects against:** Full VM-level isolation. Data locality (nothing sent to cloud).

**Known risks:**
- Self-hosted — you're responsible for security updates
- Smaller community
- Requires KVM on Linux

#### Agent Safehouse — macOS sandbox profiles (macOS only)

[Agent Safehouse](https://github.com/eugene1g/agent-safehouse) generates macOS sandbox-exec profiles with a deny-first policy. Pre-built profiles for major coding agents, composable profile system, and a policy builder web tool.

```bash
brew install eugene1g/safehouse/agent-safehouse
```

**Protects against:** Filesystem and process access via macOS Seatbelt kernel enforcement.

**Known risks:**
- macOS only (permanently — sandbox-exec is Apple-specific)
- sandbox-exec deprecation risk
- No network proxy or credential isolation

#### Cloud sandbox services (any OS)

If you'd rather not manage infrastructure, sign up for a cloud sandbox:

- [E2B](https://e2b.dev) — Firecracker microVMs, ~150ms startup, free tier
- [Modal](https://modal.com/products/sandboxes) — GPU support, sub-second starts
- [Daytona](https://www.daytona.io) — container-based, state management (pause/resume)

**Protects against:** Full VM or container isolation. No local system access.

**Known risks:**
- Your code and data run on someone else's infrastructure
- Cloud-only — requires internet access
- Usage-based pricing can accumulate
- Ephemeral by default (except Daytona and Fly Sprites which offer persistence)

<a id="sec-choosing"></a>
## Choosing a sandbox

Use this decision tree to narrow down your options:

```
Do you already use an agent with built-in sandboxing?
├── Yes (Claude Code, Codex) → You have basic protection. Consider
│   stronger options below if you handle sensitive credentials or
│   need rollback/audit capabilities.
│
└── No → What matters most to you?
    │
    ├── Credential safety (API keys, tokens)
    │   └── nono — keys never enter the sandbox
    │
    ├── Undo mistakes (rollback)
    │   └── nono — atomic rollback with integrity verification
    │
    ├── Strongest isolation boundary
    │   ├── Local → Docker Sandboxes or microsandbox (microVM)
    │   └── Cloud → E2B, Modal (Firecracker microVM)
    │
    ├── Sandbox MCP servers / third-party tools
    │   └── Anthropic srt — designed for this use case
    │
    ├── Simplest macOS setup
    │   └── Agent Safehouse (brew install, pre-built profiles)
    │
    ├── Cloud (don't want to manage infrastructure)
    │   ├── Need GPU? → Modal
    │   ├── Need persistence? → Fly Sprites or Daytona
    │   └── General purpose → E2B (most mature, free tier)
    │
    └── Kubernetes
        ├── On GKE? → GKE Agent Sandbox
        └── Any K8s cluster → agent-sandbox (kubernetes-sigs)
```

<a id="sec-safety-research"></a>
## Safety & Alignment Research

If you're doing AI safety research, RL training, capability evaluation, or adversarial red-teaming, see **[Sandboxing for AI Safety & Alignment Research](docs/safety-research.md)** — these contexts have fundamentally different containment requirements from general agent use.

---

_The sections below are generated from [`data/sandboxes.yaml`](data/sandboxes.yaml). They cover the full landscape: cloud services, standalone tools, VM runtimes, OS primitives, and WebAssembly runtimes._
