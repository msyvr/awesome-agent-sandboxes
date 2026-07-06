# Detailed Sandboxes Reference

Full information for every sandbox tracked in [awesome-agent-sandboxes](../README.md), grouped by category. Use your browser's back button or the link above to return to the main guide.

## Cloud Managed Sandboxes

<a id="ref-bunnyshell-ai-sandboxes"></a>
### Bunnyshell AI Sandboxes

**Maintainer:** Bunnyshell · **License:** Closed source · [Home](https://www.bunnyshell.com/ai-sandbox-environments/)

Firecracker sandboxes with ~100ms cold starts and MCP Server integration for Claude Code/Cursor/Windsurf.

- **Isolation:** microvm
- **Capabilities:** Firecracker isolation; ~100ms cold starts; Multi-language support; MCP server integration; Snapshots; SDK
- **Requirements:** Cloud-hosted; Paid tiers
- **Limitations:** AI sandbox is a newer product line

_Notes: MCP server integration is notable — direct plugin for Claude Code, Cursor, and Windsurf._

<a id="ref-cloudflare-dynamic-workers"></a>
### Cloudflare Dynamic Workers

**Maintainer:** Cloudflare · **License:** Closed source · [Home](https://developers.cloudflare.com/sandbox/)

V8 isolate-based sandboxing at the edge, claiming 100x faster and more memory-efficient than containers.

- **Isolation:** v8-isolate
- **Capabilities:** V8 isolate isolation; Millisecond startup; MB-level memory per isolate; globalOutbound for HTTP interception; Credential injection without agent visibility
- **Requirements:** Cloudflare Workers paid plan; $0.002/unique Worker/day (waived during beta)
- **Limitations:** JS/TS only (V8 runtime); Not for arbitrary Linux binaries; Weaker isolation than microVMs

_Notes: Unique edge-first approach using V8 isolates instead of containers/VMs. Credential injection without agent visibility is a strong security feature. Open beta early 2026._

<a id="ref-codesandbox-sdk"></a>
### CodeSandbox SDK

**Maintainer:** CodeSandbox · **License:** Closed source · [Home](https://codesandbox.io/sdk)

SDK for giving agents sandboxed MicroVM environments with parallel execution support.

- **Isolation:** microvm
- **Capabilities:** MicroVM isolation; Parallel agent execution; Web-dev environments; File operations; Port forwarding
- **Requirements:** Cloud-hosted; SDK integration
- **Limitations:** Primarily web-dev focused

_Notes: Well-established brand from the browser IDE space, expanding to agent use._

<a id="ref-daytona"></a>
### Daytona

**Maintainer:** Daytona · **License:** Apache-2.0 · [Home](https://www.daytona.io) · [Repo](https://github.com/daytonaio/daytona)

Docker/OCI container-based cloud sandboxes with native state management.

- **Isolation:** container
- **Capabilities:** Docker container isolation; <60ms provisioning; Configurable resources; State management (stop/resume/archive); Python/JS/TS SDKs
- **Requirements:** Cloud-hosted managed service; Usage-based pricing
- **Limitations:** Container-based (shared kernel, weaker isolation than microVMs); Newer platform

_Notes: Pivoted from CDE space (Feb 2025). $31M Series A (Feb 2026). State management (pause/resume) is a key differentiator vs. ephemeral-only platforms._

<a id="ref-e2b"></a>
### E2B

**Maintainer:** E2B · **License:** Apache-2.0 · [Home](https://e2b.dev) · [Repo](https://github.com/e2b-dev/E2B)

Cloud sandbox platform for AI agents using Firecracker microVMs via API/SDK.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVM isolation; ~150ms startup; Filesystem isolation; Network control; Python/JS/TS SDKs; Custom templates
- **Requirements:** Cloud-hosted managed service; Free tier available
- **Limitations:** 24-hour session limit; Cloud-only; Ephemeral by default; No GPU support

_Notes: One of the earliest and most widely adopted agent sandbox platforms. Docker MCP Catalog partnership._

<a id="ref-fly-sprites"></a>
### Fly Sprites

**Maintainer:** Fly.io · **License:** Closed source · [Home](https://sprites.dev)

Persistent Firecracker microVMs for AI agent sessions with 100GB NVMe per sprite.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVM isolation; Persistent 100GB NVMe storage; Checkpoint/restore (~300ms warm); Stateful across sessions; ~$0.07/CPU-hour
- **Requirements:** Cloud-hosted; API access; 1-12s cold start
- **Limitations:** Cold starts slower than E2B; Newer product (Jan 2026)

_Notes: Persistence is the key differentiator — most sandboxes are ephemeral. Checkpoint/restore enables warm resumption of long-running agent sessions._

<a id="ref-modal"></a>
### Modal

**Maintainer:** Modal Labs · **License:** Closed source · [Home](https://modal.com/products/sandboxes)

Serverless cloud platform with sandbox product and best-in-class GPU support.

- **Isolation:** microvm
- **Capabilities:** Sub-second starts; GPU workloads; Network tunnels; Per-sandbox egress policies; 50k+ concurrent sessions
- **Requirements:** Cloud-hosted; Python SDK; Usage-based pricing
- **Limitations:** Closed source; Cloud-only; Python-centric SDK

_Notes: Only major sandbox platform with GPU support — unique differentiator for ML/AI workloads that need compute._

<a id="ref-northflank"></a>
### Northflank

**Maintainer:** Northflank · **License:** Closed source · [Home](https://northflank.com)

Production-grade sandbox infrastructure using Kata Containers and gVisor at 2M+ isolated workloads/month.

- **Isolation:** kata, gvisor
- **Capabilities:** MicroVM via Kata + gVisor; Unlimited session duration; Any OCI image; BYOC (bring your own cloud) deployment; Resource limits; Network controls
- **Requirements:** Cloud-hosted or BYOC; Paid platform
- **Limitations:** Closed source; More complex setup than simpler platforms

_Notes: BYOC option is unusual in this space — most cloud sandboxes are single-provider. Production-proven at scale (2M+ workloads/month)._

<a id="ref-runloop"></a>
### Runloop

**Maintainer:** Runloop · **License:** Closed source · [Home](https://runloop.ai)

Enterprise-grade sandbox infrastructure (Devboxes) with SOC 2 compliance and 10k+ parallel instances.

- **Isolation:** microvm
- **Capabilities:** Blueprints and Snapshots; Isolated cloud dev environments; SOC 2 compliance; High concurrency (10k+ parallel)
- **Requirements:** Cloud-hosted; Enterprise pricing
- **Limitations:** Closed source; Enterprise-focused

_Notes: Enterprise compliance focus (SOC 2) differentiates from developer-oriented alternatives. GA May 2025._

<a id="ref-superserve"></a>
### Superserve

**Maintainer:** superserve-ai · **License:** Apache-2.0 · [Home](https://github.com/superserve-ai/superserve)

Cloud sandbox platform using Firecracker microVMs with TypeScript and Python SDKs.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVM isolation; TypeScript and Python SDKs; Managed cloud service
- **Requirements:** Cloud-hosted (superserve.ai sign-up)
- **Limitations:** Beta; SDK is open source but sandbox backend is private

_Notes: Firecracker-based like E2B. SDK is open source (Apache-2.0) but the sandbox backend infrastructure is in a separate private repo. Beta — evaluate maturity before committing to production use._

<a id="ref-vercel-sandbox"></a>
### Vercel Sandbox

**Maintainer:** Vercel · **License:** Closed source · [Home](https://vercel.com)

Firecracker microVM sandboxes for untrusted code, powering v0's code generation runtime.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVMs; Node.js + Python support; Up to 45min execution; Up to 8 vCPUs / 2GB per vCPU
- **Requirements:** Vercel account; Cloud-hosted
- **Limitations:** Node.js and Python only; 45-minute maximum execution; Tightly coupled to Vercel ecosystem

_Notes: Tightly integrated with Vercel deployment pipeline and v0._

## Agent-Integrated Sandboxes

<a id="ref-claude-code-sandbox"></a>
### Claude Code Sandbox

**Maintainer:** Anthropic · **License:** Closed source · [Home](https://code.claude.com/docs/en/sandboxing)

Native OS-level sandboxing using bubblewrap (Linux) and Seatbelt/sandbox-exec (macOS), reducing permission prompts by 84%.

- **Isolation:** user-namespace, seatbelt
- **Capabilities:** Filesystem isolation (CWD read/write, block writes elsewhere); Network isolation (proxy-based domain allowlisting); OS-level enforcement
- **Requirements:** Claude Code CLI; macOS or Linux
- **Limitations:** dangerouslyDisableSandbox escape hatch can be triggered by agent itself; macOS sandbox-exec deprecated by Apple; Shared kernel

_Notes: Demonstrated escape by Ona (March 2026) via dangerouslyDisableSandbox flag. Uses bubblewrap on Linux, Seatbelt on macOS — different mechanisms per OS._

<a id="ref-loop"></a>
### loop

**Maintainer:** radutopala (Radu Topala) · **License:** Apache-2.0 · [Home](https://github.com/radutopala/loop)

Multi-platform (desktop, Slack, Discord) Claude Code runner that traps syscalls inside Docker containers via seccomp RET_USER_NOTIF and routes each trap to a three-button chat approval card, with a body-filtering Docker API proxy as a second gate.

- **Isolation:** container, seccomp
- **Capabilities:** Hand-written seccomp BPF filter via RET_USER_NOTIF traps 12 syscalls (connect, execve, execveat, openat, openat2, renameat2, unlinkat, linkat, symlinkat, fchmodat, fchownat, mkdirat); ERRNO-denies io_uring family (closes seccomp bypass); PR_SET_NO_NEW_PRIVS + TSYNC; arch-locked with kill-process on mismatch; Trap blocks in kernel's seccomp_do_user_notification until chat click resolves; Three-button approval cards (once / session / deny / deny-session) routed to Slack or Discord; Per-container Approval Manager caches session decisions; rate limits; Docker HTTP proxy with JSONPath-lite body filtering on POST /containers/create; Symlink-resolved bind-mount source paths to defeat /workdir/link bind-escape; Bundles Claude Code; desktop, Slack, and Discord front-ends
- **Requirements:** Linux (seccomp RET_USER_NOTIF is Linux-only); Docker
- **Limitations:** Solo maintainer; project ~3 months old at time of inclusion; Approval UX depends on a responsive operator or session-cached "allow"; macOS and Windows not supported

_Notes: Differentiator vs commodity Docker-tier entries is the seccomp RET_USER_NOTIF + chat-routed HITL approval stack: kernel-parked traps resume only on SECCOMP_IOCTL_NOTIF_SEND with the CONTINUE flag, with path arguments read via process_vm_readv and symlink-resolved before the chat card is rendered. README credits agentsh for design inspiration; novel axis here is HITL governance via team chat rather than CLI prompts. ~11,500 LOC with a 1:1 test ratio despite low star count — code is production-grade on the security-critical paths._

<a id="ref-openai-codex-sandbox"></a>
### OpenAI Codex Sandbox

**Maintainer:** OpenAI · **License:** Closed source · [Home](https://developers.openai.com/codex/concepts/sandboxing)

Two modes: cloud (isolated containers, internet disabled during agent phase) and local CLI (Landlock + seccomp on Linux).

- **Isolation:** container, landlock, seccomp
- **Capabilities:** Cloud: isolated containers, two-phase runtime (setup with network, then offline agent); Cloud: per-project network lists, secrets removed before agent; Local: Landlock + seccomp, workspace-only writes
- **Requirements:** Cloud: OpenAI account + GitHub; Local: Linux kernel 5.13+
- **Limitations:** Cloud requires GitHub integration; Local is Linux-only; Network disabled by default in agent phase

_Notes: Only major agent with sandboxing enabled by default. Two-phase model (online setup, offline agent) is a unique security architecture — the agent never has network access during execution._

<a id="ref-pi-sandbox"></a>
### pi-sandbox

**Maintainer:** carderne (Chris Arderne) · **License:** MIT · [Home](https://github.com/carderne/pi-sandbox)

Sandbox extension for the pi coding agent that wraps bash subprocesses with macOS sandbox-exec / Linux bubblewrap and intercepts read/write/edit tool calls with allow/deny lists and interactive permission prompts.

- **Isolation:** seatbelt, user-namespace
- **Capabilities:** macOS Seatbelt (sandbox-exec) for bash subprocesses; Linux bubblewrap for bash subprocesses; In-process policy enforcement for read/write/edit tools; Four-tier permission persistence (Abort / session / project / global); Asymmetric read/write rule precedence (denyWrite is hard-block, denyRead is overridable default); Project config via .pi/sandbox.json, global via ~/.pi/agent/sandbox.json; /sandbox slash command in pi
- **Requirements:** pi coding agent; macOS or Linux; Anthropic sandbox-runtime; ripgrep
- **Limitations:** Specific to pi agent only; In-process file tool policy is not OS-enforced; README acknowledges example browser config opens "significant security loopholes"

_Notes: Thin agent-specific layer atop Anthropic sandbox-runtime, demonstrating that runtime as a reusable library for non-Anthropic agents. Differentiator over Claude Code's sandbox is the four-tier permission persistence with explicit asymmetric precedence between read and write rules._

## Standalone / Self-Hosted Tools

<a id="ref-agent-safehouse"></a>
### Agent Safehouse

**Maintainer:** eugene1g · **License:** OSS · [Home](https://github.com/eugene1g/agent-safehouse)

macOS sandbox-exec profile system with deny-first policy, composable profiles, and pre-built agent configurations.

- **Isolation:** seatbelt
- **Capabilities:** macOS Seatbelt profile generation; Deny-first policy; Composable profile system; Pre-built profiles for major coding agents; Policy builder web tool; Fine-grained HOME access control; Symlink-aware path resolution
- **Requirements:** macOS only; brew install eugene1g/safehouse/agent-safehouse
- **Limitations:** macOS only (permanently — sandbox-exec is Apple-specific); sandbox-exec deprecation risk

_Notes: More mature than it appears — has CI tests, docs site, and thoughtful profile composition. The most polished macOS-specific sandboxing option._

<a id="ref-agent-infra-sandbox"></a>
### agent-infra/sandbox

**Maintainer:** agent-infra (community) · **License:** OSS · [Home](https://github.com/agent-infra/sandbox)

All-in-one sandbox combining Browser, Shell, File management, MCP, and VSCode Server in a single Docker container.

- **Isolation:** container
- **Capabilities:** Browser automation; Shell access; File management; MCP integration; VSCode Server
- **Requirements:** Docker
- **Limitations:** Container isolation only (shared kernel); Monolithic design

_Notes: Kitchen-sink approach — good for prototyping and development, less suitable for security-critical production use._

<a id="ref-agent-sandbox"></a>
### agent_sandbox

**Maintainer:** katosh · **License:** MIT · [Home](https://github.com/katosh/agent_sandbox)

Kernel-enforced user-space sandbox for AI coding agents with multi-backend isolation (bubblewrap, firejail, Landlock LSM) and a Slurm "chaperon" proxy that propagates sandboxing onto HPC compute nodes.

- **Isolation:** user-namespace, landlock, seccomp
- **Capabilities:** Bubblewrap primary backend (user namespaces + bind mounts, no setuid required); Firejail and Landlock LSM fallback backends; Generated seccomp-BPF filters per syscall (x86_64 and aarch64); Slurm chaperon proxy wrapping sbatch/srun/squeue/scancel/scontrol/sacct/sacctmgr; In-sandbox Slurm stubs talk to outside chaperon via named pipes; Whitelist validation of Slurm flags; denies --pty/--container/--uid/--prolog/--bcast/--get-user-env; Sandbox-exec wrapping injected onto allocated compute nodes; Supports Claude Code, Codex, Gemini, Aider, OpenCode, pi-mono
- **Requirements:** Linux; Bubblewrap (or firejail/Landlock-capable kernel)
- **Limitations:** Linux-only — no macOS path; No egress allowlist or credential proxy (acknowledged in landscape doc); Author flags as "best-effort user-space isolation, not a security product"; Young project (2 critical / 3 high pentest findings documented and addressed)

_Notes: Only sandbox surveyed with first-class HPC/Slurm awareness — the chaperon proxy intercepts Slurm submission and wraps job commands so an agent cannot escape by submitting an unsandboxed job to a compute node. Munge auth is deliberately blocked inside the sandbox so only the outside chaperon can submit. Bind-mount filesystem isolation returns ENOENT rather than EACCES, which sidesteps the ld-linux and /proc/self/root evasions that have hit Landlock-allowlist sandboxes. Ships with a 32 KB threat model and a documented pentest cycle._

<a id="ref-agentsh"></a>
### agentsh

**Maintainer:** canyonroad · **License:** Apache-2.0 · [Home](https://github.com/canyonroad/agentsh)

Policy-enforced execution gateway that intercepts file, network, process, and signal syscalls for agent commands with allow/deny/approve/redirect decisions and structured audit.

- **Isolation:** process, landlock, seatbelt
- **Capabilities:** Syscall interception (file, network, process, signal); Subprocess tree coverage; Allow/deny/approve/redirect policy decisions; Structured audit events; Pairs with containers; Cross-platform (Linux LSM/FUSE, macOS ESF+NE, Windows minifilter); Linux is production-ready; macOS alpha; Windows pending driver signing
- **Requirements:** Linux (production), macOS (alpha), or Windows (pending); Homebrew, .deb, .rpm, or .apk install
- **Limitations:** macOS support is alpha; Windows support pending driver signing

_Notes: Real runtime enforcement, not just wrapping. The "redirect" policy decision is unusual — can transparently steer agent network calls or out-of-workspace writes to scratch dirs without the agent knowing it was redirected._

<a id="ref-ai-sandbox-wrapper"></a>
### ai-sandbox-wrapper

**Maintainer:** kokorolx · **License:** OSS · [Home](https://github.com/nano-step/ai-sandbox-wrapper)

npm CLI that wraps Docker for coding agents (opencode, amp, droid) with workspace whitelisting, capability dropping, and Git fetch-only mode.

- **Isolation:** container
- **Capabilities:** Docker container isolation; Workspace whitelisting (filesystem boundary); Non-root execution; CAP_DROP=ALL (drops all Linux capabilities); Explicit API key passing; Git fetch-only mode (egress restriction); Targets opencode, amp, droid coding agents
- **Requirements:** Docker; npm install -g @kokorolx/ai-sandbox-wrapper
- **Limitations:** No LICENSE file in repo (legal status unclear); Solo maintainer; Container isolation only (shared kernel)

_Notes: Opinionated hardening over default Docker — capability dropping and Git fetch-only mode are substantive choices most Docker wrappers don't make. No license means the code is technically all-rights-reserved by default; consider asking the author to add one before relying on it._

<a id="ref-aide"></a>
### aide

**Maintainer:** jskswamy · **License:** MIT · [Home](https://github.com/jskswamy/aide)

Unified agent launcher with capability-based permission model and OS-native sandbox enforcement on macOS.

- **Isolation:** seatbelt
- **Capabilities:** Capability-based permission model (19 built-in capabilities); Composable grants with never-allow hard denials; macOS Seatbelt sandbox enforcement; Per-project context resolution (agent, credentials, capabilities); Supports multiple agents from a single launcher
- **Requirements:** macOS (sandbox enforcement); Go
- **Limitations:** Linux sandbox not yet implemented (Landlock + seccomp planned); macOS-only sandbox enforcement today; Early project (v0.1.0)

_Notes: The capability model is the differentiator — 19 built-in capabilities (docker, k8s, aws, etc.) with composable grants and never-allow hard denials. More opinionated than fence or Agent Safehouse about what agents should be allowed to do. Linux sandbox is planned but not yet implemented._

<a id="ref-alcless"></a>
### alcless

**Maintainer:** AkihiroSuda · **License:** Apache-2.0 · [Home](https://github.com/AkihiroSuda/alcless)

macOS sandbox using separate local user accounts for process/filesystem isolation with rsync workspace sync and user-confirmed sync-back.

- **Isolation:** process
- **Capabilities:** Separate macOS user account isolation; rsync-based workspace isolation; User-confirmed file sync-back; Mach bootstrap subset isolation via pam_launchd; No VM or container overhead
- **Requirements:** macOS only
- **Limitations:** macOS only (by design — Linux/FreeBSD have containers); Requires sudo for user switching; Early project

_Notes: From AkihiroSuda (maintainer of Lima, nerdctl). Deliberately positioned as the lightweight complement to Lima (VM-based). Zero VM overhead — just Unix user separation. The rsync + confirm workflow means changes don't land on the host without approval._

<a id="ref-anthropic-sandbox-runtime-srt"></a>
### Anthropic sandbox-runtime (srt)

**Maintainer:** Anthropic · **License:** Apache-2.0 · [Home](https://github.com/anthropic-experimental/sandbox-runtime)

Lightweight sandboxing for arbitrary processes using bubblewrap (Linux) and Seatbelt (macOS), no container required.

- **Isolation:** user-namespace, seatbelt
- **Capabilities:** Filesystem isolation (directory-level); Network isolation (proxy-based domain filtering with interactive approval); Works for any process, agent, or MCP server
- **Requirements:** macOS or Linux; No root required on Linux
- **Limitations:** Experimental/research preview; Not production-hardened; macOS sandbox-exec deprecation risk

_Notes: Designed to sandbox any process, not just Claude Code. Interactive network approval mode is useful for discovering what network access a tool actually needs._

<a id="ref-brood-box"></a>
### brood-box

**Maintainer:** Stacklok · **License:** Apache-2.0 · [Home](https://github.com/stacklok/brood-box)

CLI that runs coding agents inside hardware-isolated microVMs with COW workspace snapshots and interactive per-file diff review before changes land.

- **Isolation:** kvm, microvm
- **Capabilities:** Hardware VM isolation (libkrun/KVM on Linux, Hypervisor.framework on macOS); COW workspace snapshots; Interactive per-file diff review (VM stopped before review, TOCTOU-resistant); DNS-aware egress firewall; Ephemeral SSH keys; Non-overridable secret exclusions; Permission stripping on flush
- **Requirements:** Linux (KVM) or macOS (Apple Silicon, Hypervisor.framework)
- **Limitations:** Experimental

_Notes: From Stacklok (founded by Luke Hinds of Sigstore). Hardware VM isolation like cleanroom, but adds TOCTOU-resistant diff review — the VM is stopped before the user reviews changes, preventing the agent from modifying files during review. DNS egress firewall and non-overridable secret exclusions are strong default posture._

<a id="ref-cleanroom"></a>
### cleanroom

**Maintainer:** Buildkite · **License:** OSS · [Home](https://github.com/buildkite/cleanroom)

Self-hosted microVM sandbox using Firecracker (Linux) or Apple Virtualization.framework (macOS) with deny-by-default network and host-side credential proxy.

- **Isolation:** microvm, kvm
- **Capabilities:** Firecracker microVMs (Linux); Apple Virtualization.framework (macOS); Deny-by-default egress with policy-controlled allowlists; Host-side credential proxy (credentials never enter sandbox); Repo-scoped cleanroom.yaml network policy; Docker-inside-sandbox support
- **Requirements:** Linux (KVM) or macOS
- **Limitations:** Early project; No LICENSE file in repo

_Notes: From Buildkite (established CI company). Strongest isolation in recent discovery batches — hardware VM boundary, not containers or namespaces. Credential proxy model is similar to nono (keys never enter the sandbox). cleanroom.yaml per-repo policy is a clean declarative approach._

<a id="ref-code-on-incus"></a>
### code-on-incus

**Maintainer:** mensfeld · **License:** MIT · [Home](https://github.com/mensfeld/code-on-incus)

Hardened Incus container sandbox with real-time nftables threat detection (reverse shells, C2, DNS tunneling, exfiltration) and automated container pause/kill response.

- **Isolation:** container, seccomp
- **Capabilities:** Incus unprivileged system containers (seccomp, AppArmor, UID remapping); Firewalld network isolation (restricted/allowlist/open modes); Real-time nftables threat detection daemon; Automated container pause/kill on threat detection; Protected paths via read-only mounts + chattr +i; Supply-chain hardening (read-only .git/hooks, .husky, .vscode); Credential isolation (host credentials not mounted); Health-check command verifying seccomp/AppArmor/privilege posture
- **Requirements:** Linux (native); macOS via Lima/Colima VM
- **Limitations:** Container isolation (shared kernel); Linux-native (macOS requires VM layer)

_Notes: Goes beyond isolation into active defense — the monitoring daemon uses kernel-level nftables packet inspection to detect reverse shells, C2 callbacks, DNS tunneling, and data exfiltration patterns, then auto-pauses or kills the container. Supply-chain hardening (read-only git hooks) is a detail most sandboxes miss._

<a id="ref-containarium"></a>
### Containarium

**Maintainer:** FootprintAI · **License:** Apache-2.0 · [Home](https://containarium.dev) · [Repo](https://github.com/FootprintAI/Containarium)

Self-hostable agent runtime that gives each agent a persistent, SSH-reachable LXC/Incus box with per-tenant network isolation and an in-box MCP server; Kubernetes and LXC backends with GPU passthrough.

- **Isolation:** container
- **Capabilities:** Persistent, SSH-reachable LXC/Incus box per agent; Per-tenant network isolation (agent holds an SSH key, not a kube-apiserver token); Userspace SOCKS5 egress proxy for network policy; MCP-native admin CLI plus a second MCP server running inside the box; Kubernetes and LXC/Incus backends; GPU passthrough; Port exposure to the public internet
- **Requirements:** Linux with LXC/Incus, or Kubernetes; Go 1.25 to build; Self-hosted
- **Limitations:** eBPF egress policy is experimental (under experimental/); the enforced egress path is the SOCKS5 proxy; In-box file-ops sandbox (AGENTBOX_ROOT) is opt-in, default-off; Container isolation (shared kernel)

_Notes: SSH-native per-tenant LXC/Incus boxes; blast radius is bounded by an SSH key rather than a cluster token. Ships two MCP servers (host admin and an in-box shell_exec). The tagline advertises eBPF egress, but that code is experimental — the shipping egress control is a userspace SOCKS5 proxy._

<a id="ref-cua"></a>
### cua

**Maintainer:** trycua · **License:** MIT · [Home](https://www.trycua.com) · [Repo](https://github.com/trycua/cua)

Open-source infrastructure for computer-use agents providing OS-level VM sandboxes (macOS, Windows, Linux, Android) via QEMU and Apple Virtualization.framework with a unified SDK for screen, mouse, and keyboard control.

- **Isolation:** microvm
- **Capabilities:** Multi-OS desktop sandboxes (macOS, Windows, Linux, Android); Apple Virtualization.framework on Apple Silicon (Lume); QEMU-based VMs for Linux/Windows (lumier); Unified SDK for screen capture, mouse, keyboard, multi-touch; Computer-use agent benchmarks (OSWorld, ScreenSpot, Windows Arena); Optional cuabot wrapper with H.265 streaming and shared clipboard; BYOI .qcow2/.iso support; Optional cua.ai cloud-managed offering
- **Requirements:** macOS, Linux, or Windows (depending on backend); Apple Silicon for native macOS VMs via Lume
- **Limitations:** Bundled "Cua Driver" component runs unsandboxed on host (use Sandbox/Lume/cuabot for isolation); Optional ML components include AGPL-3.0 (ultralytics) and CC-BY-4.0 (OmniParser)

_Notes: Provisions full graphical desktops for macOS, Windows, Linux, and Android — distinct from container/microVM sandboxes that only give Linux shells. One of few options that legally and performantly virtualizes macOS for agent workloads, via Apple Virtualization.framework on Apple Silicon. Designed for visual/UI-driven agents rather than code-execution agents._

<a id="ref-docker-sandboxes"></a>
### Docker Sandboxes

**Maintainer:** Docker · **License:** Closed source · [Home](https://docs.docker.com/ai/sandboxes/)

MicroVM sandboxes for AI coding agents, each with its own Docker daemon, filesystem, and network.

- **Isolation:** microvm
- **Capabilities:** MicroVM isolation (not regular containers); Dedicated Docker daemon per sandbox; Filesystem and network isolation; Supports Claude Code, Codex, Copilot, Gemini, Kiro
- **Requirements:** Docker Engine 29.1.5+ (Docker Desktop 4.58+); macOS or Linux
- **Limitations:** Experimental; MicroVM overhead

_Notes: Very new (March 2026). Multi-agent support is notable — works with most major coding agents out of the box._

<a id="ref-edgebox"></a>
### EdgeBox

**Maintainer:** BIGPPWONG · **License:** GPL-3.0 · [Home](https://github.com/BIGPPWONG/EdgeBox)

Local Electron/Docker desktop app that runs LLM agents in isolated Docker containers with both CLI and full GUI (VNC) desktop environments, exposed via MCP.

- **Isolation:** container
- **Capabilities:** Docker container isolation per session; Full GUI desktop environment (VNC) for computer-use agents; CLI shell environments; Multi-session concurrency with separate containers; MCP protocol support
- **Requirements:** Docker; Electron (desktop app)
- **Limitations:** Container isolation only (shared kernel); GPL-3.0 license

_Notes: The GUI desktop environment (VNC) is the differentiator — agents can operate browsers and desktop apps, not just execute code. Essentially a self-hosted E2B with a GUI layer for computer-use agent workflows._

<a id="ref-envpod-ce"></a>
### envpod-ce

**Maintainer:** markamo · **License:** BSL-1.1 · [Home](https://github.com/markamo/envpod-ce)

Linux governance sandbox using OverlayFS COW, namespaces, cgroups v2, and seccomp-BPF with a diff/commit/rollback workflow for agent changes to host files.

- **Isolation:** user-namespace, seccomp
- **Capabilities:** OverlayFS copy-on-write (agents work on real files, changes staged); Linux namespaces (PID, net, mount, UTS, user); cgroups v2 resource limits; seccomp-BPF syscall filtering; Per-pod DNS with allowlisting; Encrypted credential vault; Diff/commit/rollback workflow for host changes; Jailbreak test suite included
- **Requirements:** Linux only; Single-binary Rust install
- **Limitations:** Linux only; BSL-1.1 license (not OSI-approved open source); Very early (v0.1.15, 9 stars)

_Notes: The diff/commit/rollback workflow is unique — agents work on real host files via an OverlayFS overlay, and changes are staged for human review before committing to the host. Most sandboxes either fully isolate (agent can't touch host files) or don't isolate at all. This is a middle ground that enables real work with reversibility. BSL-1.1 license restricts production use without a commercial license._

<a id="ref-fence"></a>
### fence

**Maintainer:** Tusk · **License:** Apache-2.0 · [Home](https://github.com/Use-Tusk/fence)

Container-free CLI sandbox using OS-native primitives for network domain allowlisting, filesystem access control, and command deny-lists.

- **Isolation:** seatbelt, user-namespace
- **Capabilities:** macOS sandbox-exec (Seatbelt); Linux bubblewrap + socat for network bridging; Network domain allowlisting; Filesystem access control; Command deny-lists; Built-in templates for Claude Code, Codex, Amp, Gemini CLI, Copilot; Go library for programmatic use
- **Requirements:** macOS or Linux; Homebrew, Nix, or Go install
- **Limitations:** macOS sandbox-exec deprecation risk; Process-level isolation (shared kernel)

_Notes: Lightest-weight option for wrapping agent processes with real isolation — no container runtime needed. Inspired by Anthropic's srt. Built-in agent templates mean zero config for common agents. Well-documented security model and architecture._

<a id="ref-gocker"></a>
### gocker

**Maintainer:** lunguini · **License:** Apache-2.0 · [Home](https://github.com/lunguini/gocker)

Docker-compatible CLI and API daemon for Apple Container on macOS 26+, where each container runs as a hardware-isolated Linux microVM.

- **Isolation:** microvm
- **Capabilities:** Apple Container (Virtualization.framework) microVMs; Docker-compatible CLI and REST API; Docker compose support; Configurable isolation modes (full/hybrid/shared); gocker sandbox run claude command for agent sandboxing; Claude session sync; Portainer and Testcontainers compatible
- **Requirements:** macOS 26+ (Apple Silicon)
- **Limitations:** macOS only; Very early (6 stars); Requires macOS 26+

_Notes: Different from cleanroom/sand/locki — gocker is a Docker replacement on macOS, not an embeddable sandbox library. The Docker-compatible API means existing Docker workflows and tools (compose, Portainer, Testcontainers) work out of the box, but each container is a hardware-isolated microVM via Apple Virtualization.framework._

<a id="ref-gondolin"></a>
### gondolin

**Maintainer:** earendil-works · **License:** Apache-2.0 · [Home](https://github.com/earendil-works/gondolin)

TypeScript-controlled Linux microVM sandbox (QEMU/KVM or libkrun) with programmable network egress hooks and per-secret credential injection.

- **Isolation:** kvm, microvm
- **Capabilities:** Hardware VM isolation (QEMU/KVM default, experimental libkrun); TypeScript control plane (programmable sandbox API); Host-side HTTP/TLS egress hooks; Per-secret, per-destination credential injection (agent never sees real keys); Filesystem controls; Snapshot and resume; macOS + Linux
- **Requirements:** Linux (KVM) or macOS (libkrun/Hypervisor.framework); Node.js / TypeScript
- **Limitations:** libkrun backend is experimental; Linux-focused (macOS via experimental backend)

_Notes: The programmable egress hooks are the differentiator — host-side HTTP/TLS interception with per-secret, per-destination injection gives fine-grained control over what credentials reach which endpoints, without the agent ever seeing the real values. Similar credential model to nono and cleanroom but with a TypeScript programmable control plane rather than CLI/config._

<a id="ref-hazmat"></a>
### hazmat

**Maintainer:** dredozubov · **License:** MIT · [Home](https://github.com/dredozubov/hazmat)

macOS triple-layer containment stacking a dedicated user account, per-session Seatbelt kernel sandbox, and pf firewall with DNS blocklists and Kopia snapshots.

- **Isolation:** seatbelt, process
- **Capabilities:** Dedicated macOS agent user (blocks ~/.ssh, ~/.aws, Keychain); Per-session Seatbelt kernel sandbox (default-deny filesystem); pf packet filter scoped to agent user; DNS blocklists (ngrok, pastebin, webhook.site); Supply-chain hardening (npm ignore-scripts by default); Kopia backup snapshots; TLA+ formally verified session lifecycle and policy structure
- **Requirements:** macOS only; Homebrew install
- **Limitations:** macOS only; Seatbelt is undocumented by Apple; HTTPS exfiltration not blocked; /tmp is shared

_Notes: Strongest macOS-specific sandbox — layers everything alcless (user isolation) and Agent Safehouse (Seatbelt) do individually, plus pf firewall and DNS blocklists. TLA+ formal verification of session lifecycle is unusual rigor for a sandbox tool. Honest about limitations (HTTPS exfil, shared /tmp)._

<a id="ref-hole"></a>
### hole

**Maintainer:** lukashornych · **License:** Apache-2.0 · [Home](https://github.com/lukashornych/hole)

CLI that runs AI agents inside ephemeral Docker/Podman containers with proxy-based network domain whitelisting and configurable filesystem exclusions.

- **Isolation:** container
- **Capabilities:** Docker and Podman container isolation; Proxy-based network domain whitelisting (three profiles); --dump-network-access logging; File exclusion via bind-mount overrides; Docker-in-Docker support for agents that need containers; Ephemeral containers (destroyed on exit); Non-root user inside container
- **Requirements:** Docker or Podman; Linux, macOS, or WSL
- **Limitations:** Container isolation only (shared kernel); Solo maintainer; Early project

_Notes: The --dump-network-access flag is useful for discovering what network access an agent actually needs — similar to Anthropic srt's interactive approval mode but post-hoc. Docker-in-Docker support is unusual and needed for agents that themselves use containers._

<a id="ref-jailoc"></a>
### jailoc

**Maintainer:** Seznam · **License:** MIT · [Home](https://github.com/seznam/jailoc)

Per-workspace Docker Compose sandbox for OpenCode agents with iptables egress filtering, dropped capabilities, and a DinD sidecar to avoid host socket mounting.

- **Isolation:** container
- **Capabilities:** Per-workspace Docker Compose sandboxes; iptables egress filtering (blocks RFC 1918, link-local, CGNAT by default); UID 1000, dropped capabilities, no_new_privs; DinD sidecar instead of mounting docker.sock; OpenCode agent integration; Renovate-pinned base image
- **Requirements:** Docker; Linux
- **Limitations:** OpenCode-specific defaults (sandboxing model is general); Container isolation only (shared kernel)

_Notes: Backed by Seznam (Czech search engine). Network isolation via iptables allowlist prevents pivot to internal infra. The DinD sidecar approach avoids the common docker.sock mount escape vector._

<a id="ref-lince"></a>
### LINCE

**Maintainer:** RisorseArtificiali · **License:** MIT · [Home](https://lince.sh) · [Repo](https://github.com/RisorseArtificiali/lince)

Multi-agent TUI dashboard (Zellij-based) that orchestrates parallel CLI coding agents inside a bundled bubblewrap-based agent-sandbox module, with experimental nono backend on macOS.

- **Isolation:** user-namespace
- **Capabilities:** Bubblewrap-based agent-sandbox module (usable independently); Filesystem isolation and bind-mount control; Environment variable filtering; Process namespace isolation (hides host processes); Blocks git push out of sandbox; Multi-agent parallel execution via Zellij panes (up to 8 agents); Real-time status and token tracking dashboard; VoxCode/Whisper voice input integration; Experimental macOS support via nono backend
- **Requirements:** Linux (Fedora 43 tested; Ubuntu/Debian/Arch claimed); bubblewrap; Zellij
- **Limitations:** macOS support flagged experimental (delegates to nono); Standard bubblewrap isolation, no novel security primitive; Early-stage (16 stars)

_Notes: Bundled agent-sandbox module is usable independently of the dashboard (agent-sandbox run -a codex). Differentiator is the multi-agent TUI orchestration plus voice input layered on standard bubblewrap isolation, packaged as a complete coding workstation._

<a id="ref-llm-sandbox"></a>
### llm-sandbox

**Maintainer:** vndee · **License:** MIT · [Home](https://github.com/vndee/llm-sandbox)

Lightweight Python library for executing LLM-generated code inside Docker, Podman, or Kubernetes containers with network isolation and resource limits.

- **Isolation:** container
- **Capabilities:** Multi-backend (Docker, Podman, Kubernetes); Network isolation; Resource limits; Security policies; MCP integration; PyPI published
- **Requirements:** Docker, Podman, or Kubernetes; Python
- **Limitations:** Container isolation only (shared kernel); Code interpreter focus (not general agent sandboxing)

_Notes: Multi-backend support is the differentiator — same API across Docker, Podman, and K8s. Good for sandboxing LLM-generated code execution specifically. SonarCloud + codecov CI suggests reasonable code quality standards._

<a id="ref-locki"></a>
### locki

**Maintainer:** JanPokorny · **License:** OSS · [Home](https://github.com/JanPokorny/locki)

CLI that runs coding agents inside Incus containers in a shared Lima VM, with auto-managed git worktrees and a host-side SSH git proxy.

- **Isolation:** kvm, container
- **Capabilities:** VM isolation via Lima/QEMU; Container isolation via Incus; Auto-managed git worktrees; Host-side SSH git proxy with command allowlist; Supports claude, gemini, codex, opencode, shell
- **Requirements:** macOS or Linux; Lima and Incus; pip or uv install
- **Limitations:** No LICENSE file in repo (legal status unclear); Author explicitly disclaims security guarantees; No exfiltration protection; Solo maintainer; Very early

_Notes: One of the few sandboxes that layers VM (Lima/QEMU) plus container (Incus) for coding agents — interesting design worth tracking. Author is candid about "no security guarantees" in the README. No license means the code is technically all-rights-reserved by default; consider asking the author to add one before relying on it._

<a id="ref-microsandbox"></a>
### microsandbox

**Maintainer:** zerocore-ai · **License:** OSS · [Home](https://github.com/zerocore-ai/microsandbox)

Local-first programmable sandboxes using libkrun microVMs, designed for sensitive API keys with no external server.

- **Isolation:** microvm
- **Capabilities:** libkrun microVM isolation; Local-first (no external server); Programmable SDK; Agent Skills for Claude Code, Cursor, Codex, Gemini, Copilot
- **Requirements:** Linux (KVM) or macOS
- **Limitations:** Self-hosted only; Smaller community

_Notes: Local-first is the key differentiator — no credentials leave your machine. Good for privacy-conscious users handling sensitive API keys._

<a id="ref-monty"></a>
### monty

**Maintainer:** Pydantic · **License:** MIT · [Home](https://github.com/pydantic/monty)

Minimal, secure Python interpreter written in Rust providing language-runtime sandboxing for AI-generated code with no host access except via explicit caller-provided functions.

- **Isolation:** process
- **Capabilities:** Custom Python interpreter in Rust; No filesystem, env, or network access by default; Caller-provided functions for explicit host integration; Memory, stack, and time limits; Snapshotting
- **Requirements:** pip install pydantic-monty
- **Limitations:** Experimental — explicitly not ready for production; Python subset only (not full CPython)

_Notes: Different approach from Pyodide — a custom Rust interpreter rather than CPython compiled to Wasm. Will power Pydantic AI's codemode feature. Backed by Pydantic, but explicitly experimental. Categorized in the wasm tier because language-runtime sandboxing fits the same isolation strength characterization (fastest/lightest, limited to specific runtimes), even though it's not actually Wasm._

<a id="ref-nono"></a>
### nono

**Maintainer:** nolabs-ai · **License:** Apache-2.0 · [Home](https://nono.sh) · [Repo](https://github.com/nolabs-ai/nono)

Kernel-enforced agent sandbox with credential proxy, atomic rollback, Sigstore attestation, and cryptographic audit chain.

- **Isolation:** landlock, seatbelt
- **Capabilities:** Kernel-level enforcement (Landlock on Linux, Seatbelt on macOS); Credential injection via proxy (keys never enter the sandbox); Atomic rollback with Merkle tree integrity; Sigstore-based attestation of instruction files; L7 API endpoint filtering; Detach/reattach multiplexing; Rust library with Python/TS/Go bindings
- **Requirements:** macOS, Linux, or WSL2; brew install nono or single binary
- **Limitations:** Early alpha — not yet audited

_Notes: Unique combination of properties no other tool offers: credential proxy (API keys never enter the sandbox), attestation, and atomic rollback. Easy setup (brew install, then nono run -- claude). Very active development._

<a id="ref-nvidia-openshell"></a>
### NVIDIA OpenShell

**Maintainer:** NVIDIA · **License:** Apache-2.0 · [Home](https://github.com/NVIDIA/OpenShell)

Secure runtime for autonomous AI agents with kernel-level Landlock + seccomp enforcement and declarative YAML/OPA policies.

- **Isolation:** landlock, seccomp
- **Capabilities:** Landlock + seccomp kernel enforcement; Declarative YAML policies; OPA/Rego policy support; Static + dynamic policies; Filesystem/network/process isolation; Containerized agent support
- **Requirements:** Linux; Early preview
- **Limitations:** Early preview; Linux only; No macOS support

_Notes: NVIDIA backing gives visibility. OPA/Rego policy support targets enterprise governance workflows. Announced at GTC 2026._

<a id="ref-opensandbox"></a>
### OpenSandbox

**Maintainer:** Alibaba · **License:** Apache-2.0 · [Home](https://github.com/opensandbox-group/OpenSandbox)

Universal sandbox for AI apps with multi-language SDKs, Docker + K8s runtimes, covering coding agents, GUI agents, evaluation, and RL training.

- **Isolation:** container
- **Capabilities:** Multi-language SDKs (Python/Java/JS/C#/Go planned); Unified API; Dual runtime (Docker for dev, K8s for prod); Evaluation and RL training support
- **Requirements:** Docker or Kubernetes; Self-hosted
- **Limitations:** Very new (created December 2025)

_Notes: Broadest scope of any sandbox — covers evaluation and RL training environments, not just agent sandboxing._

<a id="ref-pixels"></a>
### pixels

**Maintainer:** deevus (Simon Hartcher) · **License:** MIT · [Home](https://github.com/deevus/pixels)

Disposable Incus container sandboxes for AI coding agents with ZFS-backed snapshot/clone fan-out, nftables egress allowlists, and a built-in MCP server exposing sandbox lifecycle as MCP tools.

- **Isolation:** container
- **Capabilities:** Incus (LXD-derived) system containers — kernel namespaces and cgroups; ZFS/btrfs-backed snapshots with checkpoint and clone-from-checkpoint workflow; nftables-based egress allowlist (curated AI API list); Restricted sudoers inside container; Built-in MCP server for sandbox lifecycle and file CRUD as MCP tools; Pluggable backends (local Incus, TrueNAS SCALE-managed Incus); Preloaded coding agents (Claude Code, Codex, OpenCode)
- **Requirements:** Linux with Incus; Optionally TrueNAS SCALE for remote backend
- **Limitations:** Egress is best-effort — root with cap_net_admin can bypass nftables rules; MCP server path is alpha with weaker isolation than pixels create; MCP daemon relies on loopback binding for auth; Solo maintainer

_Notes: Second Incus-based entry alongside code-on-incus, but distinct differentiators: ZFS snapshot fan-out makes spinning up N task containers from a "ready" base a first-class primitive, and the built-in MCP server fits the "MCP server sandboxing" specialized use case called out in the raised-bar criteria. Has a SECURITY.md with documented threat model._

<a id="ref-sand"></a>
### sand

**Maintainer:** banksean · **License:** Apache-2.0 · [Home](https://github.com/banksean/sand)

macOS CLI that spawns disposable Apple Containerization VMs with APFS copy-on-write workspace clones for running coding agents.

- **Isolation:** microvm
- **Capabilities:** Apple Containerization (Kata-based microVMs); APFS clonefile copy-on-write workspace clones; SSH agent forwarding; DNS; eBPF egress filtering with --allowed-domains-file; One-command launch of Claude Code or opencode
- **Requirements:** Apple Silicon; macOS 15+; Homebrew tap
- **Limitations:** macOS only (Apple Silicon); Solo maintainer

_Notes: Apple Containerization gives hardware-isolated micro-VMs (Kata-based) on Apple Silicon. APFS clonefile makes workspace clones instant without copying files. eBPF egress filtering is a notable hardening choice for a solo project._

<a id="ref-sandcastle"></a>
### sandcastle

**Maintainer:** Matt Pocock · **License:** MIT · [Home](https://github.com/mattpocock/sandcastle)

TypeScript library for orchestrating coding agents inside Docker containers with git-aware branch strategies and automatic commit merging.

- **Isolation:** container
- **Capabilities:** Docker container isolation (self-managed, not delegated); Git-aware branch strategy orchestration; Automatic commit merging from agent branches; TypeScript API (sandcastle.run()); npm package
- **Requirements:** Docker; Node.js / TypeScript
- **Limitations:** Orchestration-focused (sandboxing is the mechanism, not the product); Container isolation only (shared kernel)

_Notes: Uses Docker containers it creates directly — not delegating to E2B or Daytona. The git branch strategy (agents work on branches, commits merge back) is the differentiator. Useful if you want multi-agent orchestration with isolation included._

<a id="ref-scode"></a>
### scode

**Maintainer:** Laurent Bindschaedler · **License:** OSS · [Home](https://binds.ch/blog/scode-sandbox-for-ai-coding-tools/)

OS-level sandbox wrapper for any AI coding harness with filesystem and network restrictions.

- **Isolation:** process
- **Capabilities:** OS-level sandboxing; Works with any AI coding tool; Filesystem and network restrictions
- **Requirements:** macOS or Linux
- **Limitations:** Smaller community project

_Notes: Early entry in the space (Sept 2025), motivated by Claude Code's initial lack of built-in sandboxing._

<a id="ref-sevorix-lite"></a>
### sevorix-lite

**Maintainer:** Sevorix · **License:** AGPL-3.0 · [Home](https://github.com/sevorix/sevorix-lite)

Rust-native runtime containment engine combining eBPF syscall interception, mount namespace shell override, HTTP proxy, and a human-in-the-loop policy dashboard.

- **Isolation:** seccomp, user-namespace
- **Capabilities:** eBPF syscall interception (Linux); Mount-namespace bind-mount of sevsh over /bin/bash; HTTP proxy for network filtering; libseccomp integration; Central policy engine with web dashboard; Green/Red/Yellow lane model with human-in-the-loop intervention; Claude Code vault integration; Claims <20ms enforcement latency
- **Requirements:** Linux or WSL (full enforcement); macOS (proxy + shell interception only, no eBPF/seccomp)
- **Limitations:** macOS support is reduced (no eBPF/seccomp); "Lite" edition of a commercial product (Sevorix); AGPL means modifications must be shared

_Notes: Multi-layered runtime containment rather than VM/container isolation. The "Yellow Lane" human-in-the-loop model with countdown timer is unusual — the agent pauses pending human approval via dashboard. Claude Code support is built in, not bolted on._

<a id="ref-skilllite"></a>
### skilllite

**Maintainer:** EXboys · **License:** MIT · [Home](https://github.com/EXboys/skilllite)

Rust single-binary agent engine with a built-in OS-native sandbox using macOS Seatbelt and Linux bubblewrap/seccomp for skill execution isolation.

- **Isolation:** seatbelt, user-namespace, seccomp
- **Capabilities:** OS-native sandbox (Seatbelt on macOS, bubblewrap + seccomp on Linux); Filesystem, network, and IPC lockdown; Process-exec whitelisting; Resource limits via rlimits; Three-layer defense (install-time scan, pre-exec auth, runtime sandbox); Zero-dependency single binary; Sandbox component usable independently of the agent engine
- **Requirements:** macOS or Linux
- **Limitations:** Early project; Smaller community

_Notes: The skilllite-sandbox component is independently usable — you don't have to use the agent engine to get the sandbox. Three-layer defense model (install scan + pre-exec auth + runtime sandbox) is more depth than most standalone tools offer._

<a id="ref-warren"></a>
### warren

**Maintainer:** jayminwest · **License:** MIT · [Home](https://github.com/jayminwest/warren)

Self-hostable control plane and UI for ephemeral coding agents; each run executes in a native bubblewrap sandbox, validates, pushes a branch, and spins down, with live event streaming, mid-run steering, and human sign-off / PR-merge-gated dispatch.

- **Isolation:** user-namespace
- **Capabilities:** Native bubblewrap-isolated workspace per run (host unreachable); Control plane reaches the sandbox runtime over a unix socket with a bearer token; Live NDJSON event streaming; Mid-run steering (POST /steer); Human sign-off gates that arm dispatch; Serial plan-run dispatch gated on prior-PR merges; Built-in claude-code agent plus a steerable alternative harness; Single container/volume/HTTP API/UI; optional Postgres backend
- **Requirements:** Docker (single container), or Fly.io / a cluster; A GitHub repo URL and a prompt
- **Limitations:** Early (v0.6.2); org-readiness features (SSO, remote workers, MCP, audit, budgets) on the roadmap; Process-level isolation (bubblewrap), shared kernel

_Notes: Unlike control planes that delegate isolation to a cloud backend, warren ships its own bubblewrap sandbox — the host is unreachable and the control plane talks to the runtime over a unix socket. The differentiator is the governance layer (mid-run steering, sign-off gates, PR-merge-gated serial dispatch) on native isolation. 33 scenario-based acceptance tests; runs on Fly.io._

## Kubernetes-Native

<a id="ref-agent-sandbox-kubernetes-sigs"></a>
### Agent Sandbox (kubernetes-sigs)

**Maintainer:** Kubernetes SIG · **License:** Apache-2.0 · [Home](https://github.com/kubernetes-sigs/agent-sandbox)

Kubernetes CRD and controller for isolated agent workloads with gVisor or Kata runtime and warm pod pools.

- **Isolation:** gvisor, kata
- **Capabilities:** Declarative CRD; gVisor + Kata support; Warm pod pool for <1s cold start; Persistent storage; Stable pod identity
- **Requirements:** Kubernetes cluster; gVisor or Kata runtime
- **Limitations:** Kubernetes required; Still maturing; No standalone mode

_Notes: Official Kubernetes SIG project (launched KubeCon Atlanta Nov 2025). Likely to become the standard for K8s agent sandboxing._

<a id="ref-gke-agent-sandbox"></a>
### GKE Agent Sandbox

**Maintainer:** Google Cloud · **License:** Closed source · [Home](https://cloud.google.com)

Managed Kubernetes service for AI code isolation on GKE using gVisor and kubernetes-sigs/agent-sandbox.

- **Isolation:** gvisor, kata
- **Capabilities:** Managed gVisor/Kata runtime; GKE integration; Warm pools; Persistent storage; Cloud IAM
- **Requirements:** Google Cloud account; GKE cluster
- **Limitations:** GKE-only; Vendor lock-in

_Notes: Managed wrapper around the open-source agent-sandbox project. If you're already on GKE, this is the path of least resistance._

<a id="ref-mitos"></a>
### mitos

**Maintainer:** mitos-run · **License:** Apache-2.0 · [Home](https://mitos.run) · [Repo](https://github.com/mitos-run/mitos)

Kubernetes-native runtime that gives each agent a Firecracker microVM and live copy-on-write forks a running VM into N siblings in tens of milliseconds, with durable versioned workspaces and declarative CRDs.

- **Isolation:** microvm, kvm
- **Capabilities:** Firecracker microVM per agent (KVM hardware isolation); Live copy-on-write fork of a running VM into N siblings (tens of ms); Restore from memory snapshots in milliseconds; Durable, versioned workspaces; Declarative CRDs with a Kubernetes operator; KVM device-plugin for scheduling microVMs; Go SDK
- **Requirements:** Kubernetes; Nodes with KVM (bare-metal or nested virtualization); Self-hosted
- **Limitations:** Very new (created May 2026); prerelease tags; Alpha — features split across "husk" and "engine" paths mid-migration; Linux/KVM only

_Notes: Distinct from raw Firecracker (already listed): a live copy-on-write fork of a warm, running microVM plus a Kubernetes operator, CRDs, and a KVM device-plugin. Fast memory-snapshot restore suits parallel agent exploration and RL-style environment resets._

<a id="ref-openkruise-agents"></a>
### openkruise/agents

**Maintainer:** OpenKruise (Alibaba / CNCF) · **License:** Apache-2.0 · [Home](https://github.com/openkruise/agents)

Kubernetes operator for agent sandbox lifecycle management with resource pooling, hibernation, checkpoint/restore, and E2B API compatibility.

- **Isolation:** container
- **Capabilities:** Sandbox pod lifecycle management; Resource pooling; Sandbox hibernation and checkpoint (memory + RW layer + GPU memory); E2B API compatibility on self-hosted K8s; Configurable runtime (container, gVisor, Kata)
- **Requirements:** Kubernetes cluster
- **Limitations:** Early project; Kubernetes required

_Notes: CNCF-affiliated via OpenKruise (Alibaba). The E2B API compatibility is notable — lets you use existing E2B SDK integrations against self-hosted K8s instead of E2B's cloud. Sandbox hibernation with GPU memory checkpoint is unusual._

<a id="ref-sandbox0"></a>
### sandbox0

**Maintainer:** sandbox0-ai · **License:** Apache-2.0 · [Home](https://github.com/sandbox0-ai/sandbox0)

Kubernetes-native agent sandbox platform with warm pod pools, JuiceFS persistent storage, network policy enforcement, and in-pod process manager.

- **Isolation:** container, gvisor
- **Capabilities:** Warm pod pools; JuiceFS persistent storage; Configurable runtimeClass (gVisor/Kata); L4/L7 network enforcement via dedicated netd daemon; Egress auth proxy (credential injection outside sandbox); procd in-pod process manager (PID 1) with REPL session management
- **Requirements:** Kubernetes cluster; Self-hosted
- **Limitations:** Early project; Small community

_Notes: The procd process manager inside pods provides REPL session management — unusual for a K8s sandbox. Egress credential injection keeps secrets outside the sandbox boundary, similar to nono's credential proxy model but at the K8s level._

<a id="ref-treadstone"></a>
### treadstone

**Maintainer:** earayu · **License:** Apache-2.0 · [Home](https://github.com/earayu/treadstone)

Self-hostable Kubernetes sandbox control plane that provisions gVisor-isolated pods from templates, with CLI, Python SDK, REST API, and built-in browser handoff for human intervention.

- **Isolation:** gvisor
- **Capabilities:** Kubernetes CRD-based provisioning (built on kubernetes-sigs/agent-sandbox); gVisor isolation; Warm pod pools; CLI + Python SDK + REST API; Browser handoff — short-lived links to hand a running session to a human; MCP-over-data-plane routing; Data plane proxy for outbound traffic
- **Requirements:** Kubernetes cluster (self-hosted); or managed service at treadstone-ai.dev
- **Limitations:** Solo maintainer; Maturity unclear; Full SDK/CLI surface suggests active development

_Notes: Built on kubernetes-sigs/agent-sandbox as the underlying CRD. Browser handoff is an unusual feature — enables smooth transitions from autonomous agent execution to human intervention. Offered both as open source and as a hosted service._

## Development Environments

<a id="ref-coder"></a>
### Coder

**Maintainer:** Coder · **License:** AGPL-3.0 · [Home](https://github.com/coder/coder)

Self-hosted remote development platform with container and VM workspaces, RBAC, and audit logging.

- **Isolation:** container
- **Capabilities:** Self-hosted; Container and VM workspaces; Templates; RBAC; Audit logging
- **Requirements:** Self-hosted on Kubernetes or Docker
- **Limitations:** No agent-specific features; No MCP integration

_Notes: Not agent-specific, but good for teams wanting self-hosted isolation without cloud dependency. AGPL license means modifications must be shared._

<a id="ref-devpod"></a>
### DevPod

**Maintainer:** Loft Labs · **License:** OSS · [Home](https://github.com/loft-sh/devpod)

Client-only tool for reproducible, provider-agnostic dev environments using devcontainer.json.

- **Isolation:** container
- **Capabilities:** Provider-agnostic (Docker/SSH/K8s/cloud); devcontainer.json support; Client-only (no server); Open source
- **Requirements:** Docker or cloud provider
- **Limitations:** No agent-specific features; No MCP integration; No managed service

_Notes: Not agent-specific. Good open-source alternative to Codespaces for local-first workflows where you want reproducible isolated environments._

<a id="ref-github-codespaces"></a>
### GitHub Codespaces

**Maintainer:** GitHub / Microsoft · **License:** Closed source · [Home](https://github.com/features/codespaces)

Cloud-hosted dev environments usable for isolating agent execution in a full Linux VM.

- **Isolation:** container
- **Capabilities:** Full Linux VM; devcontainer.json support; Pre-built images; GitHub integration; Port forwarding
- **Requirements:** GitHub account; Usage-based pricing (free tier available)
- **Limitations:** Not agent-specific; Higher startup latency; Dev tool, not a sandbox service

_Notes: Not purpose-built for agents, but accessible to anyone familiar with GitHub. A "good enough" isolation option for personal agent use without learning new tools._

<a id="ref-klangk"></a>
### klangk

**Maintainer:** mcdonc · **License:** MIT · [Home](https://mcdonc.github.io/klangk/) · [Repo](https://github.com/mcdonc/klangk)

Self-hosted multi-user collaborative coding platform that runs each user's agent workspace in its own rootless-podman container, with real-time collaboration (presence, terminal-sharing, ACLs) and bundled agents.

- **Isolation:** container, seccomp
- **Capabilities:** Rootless podman, one container per workspace (filesystem, process, network); pasta networking and seccomp profiles; Per-workspace JWT and per-user bind-mounted homes; Multi-user real-time collaboration (presence, terminal-sharing, ACLs); Bundled agents (OpenClaw, Hermes, Pi); Flutter web UI with a FastAPI backend
- **Requirements:** Podman (rootless); Linux; Self-hosted
- **Limitations:** Commodity container isolation (rootless podman); no novel security primitive; Broad platform scope beyond a sandbox primitive; Early-stage (14 stars, created May 2026)

_Notes: The only multi-user collaborative sandbox platform in this list — the isolation axis is the per-user workspace (rootless podman), not multiple parallel agents (see LINCE and warren for that). The differentiator is the team-collaboration use case (presence, terminal-sharing, ACLs) on real per-workspace container isolation, not the isolation mechanism itself._

<a id="ref-koyeb"></a>
### Koyeb

**Maintainer:** Koyeb · **License:** Closed source · [Home](https://www.koyeb.com)

Serverless platform with container-based sandbox capabilities and auto-scaling.

- **Isolation:** container
- **Capabilities:** Container isolation; Auto-scaling; CI/CD integration
- **Requirements:** Cloud-hosted; Usage-based pricing
- **Limitations:** Not agent-specific; General-purpose serverless platform

_Notes: General-purpose serverless platform, not purpose-built for agents, but usable for agent isolation out of the box with standard container workflows._

<a id="ref-ona-formerly-gitpod"></a>
### Ona (formerly Gitpod)

**Maintainer:** Ona · **License:** Closed source · [Home](https://ona.com)

Pivoted from CDE to "mission control for AI agents" with sandboxed dev environments, AI agents, and guardrails.

- **Isolation:** container
- **Capabilities:** API-first environments; devcontainer.json support; OS-level isolation; Ona Agents; Ona Guardrails
- **Requirements:** Cloud-hosted; Enterprise tiers
- **Limitations:** Rapid pivot — product still evolving; Less sandbox API focus than E2B/Daytona

_Notes: Major pivot from Gitpod (rebranded Sept 2025). Demonstrated Claude Code sandbox escape (March 2026). Not agent-specific but increasingly agent-oriented._

<a id="ref-sandcat"></a>
### sandcat

**Maintainer:** VirtusLab · **License:** Apache-2.0 · [Home](https://github.com/VirtusLab/sandcat)

Docker/devcontainer sandbox that routes all container traffic through a transparent WireGuard-to-mitmproxy for allow/deny egress filtering and injects secrets at the proxy so the container never sees real credential values.

- **Isolation:** container
- **Capabilities:** Devcontainer or standalone Docker sandbox; Transparent WireGuard tunnel routing all HTTP/S, DNS, and TCP/UDP to mitmproxy; Allow/deny list-based network egress engine; Proxy-level secret substitution (real credentials never enter the container); Runs agents in bypass / auto-approve mode within the boundary; VS Code / IDE integration; CLI wrapper around docker-compose
- **Requirements:** Docker; Linux or macOS
- **Limitations:** Container isolation only (shared kernel); Templates need per-project tuning for the development stack

_Notes: Transparent full-traffic capture via WireGuard (not per-tool HTTP_PROXY) combined with proxy-level secret substitution brings the credential-proxy pattern — previously VM-tier only in this list (nono) — down to the container tier. Part of VirtusLab's Visdom delivery infrastructure._

## Abstraction Layers

<a id="ref-agentbox-sdk"></a>
### agentbox-sdk

**Maintainer:** TwillAI · **License:** MIT · [Home](https://github.com/TwillAI/agentbox-sdk)

TypeScript SDK that runs coding agents (Claude Code, opencode, codex) as server processes inside swappable sandbox backends (E2B, Modal, Daytona, Vercel, local Docker), each agent reached over its upstream-native protocol.

- **Isolation:** microvm, container
- **Capabilities:** Five sandbox backends (E2B, Modal, Daytona, Vercel, local-docker); Native-protocol agent transports — Claude Code custom HTTP daemon, opencode SSE with Last-Event-ID resume, codex JSON-RPC WebSocket; Mid-run message injection into a running agent stream; Interactive approval flows preserved across backends; Sub-agent orchestration
- **Requirements:** Node.js / TypeScript; Account with chosen backend provider (E2B/Modal/Daytona/Vercel) or local Docker
- **Limitations:** No LICENSE file in repo as of 2026-05-12 (package.json declares MIT); Isolation strength entirely dictated by chosen backend; Pre-release — no formal versions cut yet

_Notes: Differentiator vs other abstraction-tier entries is heterogeneous-protocol agent transport: each upstream agent is reached via its native protocol rather than CLI-wrapped, so mid-run interactivity, approval flows, and sub-agent orchestration survive being inside a sandbox. ComputeSDK is closed-source and sandbox-only; LangChain Sandboxes is framework-bound; NanoClaw is Claude-only; AgentScope Runtime is Python-only and ships its own agent framework._

<a id="ref-agentscope-runtime"></a>
### AgentScope Runtime

**Maintainer:** agentscope-ai (Alibaba) · **License:** Apache-2.0 · [Home](https://github.com/agentscope-ai/agentscope-runtime)

Agent runtime framework with real sandbox backends (Docker, gVisor, BoxLite, K8s, serverless) and pre-built sandbox images for GUI, browser, and mobile.

- **Isolation:** container, gvisor
- **Capabilities:** Docker container sandboxing (default); Optional gVisor hardening; BoxLite sandbox backend; K8s and serverless (Alibaba Cloud) backends; Pre-built sandbox images (base, GUI/VNC, browser, filesystem, mobile/Android); Multi-framework compatibility (AgentScope, LangGraph, Agno, AutoGen); Async sandbox support
- **Requirements:** Docker (local); K8s or Alibaba Cloud (production); Python
- **Limitations:** Primarily an agent runtime framework — sandboxing is one feature among many; Alibaba Cloud for serverless backend

_Notes: Real sandbox depth despite being a runtime framework — pre-built images covering GUI (VNC), browser, and mobile (Android emulator) environments go well beyond typical container sandboxes. Multiple sandbox backends (Docker, gVisor, BoxLite, K8s) abstracted behind a single API._

<a id="ref-computesdk"></a>
### ComputeSDK

**Maintainer:** ComputeSDK · **License:** Closed source · [Home](https://www.computesdk.com)

Unified API across multiple sandbox providers (E2B, Daytona, Modal, Blaxel, etc.).

- **Isolation:** microvm, container
- **Capabilities:** Provider-agnostic API; Single SDK for multiple backends
- **Requirements:** Account with underlying provider
- **Limitations:** Abstraction adds complexity; Provider-dependent isolation

_Notes: Useful if you want to avoid vendor lock-in. Isolation strength depends entirely on the chosen backend provider._

<a id="ref-langchain-sandboxes"></a>
### LangChain Sandboxes

**Maintainer:** LangChain · **License:** OSS · [Home](https://docs.langchain.com/oss/python/deepagents/sandboxes)

Sandbox integration layer within the LangChain agent framework.

- **Isolation:** container
- **Capabilities:** Framework integration; Provider abstraction; Agent workflow orchestration
- **Requirements:** LangChain framework; Python
- **Limitations:** Framework-dependent; Not standalone

_Notes: Only relevant if already using LangChain. The sandbox capabilities come from the underlying provider, not LangChain itself._

<a id="ref-nanoclaw"></a>
### NanoClaw

**Maintainer:** Lazer and Gavriel Cohen · **License:** MIT · [Home](https://github.com/qwibitai/nanoclaw)

Lightweight containerized agent orchestration wrapping Claude Code with messaging platform integrations.

- **Isolation:** container
- **Capabilities:** Container isolation (Docker/Docker Sandboxes/Apple Container); WhatsApp/Telegram/Slack/Discord/Gmail integration; Memory management; Scheduled jobs
- **Requirements:** Docker or Apple Container
- **Limitations:** Tied to Claude/Anthropic SDK; Container-level isolation unless using Docker Sandboxes

_Notes: More of an agent orchestration framework with sandbox support than a sandbox itself. High adoption. Sandbox capability comes from Docker or Docker Sandboxes underneath._

## Building Blocks

### VM & Container Runtimes

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

### OS-Level Sandboxing

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

### WebAssembly Runtimes

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

