# Standalone / Self-Hosted Tools

[Back to main guide](../README.md)

<a id="ref-agent-safehouse"></a>
## Agent Safehouse

**Maintainer:** eugene1g · **License:** OSS · [Home](https://github.com/eugene1g/agent-safehouse)

macOS sandbox-exec profile system with deny-first policy, composable profiles, and pre-built agent configurations.

- **Isolation:** seatbelt
- **Capabilities:** macOS Seatbelt profile generation; Deny-first policy; Composable profile system; Pre-built profiles for major coding agents; Policy builder web tool; Fine-grained HOME access control; Symlink-aware path resolution
- **Requirements:** macOS only; brew install eugene1g/safehouse/agent-safehouse
- **Limitations:** macOS only (permanently — sandbox-exec is Apple-specific); sandbox-exec deprecation risk

_Notes: More mature than it appears — has CI tests, docs site, and thoughtful profile composition. The most polished macOS-specific sandboxing option._

<a id="ref-agent-infra-sandbox"></a>
## agent-infra/sandbox

**Maintainer:** agent-infra (community) · **License:** OSS · [Home](https://github.com/agent-infra/sandbox)

All-in-one sandbox combining Browser, Shell, File management, MCP, and VSCode Server in a single Docker container.

- **Isolation:** container
- **Capabilities:** Browser automation; Shell access; File management; MCP integration; VSCode Server
- **Requirements:** Docker
- **Limitations:** Container isolation only (shared kernel); Monolithic design

_Notes: Kitchen-sink approach — good for prototyping and development, less suitable for security-critical production use._

<a id="ref-agentsh"></a>
## agentsh

**Maintainer:** canyonroad · **License:** Apache-2.0 · [Home](https://github.com/canyonroad/agentsh)

Policy-enforced execution gateway that intercepts file, network, process, and signal syscalls for agent commands with allow/deny/approve/redirect decisions and structured audit.

- **Isolation:** process, landlock, seatbelt
- **Capabilities:** Syscall interception (file, network, process, signal); Subprocess tree coverage; Allow/deny/approve/redirect policy decisions; Structured audit events; Pairs with containers; Cross-platform (Linux LSM/FUSE, macOS ESF+NE, Windows minifilter); Linux is production-ready; macOS alpha; Windows pending driver signing
- **Requirements:** Linux (production), macOS (alpha), or Windows (pending); Homebrew, .deb, .rpm, or .apk install
- **Limitations:** macOS support is alpha; Windows support pending driver signing

_Notes: Real runtime enforcement, not just wrapping. The "redirect" policy decision is unusual — can transparently steer agent network calls or out-of-workspace writes to scratch dirs without the agent knowing it was redirected._

<a id="ref-ai-sandbox-wrapper"></a>
## ai-sandbox-wrapper

**Maintainer:** kokorolx · **License:** OSS · [Home](https://github.com/nano-step/ai-sandbox-wrapper)

npm CLI that wraps Docker for coding agents (opencode, amp, droid) with workspace whitelisting, capability dropping, and Git fetch-only mode.

- **Isolation:** container
- **Capabilities:** Docker container isolation; Workspace whitelisting (filesystem boundary); Non-root execution; CAP_DROP=ALL (drops all Linux capabilities); Explicit API key passing; Git fetch-only mode (egress restriction); Targets opencode, amp, droid coding agents
- **Requirements:** Docker; npm install -g @kokorolx/ai-sandbox-wrapper
- **Limitations:** No LICENSE file in repo (legal status unclear); Solo maintainer; Container isolation only (shared kernel)

_Notes: Opinionated hardening over default Docker — capability dropping and Git fetch-only mode are substantive choices most Docker wrappers don't make. No license means the code is technically all-rights-reserved by default; consider asking the author to add one before relying on it._

<a id="ref-aide"></a>
## aide

**Maintainer:** jskswamy · **License:** MIT · [Home](https://github.com/jskswamy/aide)

Unified agent launcher with capability-based permission model and OS-native sandbox enforcement on macOS.

- **Isolation:** seatbelt
- **Capabilities:** Capability-based permission model (19 built-in capabilities); Composable grants with never-allow hard denials; macOS Seatbelt sandbox enforcement; Per-project context resolution (agent, credentials, capabilities); Supports multiple agents from a single launcher
- **Requirements:** macOS (sandbox enforcement); Go
- **Limitations:** Linux sandbox not yet implemented (Landlock + seccomp planned); macOS-only sandbox enforcement today; Early project (v0.1.0)

_Notes: The capability model is the differentiator — 19 built-in capabilities (docker, k8s, aws, etc.) with composable grants and never-allow hard denials. More opinionated than fence or Agent Safehouse about what agents should be allowed to do. Linux sandbox is planned but not yet implemented._

<a id="ref-alcless"></a>
## alcless

**Maintainer:** AkihiroSuda · **License:** Apache-2.0 · [Home](https://github.com/AkihiroSuda/alcless)

macOS sandbox using separate local user accounts for process/filesystem isolation with rsync workspace sync and user-confirmed sync-back.

- **Isolation:** process
- **Capabilities:** Separate macOS user account isolation; rsync-based workspace isolation; User-confirmed file sync-back; Mach bootstrap subset isolation via pam_launchd; No VM or container overhead
- **Requirements:** macOS only
- **Limitations:** macOS only (by design — Linux/FreeBSD have containers); Requires sudo for user switching; Early project

_Notes: From AkihiroSuda (maintainer of Lima, nerdctl). Deliberately positioned as the lightweight complement to Lima (VM-based). Zero VM overhead — just Unix user separation. The rsync + confirm workflow means changes don't land on the host without approval._

<a id="ref-anthropic-sandbox-runtime-srt"></a>
## Anthropic sandbox-runtime (srt)

**Maintainer:** Anthropic · **License:** OSS · [Home](https://github.com/anthropic-experimental/sandbox-runtime)

Lightweight sandboxing for arbitrary processes using bubblewrap (Linux) and Seatbelt (macOS), no container required.

- **Isolation:** user-namespace, seatbelt
- **Capabilities:** Filesystem isolation (directory-level); Network isolation (proxy-based domain filtering with interactive approval); Works for any process, agent, or MCP server
- **Requirements:** macOS or Linux; No root required on Linux
- **Limitations:** Experimental/research preview; Not production-hardened; macOS sandbox-exec deprecation risk

_Notes: Designed to sandbox any process, not just Claude Code. Interactive network approval mode is useful for discovering what network access a tool actually needs._

<a id="ref-brood-box"></a>
## brood-box

**Maintainer:** Stacklok · **License:** Apache-2.0 · [Home](https://github.com/stacklok/brood-box)

CLI that runs coding agents inside hardware-isolated microVMs with COW workspace snapshots and interactive per-file diff review before changes land.

- **Isolation:** kvm, microvm
- **Capabilities:** Hardware VM isolation (libkrun/KVM on Linux, Hypervisor.framework on macOS); COW workspace snapshots; Interactive per-file diff review (VM stopped before review, TOCTOU-resistant); DNS-aware egress firewall; Ephemeral SSH keys; Non-overridable secret exclusions; Permission stripping on flush
- **Requirements:** Linux (KVM) or macOS (Apple Silicon, Hypervisor.framework)
- **Limitations:** Experimental

_Notes: From Stacklok (founded by Luke Hinds of Sigstore). Hardware VM isolation like cleanroom, but adds TOCTOU-resistant diff review — the VM is stopped before the user reviews changes, preventing the agent from modifying files during review. DNS egress firewall and non-overridable secret exclusions are strong default posture._

<a id="ref-cleanroom"></a>
## cleanroom

**Maintainer:** Buildkite · **License:** OSS · [Home](https://github.com/buildkite/cleanroom)

Self-hosted microVM sandbox using Firecracker (Linux) or Apple Virtualization.framework (macOS) with deny-by-default network and host-side credential proxy.

- **Isolation:** microvm, kvm
- **Capabilities:** Firecracker microVMs (Linux); Apple Virtualization.framework (macOS); Deny-by-default egress with policy-controlled allowlists; Host-side credential proxy (credentials never enter sandbox); Repo-scoped cleanroom.yaml network policy; Docker-inside-sandbox support
- **Requirements:** Linux (KVM) or macOS
- **Limitations:** Early project; No LICENSE file in repo

_Notes: From Buildkite (established CI company). Strongest isolation in recent discovery batches — hardware VM boundary, not containers or namespaces. Credential proxy model is similar to nono (keys never enter the sandbox). cleanroom.yaml per-repo policy is a clean declarative approach._

<a id="ref-code-on-incus"></a>
## code-on-incus

**Maintainer:** mensfeld · **License:** MIT · [Home](https://github.com/mensfeld/code-on-incus)

Hardened Incus container sandbox with real-time nftables threat detection (reverse shells, C2, DNS tunneling, exfiltration) and automated container pause/kill response.

- **Isolation:** container, seccomp
- **Capabilities:** Incus unprivileged system containers (seccomp, AppArmor, UID remapping); Firewalld network isolation (restricted/allowlist/open modes); Real-time nftables threat detection daemon; Automated container pause/kill on threat detection; Protected paths via read-only mounts + chattr +i; Supply-chain hardening (read-only .git/hooks, .husky, .vscode); Credential isolation (host credentials not mounted); Health-check command verifying seccomp/AppArmor/privilege posture
- **Requirements:** Linux (native); macOS via Lima/Colima VM
- **Limitations:** Container isolation (shared kernel); Linux-native (macOS requires VM layer)

_Notes: Goes beyond isolation into active defense — the monitoring daemon uses kernel-level nftables packet inspection to detect reverse shells, C2 callbacks, DNS tunneling, and data exfiltration patterns, then auto-pauses or kills the container. Supply-chain hardening (read-only git hooks) is a detail most sandboxes miss._

<a id="ref-docker-sandboxes"></a>
## Docker Sandboxes

**Maintainer:** Docker · **License:** Closed source · [Home](https://docs.docker.com/ai/sandboxes/)

MicroVM sandboxes for AI coding agents, each with its own Docker daemon, filesystem, and network.

- **Isolation:** microvm
- **Capabilities:** MicroVM isolation (not regular containers); Dedicated Docker daemon per sandbox; Filesystem and network isolation; Supports Claude Code, Codex, Copilot, Gemini, Kiro
- **Requirements:** Docker Engine 29.1.5+ (Docker Desktop 4.58+); macOS or Linux
- **Limitations:** Experimental; MicroVM overhead

_Notes: Very new (March 2026). Multi-agent support is notable — works with most major coding agents out of the box._

<a id="ref-envpod-ce"></a>
## envpod-ce

**Maintainer:** markamo · **License:** BSL-1.1 · [Home](https://github.com/markamo/envpod-ce)

Linux governance sandbox using OverlayFS COW, namespaces, cgroups v2, and seccomp-BPF with a diff/commit/rollback workflow for agent changes to host files.

- **Isolation:** user-namespace, seccomp
- **Capabilities:** OverlayFS copy-on-write (agents work on real files, changes staged); Linux namespaces (PID, net, mount, UTS, user); cgroups v2 resource limits; seccomp-BPF syscall filtering; Per-pod DNS with allowlisting; Encrypted credential vault; Diff/commit/rollback workflow for host changes; Jailbreak test suite included
- **Requirements:** Linux only; Single-binary Rust install
- **Limitations:** Linux only; BSL-1.1 license (not OSI-approved open source); Very early (v0.1.15, 9 stars)

_Notes: The diff/commit/rollback workflow is unique — agents work on real host files via an OverlayFS overlay, and changes are staged for human review before committing to the host. Most sandboxes either fully isolate (agent can't touch host files) or don't isolate at all. This is a middle ground that enables real work with reversibility. BSL-1.1 license restricts production use without a commercial license._

<a id="ref-fence"></a>
## fence

**Maintainer:** Tusk · **License:** Apache-2.0 · [Home](https://github.com/Use-Tusk/fence)

Container-free CLI sandbox using OS-native primitives for network domain allowlisting, filesystem access control, and command deny-lists.

- **Isolation:** seatbelt, user-namespace
- **Capabilities:** macOS sandbox-exec (Seatbelt); Linux bubblewrap + socat for network bridging; Network domain allowlisting; Filesystem access control; Command deny-lists; Built-in templates for Claude Code, Codex, Amp, Gemini CLI, Copilot; Go library for programmatic use
- **Requirements:** macOS or Linux; Homebrew, Nix, or Go install
- **Limitations:** macOS sandbox-exec deprecation risk; Process-level isolation (shared kernel)

_Notes: Lightest-weight option for wrapping agent processes with real isolation — no container runtime needed. Inspired by Anthropic's srt. Built-in agent templates mean zero config for common agents. Well-documented security model and architecture._

<a id="ref-hazmat"></a>
## hazmat

**Maintainer:** dredozubov · **License:** MIT · [Home](https://github.com/dredozubov/hazmat)

macOS triple-layer containment stacking a dedicated user account, per-session Seatbelt kernel sandbox, and pf firewall with DNS blocklists and Kopia snapshots.

- **Isolation:** seatbelt, process
- **Capabilities:** Dedicated macOS agent user (blocks ~/.ssh, ~/.aws, Keychain); Per-session Seatbelt kernel sandbox (default-deny filesystem); pf packet filter scoped to agent user; DNS blocklists (ngrok, pastebin, webhook.site); Supply-chain hardening (npm ignore-scripts by default); Kopia backup snapshots; TLA+ formally verified session lifecycle and policy structure
- **Requirements:** macOS only; Homebrew install
- **Limitations:** macOS only; Seatbelt is undocumented by Apple; HTTPS exfiltration not blocked; /tmp is shared

_Notes: Strongest macOS-specific sandbox — layers everything alcless (user isolation) and Agent Safehouse (Seatbelt) do individually, plus pf firewall and DNS blocklists. TLA+ formal verification of session lifecycle is unusual rigor for a sandbox tool. Honest about limitations (HTTPS exfil, shared /tmp)._

<a id="ref-hole"></a>
## hole

**Maintainer:** lukashornych · **License:** Apache-2.0 · [Home](https://github.com/lukashornych/hole)

CLI that runs AI agents inside ephemeral Docker/Podman containers with proxy-based network domain whitelisting and configurable filesystem exclusions.

- **Isolation:** container
- **Capabilities:** Docker and Podman container isolation; Proxy-based network domain whitelisting (three profiles); --dump-network-access logging; File exclusion via bind-mount overrides; Docker-in-Docker support for agents that need containers; Ephemeral containers (destroyed on exit); Non-root user inside container
- **Requirements:** Docker or Podman; Linux, macOS, or WSL
- **Limitations:** Container isolation only (shared kernel); Solo maintainer; Early project

_Notes: The --dump-network-access flag is useful for discovering what network access an agent actually needs — similar to Anthropic srt's interactive approval mode but post-hoc. Docker-in-Docker support is unusual and needed for agents that themselves use containers._

<a id="ref-jailoc"></a>
## jailoc

**Maintainer:** Seznam · **License:** MIT · [Home](https://github.com/seznam/jailoc)

Per-workspace Docker Compose sandbox for OpenCode agents with iptables egress filtering, dropped capabilities, and a DinD sidecar to avoid host socket mounting.

- **Isolation:** container
- **Capabilities:** Per-workspace Docker Compose sandboxes; iptables egress filtering (blocks RFC 1918, link-local, CGNAT by default); UID 1000, dropped capabilities, no_new_privs; DinD sidecar instead of mounting docker.sock; OpenCode agent integration; Renovate-pinned base image
- **Requirements:** Docker; Linux
- **Limitations:** OpenCode-specific defaults (sandboxing model is general); Container isolation only (shared kernel)

_Notes: Backed by Seznam (Czech search engine). Network isolation via iptables allowlist prevents pivot to internal infra. The DinD sidecar approach avoids the common docker.sock mount escape vector._

<a id="ref-llm-sandbox"></a>
## llm-sandbox

**Maintainer:** vndee · **License:** MIT · [Home](https://github.com/vndee/llm-sandbox)

Lightweight Python library for executing LLM-generated code inside Docker, Podman, or Kubernetes containers with network isolation and resource limits.

- **Isolation:** container
- **Capabilities:** Multi-backend (Docker, Podman, Kubernetes); Network isolation; Resource limits; Security policies; MCP integration; PyPI published
- **Requirements:** Docker, Podman, or Kubernetes; Python
- **Limitations:** Container isolation only (shared kernel); Code interpreter focus (not general agent sandboxing)

_Notes: Multi-backend support is the differentiator — same API across Docker, Podman, and K8s. Good for sandboxing LLM-generated code execution specifically. SonarCloud + codecov CI suggests reasonable code quality standards._

<a id="ref-locki"></a>
## locki

**Maintainer:** JanPokorny · **License:** OSS · [Home](https://github.com/JanPokorny/locki)

CLI that runs coding agents inside Incus containers in a shared Lima VM, with auto-managed git worktrees and a host-side SSH git proxy.

- **Isolation:** kvm, container
- **Capabilities:** VM isolation via Lima/QEMU; Container isolation via Incus; Auto-managed git worktrees; Host-side SSH git proxy with command allowlist; Supports claude, gemini, codex, opencode, shell
- **Requirements:** macOS or Linux; Lima and Incus; pip or uv install
- **Limitations:** No LICENSE file in repo (legal status unclear); Author explicitly disclaims security guarantees; No exfiltration protection; Solo maintainer; Very early

_Notes: One of the few sandboxes that layers VM (Lima/QEMU) plus container (Incus) for coding agents — interesting design worth tracking. Author is candid about "no security guarantees" in the README. No license means the code is technically all-rights-reserved by default; consider asking the author to add one before relying on it._

<a id="ref-microsandbox"></a>
## microsandbox

**Maintainer:** zerocore-ai · **License:** OSS · [Home](https://github.com/zerocore-ai/microsandbox)

Local-first programmable sandboxes using libkrun microVMs, designed for sensitive API keys with no external server.

- **Isolation:** microvm
- **Capabilities:** libkrun microVM isolation; Local-first (no external server); Programmable SDK; Agent Skills for Claude Code, Cursor, Codex, Gemini, Copilot
- **Requirements:** Linux (KVM) or macOS
- **Limitations:** Self-hosted only; Smaller community

_Notes: Local-first is the key differentiator — no credentials leave your machine. Good for privacy-conscious users handling sensitive API keys._

<a id="ref-monty"></a>
## monty

**Maintainer:** Pydantic · **License:** MIT · [Home](https://github.com/pydantic/monty)

Minimal, secure Python interpreter written in Rust providing language-runtime sandboxing for AI-generated code with no host access except via explicit caller-provided functions.

- **Isolation:** process
- **Capabilities:** Custom Python interpreter in Rust; No filesystem, env, or network access by default; Caller-provided functions for explicit host integration; Memory, stack, and time limits; Snapshotting
- **Requirements:** pip install pydantic-monty
- **Limitations:** Experimental — explicitly not ready for production; Python subset only (not full CPython)

_Notes: Different approach from Pyodide — a custom Rust interpreter rather than CPython compiled to Wasm. Will power Pydantic AI's codemode feature. Backed by Pydantic, but explicitly experimental. Categorized in the wasm tier because language-runtime sandboxing fits the same isolation strength characterization (fastest/lightest, limited to specific runtimes), even though it's not actually Wasm._

<a id="ref-nono"></a>
## nono

**Maintainer:** always-further · **License:** OSS · [Home](https://nono.sh) · [Repo](https://github.com/always-further/nono)

Kernel-enforced agent sandbox with credential proxy, atomic rollback, Sigstore attestation, and cryptographic audit chain.

- **Isolation:** landlock, seatbelt
- **Capabilities:** Kernel-level enforcement (Landlock on Linux, Seatbelt on macOS); Credential injection via proxy (keys never enter the sandbox); Atomic rollback with Merkle tree integrity; Sigstore-based attestation of instruction files; L7 API endpoint filtering; Detach/reattach multiplexing; Rust library with Python/TS/Go bindings
- **Requirements:** macOS, Linux, or WSL2; brew install nono or single binary
- **Limitations:** Early alpha — not yet audited

_Notes: Unique combination of properties no other tool offers: credential proxy (API keys never enter the sandbox), attestation, and atomic rollback. Easy setup (brew install, then nono run -- claude). Very active development._

<a id="ref-nvidia-openshell"></a>
## NVIDIA OpenShell

**Maintainer:** NVIDIA · **License:** Apache-2.0 · [Home](https://github.com/NVIDIA/OpenShell)

Secure runtime for autonomous AI agents with kernel-level Landlock + seccomp enforcement and declarative YAML/OPA policies.

- **Isolation:** landlock, seccomp
- **Capabilities:** Landlock + seccomp kernel enforcement; Declarative YAML policies; OPA/Rego policy support; Static + dynamic policies; Filesystem/network/process isolation; Containerized agent support
- **Requirements:** Linux; Early preview
- **Limitations:** Early preview; Linux only; No macOS support

_Notes: NVIDIA backing gives visibility. OPA/Rego policy support targets enterprise governance workflows. Announced at GTC 2026._

<a id="ref-opensandbox"></a>
## OpenSandbox

**Maintainer:** Alibaba · **License:** OSS · [Home](https://github.com/alibaba/OpenSandbox)

Universal sandbox for AI apps with multi-language SDKs, Docker + K8s runtimes, covering coding agents, GUI agents, evaluation, and RL training.

- **Isolation:** container
- **Capabilities:** Multi-language SDKs (Python/Java/JS/C#/Go planned); Unified API; Dual runtime (Docker for dev, K8s for prod); Evaluation and RL training support
- **Requirements:** Docker or Kubernetes; Self-hosted
- **Limitations:** Very new (open-sourced March 2026)

_Notes: Broadest scope of any sandbox — covers evaluation and RL training environments, not just agent sandboxing._

<a id="ref-sand"></a>
## sand

**Maintainer:** banksean · **License:** Apache-2.0 · [Home](https://github.com/banksean/sand)

macOS CLI that spawns disposable Apple Containerization VMs with APFS copy-on-write workspace clones for running coding agents.

- **Isolation:** microvm
- **Capabilities:** Apple Containerization (Kata-based microVMs); APFS clonefile copy-on-write workspace clones; SSH agent forwarding; DNS; eBPF egress filtering with --allowed-domains-file; One-command launch of Claude Code or opencode
- **Requirements:** Apple Silicon; macOS 15+; Homebrew tap
- **Limitations:** macOS only (Apple Silicon); Solo maintainer

_Notes: Apple Containerization gives hardware-isolated micro-VMs (Kata-based) on Apple Silicon. APFS clonefile makes workspace clones instant without copying files. eBPF egress filtering is a notable hardening choice for a solo project._

<a id="ref-sandcastle"></a>
## sandcastle

**Maintainer:** Matt Pocock · **License:** MIT · [Home](https://github.com/mattpocock/sandcastle)

TypeScript library for orchestrating coding agents inside Docker containers with git-aware branch strategies and automatic commit merging.

- **Isolation:** container
- **Capabilities:** Docker container isolation (self-managed, not delegated); Git-aware branch strategy orchestration; Automatic commit merging from agent branches; TypeScript API (sandcastle.run()); npm package
- **Requirements:** Docker; Node.js / TypeScript
- **Limitations:** Orchestration-focused (sandboxing is the mechanism, not the product); Container isolation only (shared kernel)

_Notes: Uses Docker containers it creates directly — not delegating to E2B or Daytona. The git branch strategy (agents work on branches, commits merge back) is the differentiator. Useful if you want multi-agent orchestration with isolation included._

<a id="ref-scode"></a>
## scode

**Maintainer:** Laurent Bindschaedler · **License:** OSS · [Home](https://binds.ch/blog/scode-sandbox-for-ai-coding-tools/)

OS-level sandbox wrapper for any AI coding harness with filesystem and network restrictions.

- **Isolation:** process
- **Capabilities:** OS-level sandboxing; Works with any AI coding tool; Filesystem and network restrictions
- **Requirements:** macOS or Linux
- **Limitations:** Smaller community project

_Notes: Early entry in the space (Sept 2025), motivated by Claude Code's initial lack of built-in sandboxing._

<a id="ref-sevorix-lite"></a>
## sevorix-lite

**Maintainer:** Sevorix · **License:** AGPL-3.0 · [Home](https://github.com/sevorix/sevorix-lite)

Rust-native runtime containment engine combining eBPF syscall interception, mount namespace shell override, HTTP proxy, and a human-in-the-loop policy dashboard.

- **Isolation:** seccomp, user-namespace
- **Capabilities:** eBPF syscall interception (Linux); Mount-namespace bind-mount of sevsh over /bin/bash; HTTP proxy for network filtering; libseccomp integration; Central policy engine with web dashboard; Green/Red/Yellow lane model with human-in-the-loop intervention; Claude Code vault integration; Claims <20ms enforcement latency
- **Requirements:** Linux or WSL (full enforcement); macOS (proxy + shell interception only, no eBPF/seccomp)
- **Limitations:** macOS support is reduced (no eBPF/seccomp); "Lite" edition of a commercial product (Sevorix); AGPL means modifications must be shared

_Notes: Multi-layered runtime containment rather than VM/container isolation. The "Yellow Lane" human-in-the-loop model with countdown timer is unusual — the agent pauses pending human approval via dashboard. Claude Code support is built in, not bolted on._

<a id="ref-skilllite"></a>
## skilllite

**Maintainer:** EXboys · **License:** MIT · [Home](https://github.com/EXboys/skilllite)

Rust single-binary agent engine with a built-in OS-native sandbox using macOS Seatbelt and Linux bubblewrap/seccomp for skill execution isolation.

- **Isolation:** seatbelt, user-namespace, seccomp
- **Capabilities:** OS-native sandbox (Seatbelt on macOS, bubblewrap + seccomp on Linux); Filesystem, network, and IPC lockdown; Process-exec whitelisting; Resource limits via rlimits; Three-layer defense (install-time scan, pre-exec auth, runtime sandbox); Zero-dependency single binary; Sandbox component usable independently of the agent engine
- **Requirements:** macOS or Linux
- **Limitations:** Early project; Smaller community

_Notes: The skilllite-sandbox component is independently usable — you don't have to use the agent engine to get the sandbox. Three-layer defense model (install scan + pre-exec auth + runtime sandbox) is more depth than most standalone tools offer._

