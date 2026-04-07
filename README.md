# Awesome Agent Sandboxes

A comprehensive guide to sandboxing options for AI agents — coding agents, browsing agents, automation agents, and general-purpose assistants.

Whether you're a developer building with AI agents or someone using them for personal tasks, this guide helps you understand how to keep your system safe while agents work on your behalf.

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

## Quick Start: sandbox your agent in 5 minutes

The fastest path to protection depends on what agent you're using and what OS you're on. Each option below includes what it protects and what it doesn't.

### If you're using Claude Code

Claude Code has built-in sandboxing enabled by default. It uses OS-level primitives (bubblewrap on Linux, Seatbelt on macOS) to restrict filesystem and network access.

```bash
# Sandboxing is on by default — no setup needed.
# To verify, check that you haven't set dangerouslyDisableSandbox.
```

**Protects against:** Filesystem writes outside your project directory. Unrestricted network access (proxy-based domain allowlisting).

**Known risks:**
- The `dangerouslyDisableSandbox` flag can be triggered by the agent itself — a [demonstrated escape vector](https://ona.com) (March 2026)
- macOS sandbox-exec is deprecated by Apple — could break in a future macOS update with no announced replacement
- Process-level isolation (shared kernel) — weaker than VM or container isolation. A kernel exploit could bypass it.

### If you're using OpenAI Codex

Codex enables sandboxing by default in both cloud and local modes.

- **Cloud mode**: Code runs in an isolated container. Network access is disabled during the agent phase.
- **Local CLI (Linux)**: Uses Landlock + seccomp to restrict the agent to workspace-only writes.

**Protects against:** Filesystem access outside workspace. Network access during execution (cloud mode).

**Known risks:**
- Cloud mode requires GitHub integration — your code is sent to OpenAI's infrastructure
- Local mode is Linux-only (kernel 5.13+) — no macOS or Windows support
- Container isolation (cloud) shares the host kernel

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

## Choosing a sandbox

Use this decision tree to narrow down your options:

```
Do you already use an agent with built-in sandboxing?
├── Yes (Claude Code, Codex) → You have basic protection. Consider
│   stronger options below if you handle sensitive credentials or
│   need rollback/audit capabilities.
│
└── What matters most to you?
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

## Full Landscape

For a comprehensive technical comparison of all sandbox options — including cloud services, standalone tools, VM runtimes, OS primitives, and WebAssembly runtimes — see the full landscape below.

## Quick Triage

Three views of the same landscape to help you find what fits.

### How strong is the isolation?

| Tier | Mechanism | Examples | Trade-off |
|------|-----------|----------|-----------|
| **Hardware VM (KVM)** | Full hardware virtualization. Strongest isolation — separate kernel per sandbox. | Firecracker, Kata Containers, libkrun, Zeroboot |
| **MicroVM** | Lightweight VMs (e.g., Firecracker). Near-VM isolation with fast startup and low overhead. | E2B, Modal, Runloop, Northflank, Fly Sprites, +6 more |
| **Container / User-space Kernel** | Shared kernel with namespace/syscall isolation (Docker, gVisor). Weaker than VMs but lighter. | Daytona, Koyeb, OpenAI Codex Sandbox, agent-infra/sandbox, Agent Sandbox (kubernetes-sigs), +9 more |
| **Process-level** | OS-level restrictions on a process (namespaces, LSMs, Seatbelt). No VM or container overhead. | Claude Code Sandbox, nono, Anthropic sandbox-runtime (srt), NVIDIA OpenShell, Agent Safehouse, +8 more |
| **Wasm / Language Runtime** | WebAssembly or V8 isolate sandboxing. Fastest and lightest, but limited to specific runtimes. | Cloudflare Dynamic Workers, Wasmtime, WasmEdge, wasmCloud, Wassette, +1 more |

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

## Cloud Managed Sandboxes

Managed cloud services that provide sandbox environments via API/SDK. You sign up and get isolated environments on demand.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [Bunnyshell AI Sandboxes](https://www.bunnyshell.com/ai-sandbox-environments/) | Bunnyshell | No | microvm | Firecracker isolation, ~100ms cold starts, Multi-language support, +3 more | Cloud-hosted, Paid tiers | AI sandbox is a newer product line | MCP server integration is notable — direct plugin for Claude Code, Cursor, and Windsurf. |
| [Cloudflare Dynamic Workers](https://developers.cloudflare.com/sandbox/) | Cloudflare | No | v8-isolate | V8 isolate isolation, Millisecond startup, MB-level memory per isolate, +2 more | Cloudflare Workers paid plan, $0.002/unique Worker/day (waived during beta) | JS/TS only (V8 runtime), Not for arbitrary Linux binaries, Weaker isolation than microVMs | Unique edge-first approach using V8 isolates instead of containers/VMs. Credential injection without agent visibility is a strong security feature. Open beta early 2026. |
| [CodeSandbox SDK](https://codesandbox.io/sdk) | CodeSandbox | No | microvm | MicroVM isolation, Parallel agent execution, Web-dev environments, +2 more | Cloud-hosted, SDK integration | Primarily web-dev focused | Well-established brand from the browser IDE space, expanding to agent use. |
| [Daytona](https://www.daytona.io) | Daytona | Yes (Apache-2.0) | container | Docker container isolation, <60ms provisioning, Configurable resources, +2 more | Cloud-hosted managed service, Usage-based pricing | Container-based (shared kernel, weaker isolation than microVMs), Newer platform | Pivoted from CDE space (Feb 2025). $31M Series A (Feb 2026). State management (pause/resume) is a key differentiator vs. ephemeral-only platforms. |
| [E2B](https://e2b.dev) | E2B | Yes (Apache-2.0) | microvm | Firecracker microVM isolation, ~150ms startup, Filesystem isolation, +3 more | Cloud-hosted managed service, Free tier available | 24-hour session limit, Cloud-only, Ephemeral by default, +1 more | One of the earliest and most widely adopted agent sandbox platforms. Docker MCP Catalog partnership. |
| [Fly Sprites](https://sprites.dev) | Fly.io | No | microvm | Firecracker microVM isolation, Persistent 100GB NVMe storage, Checkpoint/restore (~300ms warm), +2 more | Cloud-hosted, API access, 1-12s cold start | Cold starts slower than E2B, Newer product (Jan 2026) | Persistence is the key differentiator — most sandboxes are ephemeral. Checkpoint/restore enables warm resumption of long-running agent sessions. |
| [Koyeb](https://www.koyeb.com) | Koyeb | No | container | Container isolation, Auto-scaling, CI/CD integration | Cloud-hosted, Usage-based pricing | Not agent-specific, General-purpose serverless platform | General-purpose serverless platform, not purpose-built for agents, but usable for agent isolation out of the box with standard container workflows. |
| [Modal](https://modal.com/products/sandboxes) | Modal Labs | No | microvm | Sub-second starts, GPU workloads, Network tunnels, +2 more | Cloud-hosted, Python SDK, Usage-based pricing | Closed source, Cloud-only, Python-centric SDK | Only major sandbox platform with GPU support — unique differentiator for ML/AI workloads that need compute. |
| [Northflank](https://northflank.com) | Northflank | No | kata, gvisor | MicroVM via Kata + gVisor, Unlimited session duration, Any OCI image, +3 more | Cloud-hosted or BYOC, Paid platform | Closed source, More complex setup than simpler platforms | BYOC option is unusual in this space — most cloud sandboxes are single-provider. Production-proven at scale (2M+ workloads/month). |
| [Runloop](https://runloop.ai) | Runloop | No | microvm | Blueprints and Snapshots, Isolated cloud dev environments, SOC 2 compliance, +1 more | Cloud-hosted, Enterprise pricing | Closed source, Enterprise-focused | Enterprise compliance focus (SOC 2) differentiates from developer-oriented alternatives. GA May 2025. |
| [Vercel Sandbox](https://vercel.com) | Vercel | No | microvm | Firecracker microVMs, Node.js + Python support, Up to 45min execution, +1 more | Vercel account, Cloud-hosted | Node.js and Python only, 45-minute maximum execution, Tightly coupled to Vercel ecosystem | Tightly integrated with Vercel deployment pipeline and v0. |

## Agent-Integrated Sandboxes

Sandboxing built directly into AI agent products. These activate automatically or with minimal configuration.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [Claude Code Sandbox](https://code.claude.com/docs/en/sandboxing) | Anthropic | No | user-namespace, seatbelt | Filesystem isolation (CWD read/write, block writes elsewhere), Network isolation (proxy-based domain allowlisting), OS-level enforcement | Claude Code CLI, macOS or Linux | dangerouslyDisableSandbox escape hatch can be triggered by agent itself, macOS sandbox-exec deprecated by Apple, Shared kernel | Demonstrated escape by Ona (March 2026) via dangerouslyDisableSandbox flag. Uses bubblewrap on Linux, Seatbelt on macOS — different mechanisms per OS. |
| [OpenAI Codex Sandbox](https://developers.openai.com/codex/concepts/sandboxing) | OpenAI | No | container, landlock, seccomp | Cloud: isolated containers, two-phase runtime (setup with network, then offline agent), Cloud: per-project network lists, secrets removed before agent, Local: Landlock + seccomp, workspace-only writes | Cloud: OpenAI account + GitHub, Local: Linux kernel 5.13+ | Cloud requires GitHub integration, Local is Linux-only, Network disabled by default in agent phase | Only major agent with sandboxing enabled by default. Two-phase model (online setup, offline agent) is a unique security architecture — the agent never has network access during execution. |

## Standalone / Self-Hosted Tools

Tools you install and run yourself to sandbox any agent or process on your own machine.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [Agent Safehouse](https://github.com/eugene1g/agent-safehouse) | eugene1g | Yes | seatbelt | macOS Seatbelt profile generation, Deny-first policy, Composable profile system, +4 more | macOS only, brew install eugene1g/safehouse/agent-safehouse | macOS only (permanently — sandbox-exec is Apple-specific), sandbox-exec deprecation risk | More mature than it appears — has CI tests, docs site, and thoughtful profile composition. The most polished macOS-specific sandboxing option. |
| [agent-infra/sandbox](https://github.com/agent-infra/sandbox) | agent-infra (community) | Yes | container | Browser automation, Shell access, File management, +2 more | Docker | Container isolation only (shared kernel), Monolithic design | Kitchen-sink approach — good for prototyping and development, less suitable for security-critical production use. |
| [Anthropic sandbox-runtime (srt)](https://github.com/anthropic-experimental/sandbox-runtime) | Anthropic | Yes | user-namespace, seatbelt | Filesystem isolation (directory-level), Network isolation (proxy-based domain filtering with interactive approval), Works for any process, agent, or MCP server | macOS or Linux, No root required on Linux | Experimental/research preview, Not production-hardened, macOS sandbox-exec deprecation risk | Designed to sandbox any process, not just Claude Code. Interactive network approval mode is useful for discovering what network access a tool actually needs. |
| [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/) | Docker | No | microvm | MicroVM isolation (not regular containers), Dedicated Docker daemon per sandbox, Filesystem and network isolation, +1 more | Docker Engine 29.1.5+ (Docker Desktop 4.58+), macOS or Linux | Experimental, MicroVM overhead | Very new (March 2026). Multi-agent support is notable — works with most major coding agents out of the box. |
| [microsandbox](https://github.com/zerocore-ai/microsandbox) | zerocore-ai | Yes | microvm | libkrun microVM isolation, Local-first (no external server), Programmable SDK, +1 more | Linux (KVM) or macOS | Self-hosted only, Smaller community | Local-first is the key differentiator — no credentials leave your machine. Good for privacy-conscious users handling sensitive API keys. |
| [nono](https://nono.sh) | always-further | Yes | landlock, seatbelt | Kernel-level enforcement (Landlock on Linux, Seatbelt on macOS), Credential injection via proxy (keys never enter the sandbox), Atomic rollback with Merkle tree integrity, +4 more | macOS, Linux, or WSL2, brew install nono or single binary | Early alpha — not yet audited | Unique combination of properties no other tool offers: credential proxy (API keys never enter the sandbox), attestation, and atomic rollback. Easy setup (brew install, then nono run -- claude). Very active development. |
| [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) | NVIDIA | Yes (Apache-2.0) | landlock, seccomp | Landlock + seccomp kernel enforcement, Declarative YAML policies, OPA/Rego policy support, +3 more | Linux, Early preview | Early preview, Linux only, No macOS support | NVIDIA backing gives visibility. OPA/Rego policy support targets enterprise governance workflows. Announced at GTC 2026. |
| [scode](https://binds.ch/blog/scode-sandbox-for-ai-coding-tools/) | Laurent Bindschaedler | Yes | process | OS-level sandboxing, Works with any AI coding tool, Filesystem and network restrictions | macOS or Linux | Smaller community project | Early entry in the space (Sept 2025), motivated by Claude Code's initial lack of built-in sandboxing. |

## Kubernetes-Native

Sandbox solutions designed for Kubernetes clusters.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [Agent Sandbox (kubernetes-sigs)](https://github.com/kubernetes-sigs/agent-sandbox) | Kubernetes SIG | Yes (Apache-2.0) | gvisor, kata | Declarative CRD, gVisor + Kata support, Warm pod pool for <1s cold start, +2 more | Kubernetes cluster, gVisor or Kata runtime | Kubernetes required, Still maturing, No standalone mode | Official Kubernetes SIG project (launched KubeCon Atlanta Nov 2025). Likely to become the standard for K8s agent sandboxing. |
| [GKE Agent Sandbox](https://cloud.google.com) | Google Cloud | No | gvisor, kata | Managed gVisor/Kata runtime, GKE integration, Warm pools, +2 more | Google Cloud account, GKE cluster | GKE-only, Vendor lock-in | Managed wrapper around the open-source agent-sandbox project. If you're already on GKE, this is the path of least resistance. |

## Development Environments

Development environment platforms that can be repurposed for agent isolation. These aren't agent-specific but provide usable isolation out of the box.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [Coder](https://github.com/coder/coder) | Coder | Yes (AGPL-3.0) | container | Self-hosted, Container and VM workspaces, Templates, +2 more | Self-hosted on Kubernetes or Docker | No agent-specific features, No MCP integration | Not agent-specific, but good for teams wanting self-hosted isolation without cloud dependency. AGPL license means modifications must be shared. |
| [DevPod](https://github.com/loft-sh/devpod) | Loft Labs | Yes | container | Provider-agnostic (Docker/SSH/K8s/cloud), devcontainer.json support, Client-only (no server), +1 more | Docker or cloud provider | No agent-specific features, No MCP integration, No managed service | Not agent-specific. Good open-source alternative to Codespaces for local-first workflows where you want reproducible isolated environments. |
| [GitHub Codespaces](https://github.com/features/codespaces) | GitHub / Microsoft | No | container | Full Linux VM, devcontainer.json support, Pre-built images, +2 more | GitHub account, Usage-based pricing (free tier available) | Not agent-specific, Higher startup latency, Dev tool, not a sandbox service | Not purpose-built for agents, but accessible to anyone familiar with GitHub. A "good enough" isolation option for personal agent use without learning new tools. |
| [Ona (formerly Gitpod)](https://ona.com) | Ona | No | container | API-first environments, devcontainer.json support, OS-level isolation, +2 more | Cloud-hosted, Enterprise tiers | Rapid pivot — product still evolving, Less sandbox API focus than E2B/Daytona | Major pivot from Gitpod (rebranded Sept 2025). Demonstrated Claude Code sandbox escape (March 2026). Not agent-specific but increasingly agent-oriented. |

## Abstraction Layers

SDKs and frameworks that abstract across multiple sandbox providers.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [ComputeSDK](https://www.computesdk.com) | ComputeSDK | No | microvm, container | Provider-agnostic API, Single SDK for multiple backends | Account with underlying provider | Abstraction adds complexity, Provider-dependent isolation | Useful if you want to avoid vendor lock-in. Isolation strength depends entirely on the chosen backend provider. |
| [LangChain Sandboxes](https://docs.langchain.com/oss/python/deepagents/sandboxes) | LangChain | Yes | container | Framework integration, Provider abstraction, Agent workflow orchestration | LangChain framework, Python | Framework-dependent, Not standalone | Only relevant if already using LangChain. The sandbox capabilities come from the underlying provider, not LangChain itself. |

## Enterprise / Multi-Purpose

Broad-scope platforms covering agent sandboxing alongside evaluation, orchestration, or other capabilities.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [NanoClaw](https://github.com/qwibitai/nanoclaw) | Lazer and Gavriel Cohen | Yes (MIT) | container | Container isolation (Docker/Docker Sandboxes/Apple Container), WhatsApp/Telegram/Slack/Discord/Gmail integration, Memory management, +1 more | Docker or Apple Container | Tied to Claude/Anthropic SDK, Container-level isolation unless using Docker Sandboxes | More of an agent orchestration framework with sandbox support than a sandbox itself. High adoption. Sandbox capability comes from Docker or Docker Sandboxes underneath. |
| [OpenSandbox](https://github.com/alibaba/OpenSandbox) | Alibaba | Yes | container | Multi-language SDKs (Python/Java/JS/C#/Go planned), Unified API, Dual runtime (Docker for dev, K8s for prod), +1 more | Docker or Kubernetes, Self-hosted | Very new (open-sourced March 2026) | Broadest scope of any sandbox — covers evaluation and RL training environments, not just agent sandboxing. |

---

## Building Blocks

The underlying technologies that sandbox products are built on. Most users interact with these indirectly — this section is for people building their own sandbox infrastructure or evaluating isolation claims.

### VM & Container Runtimes

The underlying VM and container runtimes that sandbox products are built on. Use these if you're building your own sandbox infrastructure.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [Firecracker](https://github.com/firecracker-microvm/firecracker) | AWS | Yes (Apache-2.0) | kvm, microvm | KVM hardware isolation, <125ms boot, <5MB memory per VM, +3 more | Linux with KVM, x86_64 or aarch64 | Linux only, No GPU passthrough, Minimal device model, +1 more | The foundation most cloud sandbox platforms build on. Battle-tested at AWS scale (Lambda, Fargate). If you're building a sandbox product, this is likely your starting point. |
| [gVisor](https://github.com/google/gvisor) | Google | Yes (Apache-2.0) | gvisor | Syscall interception in user space, No hardware virtualization needed, OCI-compatible (drop-in runsc runtime), +1 more | Linux, OCI runtime (runsc) | Performance overhead on syscall-heavy workloads, Not all syscalls implemented | Used by GKE and kubernetes-sigs/agent-sandbox. Good middle ground between container and VM isolation — stronger than containers, lighter than full VMs. |
| [Kata Containers](https://github.com/kata-containers/kata-containers) | OpenInfra Foundation | Yes (Apache-2.0) | kata, kvm | Hardware VM per container, OCI/CRI compatible, Multiple VMM backends (QEMU/Cloud Hypervisor/Firecracker), +1 more | Linux with KVM | Higher overhead than gVisor, Requires KVM, More complex setup | Production-proven at scale via Northflank (2M+ workloads/month). Good for Kubernetes environments that need VM-level isolation per pod. |
| [libkrun](https://github.com/containers/libkrun) | Containers project (Red Hat) | Yes (Apache-2.0) | kvm | Library-embeddable (no daemon), KVM isolation, Fast startup, +1 more | Linux (KVM) or macOS (Virtualization.framework) | Less tooling than Firecracker, Smaller community | macOS support via Apple Virtualization.framework is unique among VM runtimes — Firecracker and Kata are Linux-only. Used by microsandbox. |
| [Zeroboot](https://github.com/zerobootdev/zeroboot) | Zeroboot (community) | Yes | kvm, microvm | KVM isolation, Firecracker snapshot COW forking, ~0.8ms sandbox creation, +2 more | Linux with KVM | Very new, Small community | 0.8ms sandbox creation via COW forking is remarkable if verified at scale. Worth watching as a potential next-gen approach to sandbox provisioning. |

### OS-Level Sandboxing

OS-level isolation primitives. These are building blocks — most users interact with them indirectly through higher-level tools.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [bubblewrap (bwrap)](https://github.com/containers/bubblewrap) | Containers project (Flatpak origin) | Yes (LGPL-2.0+) | user-namespace | User namespaces, Mount namespaces, Network namespace, +1 more | Linux with user namespace support | Linux only, Low-level (must compose with other tools) | Years of hardening via Flatpak. Claude Code's Linux sandbox builds on this. The go-to unprivileged sandbox primitive on Linux. |
| [Firejail](https://github.com/netblue30/firejail) | netblue30 (community) | Yes (GPL-2.0) | user-namespace, seccomp | Namespace isolation, seccomp-BPF filtering, Filesystem whitelisting, +3 more | Linux, Setuid binary | SUID is a larger attack surface, Desktop-focused, Linux only | Primarily for desktop app sandboxing, but applicable to agent processes. SUID requirement is a trade-off — convenience vs. attack surface. |
| [Landlock LSM](https://landlock.io) | Linux kernel community | Yes (GPL-2.0) | landlock | Filesystem access restrictions per path, Unprivileged (no root), Stackable with other LSMs, +1 more | Linux kernel 5.13+ (network support in 6.7+) | Filesystem only in early kernel versions, Must combine with seccomp for full coverage, Linux only | The modern Linux answer to unprivileged sandboxing. Network support in kernel 6.7 makes it much more complete. Used by Codex CLI and OpenShell. |
| Linux Namespaces + cgroups | Linux kernel community | Yes (GPL-2.0) | user-namespace | Process isolation (PID namespace), Filesystem isolation (mount namespace), Network isolation (network namespace), +2 more | Linux | Building blocks only — must compose into usable tools, Shared kernel, Linux only | Everything in the container and VM space builds on these primitives. Understanding namespaces and cgroups is foundational to evaluating any Linux-based sandbox's isolation claims. |
| macOS Seatbelt / sandbox-exec | Apple | No | seatbelt | Filesystem access control, Network control, Process restrictions, +1 more | macOS only | sandbox-exec deprecated by Apple, SBPL policy language poorly documented | Deprecated but still the only game in town for macOS process sandboxing. Used by Claude Code, Agent Safehouse, and srt on macOS. No replacement announced by Apple. |
| [nsjail](https://github.com/google/nsjail) | Google | Yes (Apache-2.0) | user-namespace, seccomp | Namespace isolation, seccomp-BPF filtering, cgroup resource limits, +3 more | Linux | Linux only, Less actively maintained, CLI only | Google-maintained. Kafel policy language is more ergonomic than raw seccomp-BPF. Used by competitive programming judges for untrusted code execution. |
| seccomp-BPF | Linux kernel community | Yes (GPL-2.0) | seccomp | Syscall-level filtering, BPF programmability, Kill/trap/errno on forbidden syscalls | Linux kernel 3.5+ | Syscall-level only (no file path awareness), Complex BPF filter authoring, Linux only | Building block, not standalone. Almost always used alongside Landlock or namespaces to provide full sandbox coverage. |

### WebAssembly Runtimes

WebAssembly runtimes providing language-level sandboxing. Architecturally elegant but require compiling tools to Wasm.

| Name | Maintainer | OSS? | Isolation | Key Capabilities | Requirements | Limitations | Notes |
|------|------------|------|-----------|------------------|--------------|-------------|-------|
| [Pyodide](https://github.com/pyodide/pyodide) | Pyodide community (Mozilla origin) | Yes (MPL-2.0) | wasm | Full CPython in Wasm, Browser-grade isolation, Supports NumPy, Pandas, and other scientific packages | Browser or Wasm runtime | Python only, Not all C extensions supported, No native filesystem or network access, +1 more | Good for sandboxing Python-only agent code execution where you need browser-grade isolation guarantees without running a VM. |
| [wasmCloud](https://github.com/wasmCloud/wasmCloud) | wasmCloud community | Yes (Apache-2.0) | wasm | Distributed Wasm applications, Capability-based security model, Provider-based extensibility, +1 more | Cross-platform, NATS for messaging | Must compile to Wasm, More complex than standalone runtimes, Application platform, not just a runtime | Higher-level than Wasmtime or WasmEdge — it's an application platform, not just a runtime. Useful if building distributed agent systems with Wasm isolation. |
| [WasmEdge](https://github.com/WasmEdge/WasmEdge) | CNCF | Yes (Apache-2.0) | wasm | Memory-safe execution, WASI support, AI/ML inference extensions, +2 more | Cross-platform, Must compile tools to Wasm | Must compile to Wasm, Not for arbitrary Linux binaries | CNCF project. Differentiates from Wasmtime with AI/ML inference extensions and edge deployment focus. |
| [Wasmtime](https://github.com/bytecodealliance/wasmtime) | Bytecode Alliance | Yes (Apache-2.0) | wasm | Memory-safe execution, WASI capability-based security, Multi-tenant isolation, +2 more | Cross-platform, Must compile tools to Wasm | Must compile to Wasm, Not for arbitrary Linux binaries, Ecosystem still maturing | The reference Wasm runtime from Bytecode Alliance. Architecturally elegant sandboxing but requires toolchain buy-in — you can't run arbitrary binaries. |
| [Wassette](https://github.com/microsoft/wassette) | Microsoft (Azure Core Upstream) | Yes | wasm | Wasm Component Model, MCP interface, Deny-by-default security, +2 more | Rust toolchain, MCP-compatible agent | Wasm only (must compile tools to Wasm), Early ecosystem | Interesting intersection of MCP and Wasm — agents discover and load sandboxed tools via MCP from OCI registries. Microsoft backing. Released Aug 2025. |

## References

See [references/reading-list.md](references/reading-list.md) for blog posts, papers, and discussions on agent sandboxing.

## Contributing

To add or update a sandbox entry:

1. Edit `data/sandboxes.yaml` — follow the existing schema (all fields documented in the file header)
2. Run `python scripts/generate_readme.py` to regenerate the README
3. Open a PR

The generate script validates the YAML schema and will fail fast on missing required fields or invalid vocabulary values.

