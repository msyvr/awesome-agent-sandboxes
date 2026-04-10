# Awesome Agent Sandboxes

A comprehensive guide to sandboxing options for AI agents — coding agents, browsing agents, automation agents, and general-purpose assistants.

Whether you're a developer building with AI agents or someone using them for personal tasks, this guide helps you understand how to keep your system safe while agents work on your behalf.

## Table of Contents

- [What is sandboxing and why should you care?](#sec-what-is-sandboxing)
- [Quick Start: sandbox your agent in 5 minutes](#sec-quick-start)
  - [If you're using Claude Code](#sec-qs-claude-code)
  - [If you're using OpenAI Codex](#sec-qs-codex)
  - [If you want stronger isolation](#sec-qs-stronger)
- [Choosing a sandbox](#sec-choosing)
  - [Safety & Alignment Research](#sec-safety-research)
- [Quick Triage](#sec-quick-triage)
- [Cloud Managed Sandboxes](#sec-cloud-managed)
- [Agent-Integrated Sandboxes](#sec-agent-integrated)
- [Standalone / Self-Hosted Tools](#sec-standalone)
- [Kubernetes-Native](#sec-kubernetes)
- [Development Environments](#sec-dev-environment)
- [Abstraction Layers](#sec-abstraction)
- [Building Blocks](#sec-building-blocks)
  - [VM & Container Runtimes](#sec-vm-runtime)
  - [OS-Level Sandboxing](#sec-os-primitive)
  - [WebAssembly Runtimes](#sec-wasm-runtime)
- [Detailed Reference](#sec-detailed-reference)
- [References](#sec-references)
- [Contributing](#sec-contributing)

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
### Safety & Alignment Research

If you're doing AI safety research, RL training, capability evaluation, or adversarial red-teaming, see **[Sandboxing for AI Safety & Alignment Research](docs/safety-research.md)** — these contexts have fundamentally different containment requirements from general agent use.

---

_The sections below are generated from [`data/sandboxes.yaml`](data/sandboxes.yaml). They cover the full landscape: cloud services, standalone tools, VM runtimes, OS primitives, and WebAssembly runtimes._

<a id="sec-quick-triage"></a>
## Quick Triage

Three views of the same landscape to help you find what fits.

### How strong is the isolation?

| Tier | Mechanism | Examples | Trade-off |
|------|-----------|----------|-----------|
| **Hardware VM (KVM)** | Full hardware virtualization with separate kernel per sandbox. | Firecracker, Kata Containers, libkrun, Zeroboot | Higher overhead and resource use; requires KVM/hypervisor. |
| **MicroVM** | Lightweight VMs (e.g., Firecracker) with fast startup and low overhead. | E2B, Modal, Runloop, Northflank, Fly Sprites, +6 more | Slightly weaker than full VMs; Linux-only for most options. |
| **Container / User-space Kernel** | Shared kernel with namespace or syscall isolation (Docker, gVisor). | Daytona, Koyeb, OpenAI Codex Sandbox, agent-infra/sandbox, Agent Sandbox (kubernetes-sigs), +9 more | Shared kernel means a kernel exploit can bypass isolation. |
| **Process-level** | OS-level restrictions on a process (namespaces, LSMs, Seatbelt). | Claude Code Sandbox, nono, Anthropic sandbox-runtime (srt), NVIDIA OpenShell, Agent Safehouse, +8 more | Weakest containment boundary; not for adversarial workloads. |
| **Wasm / Language Runtime** | WebAssembly or V8 isolate sandboxing. | Cloudflare Dynamic Workers, Wasmtime, WasmEdge, wasmCloud, Wassette, +1 more | Limited to specific runtimes; can't run arbitrary binaries. |

### How do I get started?

| Effort | What it means | Examples |
|--------|---------------|----------|
| **Zero-config** | Built into the agent — sandboxing is on by default with no setup. | Claude Code Sandbox, OpenAI Codex Sandbox |
| **Sign up for a service** | Create an account and use a cloud API/SDK. No local infrastructure. | E2B, Daytona, Modal, Runloop, Northflank, +10 more |
| **Install a tool** | Install a standalone tool or runtime on your machine. | Docker Sandboxes, nono, Anthropic sandbox-runtime (srt), NVIDIA OpenShell, Agent Safehouse, +10 more |
| **Compose building blocks** | Assemble from OS primitives or VM runtimes. Requires systems knowledge. | Firecracker, gVisor, Kata Containers, libkrun, Zeroboot, +11 more |

### Where does it run?

| Model | What it means | Examples |
|-------|---------------|----------|
| **Built into agent** | Sandboxing ships with the agent itself. | Claude Code Sandbox, OpenAI Codex Sandbox |
| **Cloud managed** | Runs on someone else's infrastructure. | E2B, Daytona, Modal, Runloop, Northflank, +10 more |
| **Local** | Runs on your machine, data stays local. | Docker Sandboxes, nono, Anthropic sandbox-runtime (srt), NVIDIA OpenShell, Agent Safehouse, +16 more |
| **Self-hosted** | You host and manage the infrastructure. | Coder, OpenSandbox, Firecracker, gVisor, Kata Containers, +3 more |
| **Kubernetes** | Runs on a Kubernetes cluster. | Agent Sandbox (kubernetes-sigs), GKE Agent Sandbox |

---

<a id="sec-cloud-managed"></a>
## Cloud Managed Sandboxes

Managed cloud services that provide sandbox environments via API/SDK. You sign up and get isolated environments on demand.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [Bunnyshell AI Sandboxes](#ref-bunnyshell-ai-sandboxes) | No | microvm | MCP server integration is notable — direct plugin for Claude Code, Cursor, and Windsurf. |
| [Cloudflare Dynamic Workers](#ref-cloudflare-dynamic-workers) | No | v8-isolate | Unique edge-first approach using V8 isolates instead of containers/VMs. Credential injection without agent visibility is a strong security feature. Open beta early 2026. |
| [CodeSandbox SDK](#ref-codesandbox-sdk) | No | microvm | Well-established brand from the browser IDE space, expanding to agent use. |
| [Daytona](#ref-daytona) | Yes (Apache-2.0) | container | Pivoted from CDE space (Feb 2025). $31M Series A (Feb 2026). State management (pause/resume) is a key differentiator vs. ephemeral-only platforms. |
| [E2B](#ref-e2b) | Yes (Apache-2.0) | microvm | One of the earliest and most widely adopted agent sandbox platforms. Docker MCP Catalog partnership. |
| [Fly Sprites](#ref-fly-sprites) | No | microvm | Persistence is the key differentiator — most sandboxes are ephemeral. Checkpoint/restore enables warm resumption of long-running agent sessions. |
| [Modal](#ref-modal) | No | microvm | Only major sandbox platform with GPU support — unique differentiator for ML/AI workloads that need compute. |
| [Northflank](#ref-northflank) | No | kata, gvisor | BYOC option is unusual in this space — most cloud sandboxes are single-provider. Production-proven at scale (2M+ workloads/month). |
| [Runloop](#ref-runloop) | No | microvm | Enterprise compliance focus (SOC 2) differentiates from developer-oriented alternatives. GA May 2025. |
| [Vercel Sandbox](#ref-vercel-sandbox) | No | microvm | Tightly integrated with Vercel deployment pipeline and v0. |

<a id="sec-agent-integrated"></a>
## Agent-Integrated Sandboxes

Sandboxing built directly into AI agent products. These activate automatically or with minimal configuration.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [Claude Code Sandbox](#ref-claude-code-sandbox) | No | user-namespace, seatbelt | Demonstrated escape by Ona (March 2026) via dangerouslyDisableSandbox flag. Uses bubblewrap on Linux, Seatbelt on macOS — different mechanisms per OS. |
| [OpenAI Codex Sandbox](#ref-openai-codex-sandbox) | No | container, landlock, seccomp | Only major agent with sandboxing enabled by default. Two-phase model (online setup, offline agent) is a unique security architecture — the agent never has network access during execution. |

<a id="sec-standalone"></a>
## Standalone / Self-Hosted Tools

Tools you install and run yourself to sandbox any agent or process on your own machine.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [Agent Safehouse](#ref-agent-safehouse) | Yes | seatbelt | More mature than it appears — has CI tests, docs site, and thoughtful profile composition. The most polished macOS-specific sandboxing option. |
| [agent-infra/sandbox](#ref-agent-infra-sandbox) | Yes | container | Kitchen-sink approach — good for prototyping and development, less suitable for security-critical production use. |
| [Anthropic sandbox-runtime (srt)](#ref-anthropic-sandbox-runtime-srt) | Yes | user-namespace, seatbelt | Designed to sandbox any process, not just Claude Code. Interactive network approval mode is useful for discovering what network access a tool actually needs. |
| [Docker Sandboxes](#ref-docker-sandboxes) | No | microvm | Very new (March 2026). Multi-agent support is notable — works with most major coding agents out of the box. |
| [microsandbox](#ref-microsandbox) | Yes | microvm | Local-first is the key differentiator — no credentials leave your machine. Good for privacy-conscious users handling sensitive API keys. |
| [nono](#ref-nono) | Yes | landlock, seatbelt | Unique combination of properties no other tool offers: credential proxy (API keys never enter the sandbox), attestation, and atomic rollback. Easy setup (brew install, then nono run -- claude). Very active development. |
| [NVIDIA OpenShell](#ref-nvidia-openshell) | Yes (Apache-2.0) | landlock, seccomp | NVIDIA backing gives visibility. OPA/Rego policy support targets enterprise governance workflows. Announced at GTC 2026. |
| [OpenSandbox](#ref-opensandbox) | Yes | container | Broadest scope of any sandbox — covers evaluation and RL training environments, not just agent sandboxing. |
| [scode](#ref-scode) | Yes | process | Early entry in the space (Sept 2025), motivated by Claude Code's initial lack of built-in sandboxing. |

<a id="sec-kubernetes"></a>
## Kubernetes-Native

Sandbox solutions designed for Kubernetes clusters.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [Agent Sandbox (kubernetes-sigs)](#ref-agent-sandbox-kubernetes-sigs) | Yes (Apache-2.0) | gvisor, kata | Official Kubernetes SIG project (launched KubeCon Atlanta Nov 2025). Likely to become the standard for K8s agent sandboxing. |
| [GKE Agent Sandbox](#ref-gke-agent-sandbox) | No | gvisor, kata | Managed wrapper around the open-source agent-sandbox project. If you're already on GKE, this is the path of least resistance. |

<a id="sec-dev-environment"></a>
## Development Environments

Development environment platforms that can be repurposed for agent isolation. These aren't agent-specific but provide usable isolation out of the box.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [Coder](#ref-coder) | Yes (AGPL-3.0) | container | Not agent-specific, but good for teams wanting self-hosted isolation without cloud dependency. AGPL license means modifications must be shared. |
| [DevPod](#ref-devpod) | Yes | container | Not agent-specific. Good open-source alternative to Codespaces for local-first workflows where you want reproducible isolated environments. |
| [GitHub Codespaces](#ref-github-codespaces) | No | container | Not purpose-built for agents, but accessible to anyone familiar with GitHub. A "good enough" isolation option for personal agent use without learning new tools. |
| [Koyeb](#ref-koyeb) | No | container | General-purpose serverless platform, not purpose-built for agents, but usable for agent isolation out of the box with standard container workflows. |
| [Ona (formerly Gitpod)](#ref-ona-formerly-gitpod) | No | container | Major pivot from Gitpod (rebranded Sept 2025). Demonstrated Claude Code sandbox escape (March 2026). Not agent-specific but increasingly agent-oriented. |

<a id="sec-abstraction"></a>
## Abstraction Layers

SDKs and frameworks that abstract across multiple sandbox providers.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [ComputeSDK](#ref-computesdk) | No | microvm, container | Useful if you want to avoid vendor lock-in. Isolation strength depends entirely on the chosen backend provider. |
| [LangChain Sandboxes](#ref-langchain-sandboxes) | Yes | container | Only relevant if already using LangChain. The sandbox capabilities come from the underlying provider, not LangChain itself. |
| [NanoClaw](#ref-nanoclaw) | Yes (MIT) | container | More of an agent orchestration framework with sandbox support than a sandbox itself. High adoption. Sandbox capability comes from Docker or Docker Sandboxes underneath. |

---

<a id="sec-building-blocks"></a>
## Building Blocks

The underlying technologies that sandbox products are built on. Most users interact with these indirectly — this section is for people building their own sandbox infrastructure or evaluating isolation claims.

<a id="sec-vm-runtime"></a>
### VM & Container Runtimes

The underlying VM and container runtimes that sandbox products are built on. Use these if you're building your own sandbox infrastructure.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [Firecracker](#ref-firecracker) | Yes (Apache-2.0) | kvm, microvm | The foundation most cloud sandbox platforms build on. Battle-tested at AWS scale (Lambda, Fargate). If you're building a sandbox product, this is likely your starting point. |
| [gVisor](#ref-gvisor) | Yes (Apache-2.0) | gvisor | Used by GKE and kubernetes-sigs/agent-sandbox. Good middle ground between container and VM isolation — stronger than containers, lighter than full VMs. |
| [Kata Containers](#ref-kata-containers) | Yes (Apache-2.0) | kata, kvm | Production-proven at scale via Northflank (2M+ workloads/month). Good for Kubernetes environments that need VM-level isolation per pod. |
| [libkrun](#ref-libkrun) | Yes (Apache-2.0) | kvm | macOS support via Apple Virtualization.framework is unique among VM runtimes — Firecracker and Kata are Linux-only. Used by microsandbox. |
| [Zeroboot](#ref-zeroboot) | Yes | kvm, microvm | 0.8ms sandbox creation via COW forking is remarkable if verified at scale. Worth watching as a potential next-gen approach to sandbox provisioning. |

<a id="sec-os-primitive"></a>
### OS-Level Sandboxing

OS-level isolation primitives. These are building blocks — most users interact with them indirectly through higher-level tools.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [bubblewrap (bwrap)](#ref-bubblewrap-bwrap) | Yes (LGPL-2.0+) | user-namespace | Years of hardening via Flatpak. Claude Code's Linux sandbox builds on this. The go-to unprivileged sandbox primitive on Linux. |
| [Firejail](#ref-firejail) | Yes (GPL-2.0) | user-namespace, seccomp | Primarily for desktop app sandboxing, but applicable to agent processes. SUID requirement is a trade-off — convenience vs. attack surface. |
| [Landlock LSM](#ref-landlock-lsm) | Yes (GPL-2.0) | landlock | The modern Linux answer to unprivileged sandboxing. Network support in kernel 6.7 makes it much more complete. Used by Codex CLI and OpenShell. |
| [Linux Namespaces + cgroups](#ref-linux-namespaces-cgroups) | Yes (GPL-2.0) | user-namespace | Everything in the container and VM space builds on these primitives. Understanding namespaces and cgroups is foundational to evaluating any Linux-based sandbox's isolation claims. |
| [macOS Seatbelt / sandbox-exec](#ref-macos-seatbelt-sandbox-exec) | No | seatbelt | Deprecated but still the only game in town for macOS process sandboxing. Used by Claude Code, Agent Safehouse, and srt on macOS. No replacement announced by Apple. |
| [nsjail](#ref-nsjail) | Yes (Apache-2.0) | user-namespace, seccomp | Google-maintained. Kafel policy language is more ergonomic than raw seccomp-BPF. Used by competitive programming judges for untrusted code execution. |
| [seccomp-BPF](#ref-seccomp-bpf) | Yes (GPL-2.0) | seccomp | Building block, not standalone. Almost always used alongside Landlock or namespaces to provide full sandbox coverage. |

<a id="sec-wasm-runtime"></a>
### WebAssembly Runtimes

WebAssembly runtimes providing language-level sandboxing. Architecturally elegant but require compiling tools to Wasm.

| Name | OSS? | Isolation | Notes |
|------|------|-----------|-------|
| [Pyodide](#ref-pyodide) | Yes (MPL-2.0) | wasm | Good for sandboxing Python-only agent code execution where you need browser-grade isolation guarantees without running a VM. |
| [wasmCloud](#ref-wasmcloud) | Yes (Apache-2.0) | wasm | Higher-level than Wasmtime or WasmEdge — it's an application platform, not just a runtime. Useful if building distributed agent systems with Wasm isolation. |
| [WasmEdge](#ref-wasmedge) | Yes (Apache-2.0) | wasm | CNCF project. Differentiates from Wasmtime with AI/ML inference extensions and edge deployment focus. |
| [Wasmtime](#ref-wasmtime) | Yes (Apache-2.0) | wasm | The reference Wasm runtime from Bytecode Alliance. Architecturally elegant sandboxing but requires toolchain buy-in — you can't run arbitrary binaries. |
| [Wassette](#ref-wassette) | Yes | wasm | Interesting intersection of MCP and Wasm — agents discover and load sandboxed tools via MCP from OCI registries. Microsoft backing. Released Aug 2025. |

---

<a id="sec-detailed-reference"></a>
## Detailed Reference

Full information for every entry, grouped by category. The compact tables above link here.

### Cloud Managed Sandboxes

<a id="ref-bunnyshell-ai-sandboxes"></a>
#### Bunnyshell AI Sandboxes

**Maintainer:** Bunnyshell · **License:** Closed source · [Home](https://www.bunnyshell.com/ai-sandbox-environments/)

Firecracker sandboxes with ~100ms cold starts and MCP Server integration for Claude Code/Cursor/Windsurf.

- **Isolation:** microvm
- **Capabilities:** Firecracker isolation; ~100ms cold starts; Multi-language support; MCP server integration; Snapshots; SDK
- **Requirements:** Cloud-hosted; Paid tiers
- **Limitations:** AI sandbox is a newer product line

_Notes: MCP server integration is notable — direct plugin for Claude Code, Cursor, and Windsurf._

<a id="ref-cloudflare-dynamic-workers"></a>
#### Cloudflare Dynamic Workers

**Maintainer:** Cloudflare · **License:** Closed source · [Home](https://developers.cloudflare.com/sandbox/)

V8 isolate-based sandboxing at the edge, claiming 100x faster and more memory-efficient than containers.

- **Isolation:** v8-isolate
- **Capabilities:** V8 isolate isolation; Millisecond startup; MB-level memory per isolate; globalOutbound for HTTP interception; Credential injection without agent visibility
- **Requirements:** Cloudflare Workers paid plan; $0.002/unique Worker/day (waived during beta)
- **Limitations:** JS/TS only (V8 runtime); Not for arbitrary Linux binaries; Weaker isolation than microVMs

_Notes: Unique edge-first approach using V8 isolates instead of containers/VMs. Credential injection without agent visibility is a strong security feature. Open beta early 2026._

<a id="ref-codesandbox-sdk"></a>
#### CodeSandbox SDK

**Maintainer:** CodeSandbox · **License:** Closed source · [Home](https://codesandbox.io/sdk)

SDK for giving agents sandboxed MicroVM environments with parallel execution support.

- **Isolation:** microvm
- **Capabilities:** MicroVM isolation; Parallel agent execution; Web-dev environments; File operations; Port forwarding
- **Requirements:** Cloud-hosted; SDK integration
- **Limitations:** Primarily web-dev focused

_Notes: Well-established brand from the browser IDE space, expanding to agent use._

<a id="ref-daytona"></a>
#### Daytona

**Maintainer:** Daytona · **License:** Apache-2.0 · [Home](https://www.daytona.io) · [Repo](https://github.com/daytonaio/daytona)

Docker/OCI container-based cloud sandboxes with native state management.

- **Isolation:** container
- **Capabilities:** Docker container isolation; <60ms provisioning; Configurable resources; State management (stop/resume/archive); Python/JS/TS SDKs
- **Requirements:** Cloud-hosted managed service; Usage-based pricing
- **Limitations:** Container-based (shared kernel, weaker isolation than microVMs); Newer platform

_Notes: Pivoted from CDE space (Feb 2025). $31M Series A (Feb 2026). State management (pause/resume) is a key differentiator vs. ephemeral-only platforms._

<a id="ref-e2b"></a>
#### E2B

**Maintainer:** E2B · **License:** Apache-2.0 · [Home](https://e2b.dev) · [Repo](https://github.com/e2b-dev/E2B)

Cloud sandbox platform for AI agents using Firecracker microVMs via API/SDK.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVM isolation; ~150ms startup; Filesystem isolation; Network control; Python/JS/TS SDKs; Custom templates
- **Requirements:** Cloud-hosted managed service; Free tier available
- **Limitations:** 24-hour session limit; Cloud-only; Ephemeral by default; No GPU support

_Notes: One of the earliest and most widely adopted agent sandbox platforms. Docker MCP Catalog partnership._

<a id="ref-fly-sprites"></a>
#### Fly Sprites

**Maintainer:** Fly.io · **License:** Closed source · [Home](https://sprites.dev)

Persistent Firecracker microVMs for AI agent sessions with 100GB NVMe per sprite.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVM isolation; Persistent 100GB NVMe storage; Checkpoint/restore (~300ms warm); Stateful across sessions; ~$0.07/CPU-hour
- **Requirements:** Cloud-hosted; API access; 1-12s cold start
- **Limitations:** Cold starts slower than E2B; Newer product (Jan 2026)

_Notes: Persistence is the key differentiator — most sandboxes are ephemeral. Checkpoint/restore enables warm resumption of long-running agent sessions._

<a id="ref-modal"></a>
#### Modal

**Maintainer:** Modal Labs · **License:** Closed source · [Home](https://modal.com/products/sandboxes)

Serverless cloud platform with sandbox product and best-in-class GPU support.

- **Isolation:** microvm
- **Capabilities:** Sub-second starts; GPU workloads; Network tunnels; Per-sandbox egress policies; 50k+ concurrent sessions
- **Requirements:** Cloud-hosted; Python SDK; Usage-based pricing
- **Limitations:** Closed source; Cloud-only; Python-centric SDK

_Notes: Only major sandbox platform with GPU support — unique differentiator for ML/AI workloads that need compute._

<a id="ref-northflank"></a>
#### Northflank

**Maintainer:** Northflank · **License:** Closed source · [Home](https://northflank.com)

Production-grade sandbox infrastructure using Kata Containers and gVisor at 2M+ isolated workloads/month.

- **Isolation:** kata, gvisor
- **Capabilities:** MicroVM via Kata + gVisor; Unlimited session duration; Any OCI image; BYOC (bring your own cloud) deployment; Resource limits; Network controls
- **Requirements:** Cloud-hosted or BYOC; Paid platform
- **Limitations:** Closed source; More complex setup than simpler platforms

_Notes: BYOC option is unusual in this space — most cloud sandboxes are single-provider. Production-proven at scale (2M+ workloads/month)._

<a id="ref-runloop"></a>
#### Runloop

**Maintainer:** Runloop · **License:** Closed source · [Home](https://runloop.ai)

Enterprise-grade sandbox infrastructure (Devboxes) with SOC 2 compliance and 10k+ parallel instances.

- **Isolation:** microvm
- **Capabilities:** Blueprints and Snapshots; Isolated cloud dev environments; SOC 2 compliance; High concurrency (10k+ parallel)
- **Requirements:** Cloud-hosted; Enterprise pricing
- **Limitations:** Closed source; Enterprise-focused

_Notes: Enterprise compliance focus (SOC 2) differentiates from developer-oriented alternatives. GA May 2025._

<a id="ref-vercel-sandbox"></a>
#### Vercel Sandbox

**Maintainer:** Vercel · **License:** Closed source · [Home](https://vercel.com)

Firecracker microVM sandboxes for untrusted code, powering v0's code generation runtime.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVMs; Node.js + Python support; Up to 45min execution; Up to 8 vCPUs / 2GB per vCPU
- **Requirements:** Vercel account; Cloud-hosted
- **Limitations:** Node.js and Python only; 45-minute maximum execution; Tightly coupled to Vercel ecosystem

_Notes: Tightly integrated with Vercel deployment pipeline and v0._

### Agent-Integrated Sandboxes

<a id="ref-claude-code-sandbox"></a>
#### Claude Code Sandbox

**Maintainer:** Anthropic · **License:** Closed source · [Home](https://code.claude.com/docs/en/sandboxing)

Native OS-level sandboxing using bubblewrap (Linux) and Seatbelt/sandbox-exec (macOS), reducing permission prompts by 84%.

- **Isolation:** user-namespace, seatbelt
- **Capabilities:** Filesystem isolation (CWD read/write, block writes elsewhere); Network isolation (proxy-based domain allowlisting); OS-level enforcement
- **Requirements:** Claude Code CLI; macOS or Linux
- **Limitations:** dangerouslyDisableSandbox escape hatch can be triggered by agent itself; macOS sandbox-exec deprecated by Apple; Shared kernel

_Notes: Demonstrated escape by Ona (March 2026) via dangerouslyDisableSandbox flag. Uses bubblewrap on Linux, Seatbelt on macOS — different mechanisms per OS._

<a id="ref-openai-codex-sandbox"></a>
#### OpenAI Codex Sandbox

**Maintainer:** OpenAI · **License:** Closed source · [Home](https://developers.openai.com/codex/concepts/sandboxing)

Two modes: cloud (isolated containers, internet disabled during agent phase) and local CLI (Landlock + seccomp on Linux).

- **Isolation:** container, landlock, seccomp
- **Capabilities:** Cloud: isolated containers, two-phase runtime (setup with network, then offline agent); Cloud: per-project network lists, secrets removed before agent; Local: Landlock + seccomp, workspace-only writes
- **Requirements:** Cloud: OpenAI account + GitHub; Local: Linux kernel 5.13+
- **Limitations:** Cloud requires GitHub integration; Local is Linux-only; Network disabled by default in agent phase

_Notes: Only major agent with sandboxing enabled by default. Two-phase model (online setup, offline agent) is a unique security architecture — the agent never has network access during execution._

### Standalone / Self-Hosted Tools

<a id="ref-agent-safehouse"></a>
#### Agent Safehouse

**Maintainer:** eugene1g · **License:** OSS · [Home](https://github.com/eugene1g/agent-safehouse)

macOS sandbox-exec profile system with deny-first policy, composable profiles, and pre-built agent configurations.

- **Isolation:** seatbelt
- **Capabilities:** macOS Seatbelt profile generation; Deny-first policy; Composable profile system; Pre-built profiles for major coding agents; Policy builder web tool; Fine-grained HOME access control; Symlink-aware path resolution
- **Requirements:** macOS only; brew install eugene1g/safehouse/agent-safehouse
- **Limitations:** macOS only (permanently — sandbox-exec is Apple-specific); sandbox-exec deprecation risk

_Notes: More mature than it appears — has CI tests, docs site, and thoughtful profile composition. The most polished macOS-specific sandboxing option._

<a id="ref-agent-infra-sandbox"></a>
#### agent-infra/sandbox

**Maintainer:** agent-infra (community) · **License:** OSS · [Home](https://github.com/agent-infra/sandbox)

All-in-one sandbox combining Browser, Shell, File management, MCP, and VSCode Server in a single Docker container.

- **Isolation:** container
- **Capabilities:** Browser automation; Shell access; File management; MCP integration; VSCode Server
- **Requirements:** Docker
- **Limitations:** Container isolation only (shared kernel); Monolithic design

_Notes: Kitchen-sink approach — good for prototyping and development, less suitable for security-critical production use._

<a id="ref-anthropic-sandbox-runtime-srt"></a>
#### Anthropic sandbox-runtime (srt)

**Maintainer:** Anthropic · **License:** OSS · [Home](https://github.com/anthropic-experimental/sandbox-runtime)

Lightweight sandboxing for arbitrary processes using bubblewrap (Linux) and Seatbelt (macOS), no container required.

- **Isolation:** user-namespace, seatbelt
- **Capabilities:** Filesystem isolation (directory-level); Network isolation (proxy-based domain filtering with interactive approval); Works for any process, agent, or MCP server
- **Requirements:** macOS or Linux; No root required on Linux
- **Limitations:** Experimental/research preview; Not production-hardened; macOS sandbox-exec deprecation risk

_Notes: Designed to sandbox any process, not just Claude Code. Interactive network approval mode is useful for discovering what network access a tool actually needs._

<a id="ref-docker-sandboxes"></a>
#### Docker Sandboxes

**Maintainer:** Docker · **License:** Closed source · [Home](https://docs.docker.com/ai/sandboxes/)

MicroVM sandboxes for AI coding agents, each with its own Docker daemon, filesystem, and network.

- **Isolation:** microvm
- **Capabilities:** MicroVM isolation (not regular containers); Dedicated Docker daemon per sandbox; Filesystem and network isolation; Supports Claude Code, Codex, Copilot, Gemini, Kiro
- **Requirements:** Docker Engine 29.1.5+ (Docker Desktop 4.58+); macOS or Linux
- **Limitations:** Experimental; MicroVM overhead

_Notes: Very new (March 2026). Multi-agent support is notable — works with most major coding agents out of the box._

<a id="ref-microsandbox"></a>
#### microsandbox

**Maintainer:** zerocore-ai · **License:** OSS · [Home](https://github.com/zerocore-ai/microsandbox)

Local-first programmable sandboxes using libkrun microVMs, designed for sensitive API keys with no external server.

- **Isolation:** microvm
- **Capabilities:** libkrun microVM isolation; Local-first (no external server); Programmable SDK; Agent Skills for Claude Code, Cursor, Codex, Gemini, Copilot
- **Requirements:** Linux (KVM) or macOS
- **Limitations:** Self-hosted only; Smaller community

_Notes: Local-first is the key differentiator — no credentials leave your machine. Good for privacy-conscious users handling sensitive API keys._

<a id="ref-nono"></a>
#### nono

**Maintainer:** always-further · **License:** OSS · [Home](https://nono.sh) · [Repo](https://github.com/always-further/nono)

Kernel-enforced agent sandbox with credential proxy, atomic rollback, Sigstore attestation, and cryptographic audit chain.

- **Isolation:** landlock, seatbelt
- **Capabilities:** Kernel-level enforcement (Landlock on Linux, Seatbelt on macOS); Credential injection via proxy (keys never enter the sandbox); Atomic rollback with Merkle tree integrity; Sigstore-based attestation of instruction files; L7 API endpoint filtering; Detach/reattach multiplexing; Rust library with Python/TS/Go bindings
- **Requirements:** macOS, Linux, or WSL2; brew install nono or single binary
- **Limitations:** Early alpha — not yet audited

_Notes: Unique combination of properties no other tool offers: credential proxy (API keys never enter the sandbox), attestation, and atomic rollback. Easy setup (brew install, then nono run -- claude). Very active development._

<a id="ref-nvidia-openshell"></a>
#### NVIDIA OpenShell

**Maintainer:** NVIDIA · **License:** Apache-2.0 · [Home](https://github.com/NVIDIA/OpenShell)

Secure runtime for autonomous AI agents with kernel-level Landlock + seccomp enforcement and declarative YAML/OPA policies.

- **Isolation:** landlock, seccomp
- **Capabilities:** Landlock + seccomp kernel enforcement; Declarative YAML policies; OPA/Rego policy support; Static + dynamic policies; Filesystem/network/process isolation; Containerized agent support
- **Requirements:** Linux; Early preview
- **Limitations:** Early preview; Linux only; No macOS support

_Notes: NVIDIA backing gives visibility. OPA/Rego policy support targets enterprise governance workflows. Announced at GTC 2026._

<a id="ref-opensandbox"></a>
#### OpenSandbox

**Maintainer:** Alibaba · **License:** OSS · [Home](https://github.com/alibaba/OpenSandbox)

Universal sandbox for AI apps with multi-language SDKs, Docker + K8s runtimes, covering coding agents, GUI agents, evaluation, and RL training.

- **Isolation:** container
- **Capabilities:** Multi-language SDKs (Python/Java/JS/C#/Go planned); Unified API; Dual runtime (Docker for dev, K8s for prod); Evaluation and RL training support
- **Requirements:** Docker or Kubernetes; Self-hosted
- **Limitations:** Very new (open-sourced March 2026)

_Notes: Broadest scope of any sandbox — covers evaluation and RL training environments, not just agent sandboxing._

<a id="ref-scode"></a>
#### scode

**Maintainer:** Laurent Bindschaedler · **License:** OSS · [Home](https://binds.ch/blog/scode-sandbox-for-ai-coding-tools/)

OS-level sandbox wrapper for any AI coding harness with filesystem and network restrictions.

- **Isolation:** process
- **Capabilities:** OS-level sandboxing; Works with any AI coding tool; Filesystem and network restrictions
- **Requirements:** macOS or Linux
- **Limitations:** Smaller community project

_Notes: Early entry in the space (Sept 2025), motivated by Claude Code's initial lack of built-in sandboxing._

### Kubernetes-Native

<a id="ref-agent-sandbox-kubernetes-sigs"></a>
#### Agent Sandbox (kubernetes-sigs)

**Maintainer:** Kubernetes SIG · **License:** Apache-2.0 · [Home](https://github.com/kubernetes-sigs/agent-sandbox)

Kubernetes CRD and controller for isolated agent workloads with gVisor or Kata runtime and warm pod pools.

- **Isolation:** gvisor, kata
- **Capabilities:** Declarative CRD; gVisor + Kata support; Warm pod pool for <1s cold start; Persistent storage; Stable pod identity
- **Requirements:** Kubernetes cluster; gVisor or Kata runtime
- **Limitations:** Kubernetes required; Still maturing; No standalone mode

_Notes: Official Kubernetes SIG project (launched KubeCon Atlanta Nov 2025). Likely to become the standard for K8s agent sandboxing._

<a id="ref-gke-agent-sandbox"></a>
#### GKE Agent Sandbox

**Maintainer:** Google Cloud · **License:** Closed source · [Home](https://cloud.google.com)

Managed Kubernetes service for AI code isolation on GKE using gVisor and kubernetes-sigs/agent-sandbox.

- **Isolation:** gvisor, kata
- **Capabilities:** Managed gVisor/Kata runtime; GKE integration; Warm pools; Persistent storage; Cloud IAM
- **Requirements:** Google Cloud account; GKE cluster
- **Limitations:** GKE-only; Vendor lock-in

_Notes: Managed wrapper around the open-source agent-sandbox project. If you're already on GKE, this is the path of least resistance._

### Development Environments

<a id="ref-coder"></a>
#### Coder

**Maintainer:** Coder · **License:** AGPL-3.0 · [Home](https://github.com/coder/coder)

Self-hosted remote development platform with container and VM workspaces, RBAC, and audit logging.

- **Isolation:** container
- **Capabilities:** Self-hosted; Container and VM workspaces; Templates; RBAC; Audit logging
- **Requirements:** Self-hosted on Kubernetes or Docker
- **Limitations:** No agent-specific features; No MCP integration

_Notes: Not agent-specific, but good for teams wanting self-hosted isolation without cloud dependency. AGPL license means modifications must be shared._

<a id="ref-devpod"></a>
#### DevPod

**Maintainer:** Loft Labs · **License:** OSS · [Home](https://github.com/loft-sh/devpod)

Client-only tool for reproducible, provider-agnostic dev environments using devcontainer.json.

- **Isolation:** container
- **Capabilities:** Provider-agnostic (Docker/SSH/K8s/cloud); devcontainer.json support; Client-only (no server); Open source
- **Requirements:** Docker or cloud provider
- **Limitations:** No agent-specific features; No MCP integration; No managed service

_Notes: Not agent-specific. Good open-source alternative to Codespaces for local-first workflows where you want reproducible isolated environments._

<a id="ref-github-codespaces"></a>
#### GitHub Codespaces

**Maintainer:** GitHub / Microsoft · **License:** Closed source · [Home](https://github.com/features/codespaces)

Cloud-hosted dev environments usable for isolating agent execution in a full Linux VM.

- **Isolation:** container
- **Capabilities:** Full Linux VM; devcontainer.json support; Pre-built images; GitHub integration; Port forwarding
- **Requirements:** GitHub account; Usage-based pricing (free tier available)
- **Limitations:** Not agent-specific; Higher startup latency; Dev tool, not a sandbox service

_Notes: Not purpose-built for agents, but accessible to anyone familiar with GitHub. A "good enough" isolation option for personal agent use without learning new tools._

<a id="ref-koyeb"></a>
#### Koyeb

**Maintainer:** Koyeb · **License:** Closed source · [Home](https://www.koyeb.com)

Serverless platform with container-based sandbox capabilities and auto-scaling.

- **Isolation:** container
- **Capabilities:** Container isolation; Auto-scaling; CI/CD integration
- **Requirements:** Cloud-hosted; Usage-based pricing
- **Limitations:** Not agent-specific; General-purpose serverless platform

_Notes: General-purpose serverless platform, not purpose-built for agents, but usable for agent isolation out of the box with standard container workflows._

<a id="ref-ona-formerly-gitpod"></a>
#### Ona (formerly Gitpod)

**Maintainer:** Ona · **License:** Closed source · [Home](https://ona.com)

Pivoted from CDE to "mission control for AI agents" with sandboxed dev environments, AI agents, and guardrails.

- **Isolation:** container
- **Capabilities:** API-first environments; devcontainer.json support; OS-level isolation; Ona Agents; Ona Guardrails
- **Requirements:** Cloud-hosted; Enterprise tiers
- **Limitations:** Rapid pivot — product still evolving; Less sandbox API focus than E2B/Daytona

_Notes: Major pivot from Gitpod (rebranded Sept 2025). Demonstrated Claude Code sandbox escape (March 2026). Not agent-specific but increasingly agent-oriented._

### Abstraction Layers

<a id="ref-computesdk"></a>
#### ComputeSDK

**Maintainer:** ComputeSDK · **License:** Closed source · [Home](https://www.computesdk.com)

Unified API across multiple sandbox providers (E2B, Daytona, Modal, Blaxel, etc.).

- **Isolation:** microvm, container
- **Capabilities:** Provider-agnostic API; Single SDK for multiple backends
- **Requirements:** Account with underlying provider
- **Limitations:** Abstraction adds complexity; Provider-dependent isolation

_Notes: Useful if you want to avoid vendor lock-in. Isolation strength depends entirely on the chosen backend provider._

<a id="ref-langchain-sandboxes"></a>
#### LangChain Sandboxes

**Maintainer:** LangChain · **License:** OSS · [Home](https://docs.langchain.com/oss/python/deepagents/sandboxes)

Sandbox integration layer within the LangChain agent framework.

- **Isolation:** container
- **Capabilities:** Framework integration; Provider abstraction; Agent workflow orchestration
- **Requirements:** LangChain framework; Python
- **Limitations:** Framework-dependent; Not standalone

_Notes: Only relevant if already using LangChain. The sandbox capabilities come from the underlying provider, not LangChain itself._

<a id="ref-nanoclaw"></a>
#### NanoClaw

**Maintainer:** Lazer and Gavriel Cohen · **License:** MIT · [Home](https://github.com/qwibitai/nanoclaw)

Lightweight containerized agent orchestration wrapping Claude Code with messaging platform integrations.

- **Isolation:** container
- **Capabilities:** Container isolation (Docker/Docker Sandboxes/Apple Container); WhatsApp/Telegram/Slack/Discord/Gmail integration; Memory management; Scheduled jobs
- **Requirements:** Docker or Apple Container
- **Limitations:** Tied to Claude/Anthropic SDK; Container-level isolation unless using Docker Sandboxes

_Notes: More of an agent orchestration framework with sandbox support than a sandbox itself. High adoption. Sandbox capability comes from Docker or Docker Sandboxes underneath._

### Building Blocks

#### VM & Container Runtimes

<a id="ref-firecracker"></a>
#### Firecracker

**Maintainer:** AWS · **License:** Apache-2.0 · [Home](https://github.com/firecracker-microvm/firecracker)

Lightweight microVM monitor using KVM with <5MB overhead, powering Lambda, Fargate, E2B, Vercel, Bunnyshell, and Fly Sprites.

- **Isolation:** kvm, microvm
- **Capabilities:** KVM hardware isolation; <125ms boot; <5MB memory per VM; Snapshot/restore (~28ms); Rate limiters; Jailer for additional containment
- **Requirements:** Linux with KVM; x86_64 or aarch64
- **Limitations:** Linux only; No GPU passthrough; Minimal device model; Must build own orchestration layer

_Notes: The foundation most cloud sandbox platforms build on. Battle-tested at AWS scale (Lambda, Fargate). If you're building a sandbox product, this is likely your starting point._

<a id="ref-gvisor"></a>
#### gVisor

**Maintainer:** Google · **License:** Apache-2.0 · [Home](https://github.com/google/gvisor)

User-space kernel that intercepts and re-implements Linux syscalls, providing container isolation without hardware virtualization.

- **Isolation:** gvisor
- **Capabilities:** Syscall interception in user space; No hardware virtualization needed; OCI-compatible (drop-in runsc runtime); Sentry kernel + Gofer file proxy architecture
- **Requirements:** Linux; OCI runtime (runsc)
- **Limitations:** Performance overhead on syscall-heavy workloads; Not all syscalls implemented

_Notes: Used by GKE and kubernetes-sigs/agent-sandbox. Good middle ground between container and VM isolation — stronger than containers, lighter than full VMs._

<a id="ref-kata-containers"></a>
#### Kata Containers

**Maintainer:** OpenInfra Foundation · **License:** Apache-2.0 · [Home](https://github.com/kata-containers/kata-containers)

VM-level isolation per container, OCI/CRI compatible, supporting QEMU, Cloud Hypervisor, and Firecracker VMMs.

- **Isolation:** kata, kvm
- **Capabilities:** Hardware VM per container; OCI/CRI compatible; Multiple VMM backends (QEMU/Cloud Hypervisor/Firecracker); Kubernetes integration
- **Requirements:** Linux with KVM
- **Limitations:** Higher overhead than gVisor; Requires KVM; More complex setup

_Notes: Production-proven at scale via Northflank (2M+ workloads/month). Good for Kubernetes environments that need VM-level isolation per pod._

<a id="ref-libkrun"></a>
#### libkrun

**Maintainer:** Containers project (Red Hat) · **License:** Apache-2.0 · [Home](https://github.com/containers/libkrun)

Library-based KVM virtualization with container-competitive startup, supporting Apple Virtualization.framework on macOS.

- **Isolation:** kvm
- **Capabilities:** Library-embeddable (no daemon); KVM isolation; Fast startup; Apple Virtualization.framework on macOS
- **Requirements:** Linux (KVM) or macOS (Virtualization.framework)
- **Limitations:** Less tooling than Firecracker; Smaller community

_Notes: macOS support via Apple Virtualization.framework is unique among VM runtimes — Firecracker and Kata are Linux-only. Used by microsandbox._

<a id="ref-zeroboot"></a>
#### Zeroboot

**Maintainer:** Zeroboot (community) · **License:** OSS · [Home](https://github.com/zerobootdev/zeroboot)

Sub-millisecond VM sandboxes via COW forking of Firecracker snapshots (~0.8ms fork creation).

- **Isolation:** kvm, microvm
- **Capabilities:** KVM isolation; Firecracker snapshot COW forking; ~0.8ms sandbox creation; Self-hostable; Managed API also available
- **Requirements:** Linux with KVM
- **Limitations:** Very new; Small community

_Notes: 0.8ms sandbox creation via COW forking is remarkable if verified at scale. Worth watching as a potential next-gen approach to sandbox provisioning._

#### OS-Level Sandboxing

<a id="ref-bubblewrap-bwrap"></a>
#### bubblewrap (bwrap)

**Maintainer:** Containers project (Flatpak origin) · **License:** LGPL-2.0+ · [Home](https://github.com/containers/bubblewrap)

Unprivileged user-namespace sandbox for Linux requiring no root, used by Claude Code and Flatpak.

- **Isolation:** user-namespace
- **Capabilities:** User namespaces; Mount namespaces; Network namespace; No root required
- **Requirements:** Linux with user namespace support
- **Limitations:** Linux only; Low-level (must compose with other tools)

_Notes: Years of hardening via Flatpak. Claude Code's Linux sandbox builds on this. The go-to unprivileged sandbox primitive on Linux._

<a id="ref-firejail"></a>
#### Firejail

**Maintainer:** netblue30 (community) · **License:** GPL-2.0 · [Home](https://github.com/netblue30/firejail)

SUID sandbox combining namespaces, seccomp, and capabilities with desktop-aware features (audio, display).

- **Isolation:** user-namespace, seccomp
- **Capabilities:** Namespace isolation; seccomp-BPF filtering; Filesystem whitelisting; Network filtering; Desktop app support (audio, display); Pre-built profiles for common apps
- **Requirements:** Linux; Setuid binary
- **Limitations:** SUID is a larger attack surface; Desktop-focused; Linux only

_Notes: Primarily for desktop app sandboxing, but applicable to agent processes. SUID requirement is a trade-off — convenience vs. attack surface._

<a id="ref-landlock-lsm"></a>
#### Landlock LSM

**Maintainer:** Linux kernel community · **License:** GPL-2.0 · [Home](https://landlock.io)

Unprivileged filesystem access control at kernel level, used by Codex CLI and NVIDIA OpenShell.

- **Isolation:** landlock
- **Capabilities:** Filesystem access restrictions per path; Unprivileged (no root); Stackable with other LSMs; Kernel-level enforcement
- **Requirements:** Linux kernel 5.13+ (network support in 6.7+)
- **Limitations:** Filesystem only in early kernel versions; Must combine with seccomp for full coverage; Linux only

_Notes: The modern Linux answer to unprivileged sandboxing. Network support in kernel 6.7 makes it much more complete. Used by Codex CLI and OpenShell._

<a id="ref-linux-namespaces-cgroups"></a>
#### Linux Namespaces + cgroups

**Maintainer:** Linux kernel community · **License:** GPL-2.0

Foundation of all container technology — PID, mount, network, user, UTS, and IPC namespaces plus cgroups for resource limits.

- **Isolation:** user-namespace
- **Capabilities:** Process isolation (PID namespace); Filesystem isolation (mount namespace); Network isolation (network namespace); User isolation (user namespace); CPU/memory/IO limits (cgroups)
- **Requirements:** Linux
- **Limitations:** Building blocks only — must compose into usable tools; Shared kernel; Linux only

_Notes: Everything in the container and VM space builds on these primitives. Understanding namespaces and cgroups is foundational to evaluating any Linux-based sandbox's isolation claims._

<a id="ref-macos-seatbelt-sandbox-exec"></a>
#### macOS Seatbelt / sandbox-exec

**Maintainer:** Apple · **License:** Closed source

macOS mandatory access control using SBPL policies for filesystem, network, and process restrictions.

- **Isolation:** seatbelt
- **Capabilities:** Filesystem access control; Network control; Process restrictions; Kernel-level enforcement
- **Requirements:** macOS only
- **Limitations:** sandbox-exec deprecated by Apple; SBPL policy language poorly documented

_Notes: Deprecated but still the only game in town for macOS process sandboxing. Used by Claude Code, Agent Safehouse, and srt on macOS. No replacement announced by Apple._

<a id="ref-nsjail"></a>
#### nsjail

**Maintainer:** Google · **License:** Apache-2.0 · [Home](https://github.com/google/nsjail)

Process isolation tool combining namespaces, seccomp, and resource limits with the Kafel policy language.

- **Isolation:** user-namespace, seccomp
- **Capabilities:** Namespace isolation; seccomp-BPF filtering; cgroup resource limits; chroot/pivot_root; Network filtering; Kafel policy language
- **Requirements:** Linux
- **Limitations:** Linux only; Less actively maintained; CLI only

_Notes: Google-maintained. Kafel policy language is more ergonomic than raw seccomp-BPF. Used by competitive programming judges for untrusted code execution._

<a id="ref-seccomp-bpf"></a>
#### seccomp-BPF

**Maintainer:** Linux kernel community · **License:** GPL-2.0

Syscall filtering using BPF programs to kill, trap, or errno on forbidden syscalls.

- **Isolation:** seccomp
- **Capabilities:** Syscall-level filtering; BPF programmability; Kill/trap/errno on forbidden syscalls
- **Requirements:** Linux kernel 3.5+
- **Limitations:** Syscall-level only (no file path awareness); Complex BPF filter authoring; Linux only

_Notes: Building block, not standalone. Almost always used alongside Landlock or namespaces to provide full sandbox coverage._

#### WebAssembly Runtimes

<a id="ref-pyodide"></a>
#### Pyodide

**Maintainer:** Pyodide community (Mozilla origin) · **License:** MPL-2.0 · [Home](https://github.com/pyodide/pyodide)

CPython compiled to WebAssembly providing browser-grade sandbox security for Python execution.

- **Isolation:** wasm
- **Capabilities:** Full CPython in Wasm; Browser-grade isolation; Supports NumPy, Pandas, and other scientific packages
- **Requirements:** Browser or Wasm runtime
- **Limitations:** Python only; Not all C extensions supported; No native filesystem or network access; Performance overhead vs. native CPython

_Notes: Good for sandboxing Python-only agent code execution where you need browser-grade isolation guarantees without running a VM._

<a id="ref-wasmcloud"></a>
#### wasmCloud

**Maintainer:** wasmCloud community · **License:** Apache-2.0 · [Home](https://github.com/wasmCloud/wasmCloud)

Application platform for building distributed Wasm applications with capability-based security.

- **Isolation:** wasm
- **Capabilities:** Distributed Wasm applications; Capability-based security model; Provider-based extensibility; Lattice networking
- **Requirements:** Cross-platform; NATS for messaging
- **Limitations:** Must compile to Wasm; More complex than standalone runtimes; Application platform, not just a runtime

_Notes: Higher-level than Wasmtime or WasmEdge — it's an application platform, not just a runtime. Useful if building distributed agent systems with Wasm isolation._

<a id="ref-wasmedge"></a>
#### WasmEdge

**Maintainer:** CNCF · **License:** Apache-2.0 · [Home](https://github.com/WasmEdge/WasmEdge)

Cloud-native WebAssembly runtime optimized for edge, AI, and serverless workloads.

- **Isolation:** wasm
- **Capabilities:** Memory-safe execution; WASI support; AI/ML inference extensions; Kubernetes integration; Edge deployment focus
- **Requirements:** Cross-platform; Must compile tools to Wasm
- **Limitations:** Must compile to Wasm; Not for arbitrary Linux binaries

_Notes: CNCF project. Differentiates from Wasmtime with AI/ML inference extensions and edge deployment focus._

<a id="ref-wasmtime"></a>
#### Wasmtime

**Maintainer:** Bytecode Alliance · **License:** Apache-2.0 · [Home](https://github.com/bytecodealliance/wasmtime)

Fast, secure WebAssembly runtime with WASI capability-based security and linear memory isolation.

- **Isolation:** wasm
- **Capabilities:** Memory-safe execution; WASI capability-based security; Multi-tenant isolation; Thousands of concurrent instances; Cross-platform
- **Requirements:** Cross-platform; Must compile tools to Wasm
- **Limitations:** Must compile to Wasm; Not for arbitrary Linux binaries; Ecosystem still maturing

_Notes: The reference Wasm runtime from Bytecode Alliance. Architecturally elegant sandboxing but requires toolchain buy-in — you can't run arbitrary binaries._

<a id="ref-wassette"></a>
#### Wassette

**Maintainer:** Microsoft (Azure Core Upstream) · **License:** OSS · [Home](https://github.com/microsoft/wassette)

Wasm Components exposed via MCP, using Wasmtime runtime with agents fetching Wasm tools from OCI registries.

- **Isolation:** wasm
- **Capabilities:** Wasm Component Model; MCP interface; Deny-by-default security; Wasmtime runtime (browser-grade isolation); OCI registry integration
- **Requirements:** Rust toolchain; MCP-compatible agent
- **Limitations:** Wasm only (must compile tools to Wasm); Early ecosystem

_Notes: Interesting intersection of MCP and Wasm — agents discover and load sandboxed tools via MCP from OCI registries. Microsoft backing. Released Aug 2025._

<a id="sec-references"></a>
## References

See [references/reading-list.md](references/reading-list.md) for blog posts, papers, and discussions on agent sandboxing.

<a id="sec-contributing"></a>
## Contributing

To add or update a sandbox entry:

1. Edit `data/sandboxes.yaml` — follow the existing schema (all fields documented in the file header)
2. Run `python scripts/generate_readme.py` to regenerate the README
3. Open a PR

The generate script validates the YAML schema and will fail fast on missing required fields or invalid vocabulary values.

