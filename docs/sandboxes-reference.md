# Detailed Sandboxes Reference

Full information for every sandbox tracked in [awesome-agent-sandboxes](../README.md), grouped by category. Use your browser's back button or the link above to return to the main guide.

## Cloud Managed Sandboxes

<a id="ref-alibaba-cloud-agentbay"></a>
### Alibaba Cloud AgentBay

**Maintainer:** Alibaba Cloud (Wuying) · **License:** Closed source · [Home](https://www.alibabacloud.com/product/agentbay) · [Repo](https://github.com/agentbay-ai/wuying-agentbay-sdk)

Managed Alibaba Cloud service running each agent session in a virtual machine with its own guest kernel, built on Wuying cloud desktop infrastructure, offering code, browser, Windows/Linux desktop, and Android mobile environments.

- **Isolation:** kvm
- **Capabilities:** Each sandbox runs in a VM with an independent guest OS kernel on enterprise hardware virtualization (security whitepaper); Environment types Code Space, Browser Use, Computer Use (Windows or Linux desktop), and Mobile Use (Android); Sessions auto-destroyed on timeout or termination; whitepaper states memory and temporary storage are cleared; Security groups admit only the streaming gateway's ASP protocol inbound by default; VPC network isolation; Python, TypeScript, Golang, and Java SDKs plus MCP integration; Custom images based on the built-in Linux base image; cross-session data persistence via contexts; Built-in ToolUseAgent billed in points; device fingerprint as an advanced feature
- **Requirements:** Alibaba Cloud account (free base tier; Pro/Ultra packages or pay-as-you-go)
- **Limitations:** Hypervisor not named; the whitepaper says "enterprise-grade hardware virtualization" only, so [kvm] is inferred from VM-with-own-kernel, not stated; English product overview describes "enterprise-grade secure containers" while the Chinese security whitepaper and FAQ say virtual machine; the two pages disagree in wording; International product page (alibabacloud.com) returned no content when fetched; Chinese page (cn.aliyun.com) and help docs were used; Region list not published on the pages checked ("globally deployed Alibaba Cloud Workspace resource pools")

_Notes: Direct peer of Tencent Cloud Agent Sandbox (AGS), the only other managed offering with Android and Windows sandbox types; AgentBay's isolation is a full VM derived from Wuying cloud desktops rather than AGS's microVM engine. Unlike cua and pixels, the desktop VMs are hosted and billed per concurrent session license. SDK open-source (Apache-2.0, 1,147 stars, last push 2026-06); platform proprietary. Not to be confused with Alibaba Cloud's separate Kubernetes-based Agent Sandbox in Container Compute Service (ACS)._

<a id="ref-beam"></a>
### Beam

**Maintainer:** Beam Cloud · **License:** AGPL-3.0 · [Home](https://www.beam.cloud/sandbox) · [Repo](https://github.com/beam-cloud/beta9)

Serverless AI compute platform whose Sandbox API runs LLM-generated code in gVisor or runc containers with optional GPUs, Docker-in-Docker, snapshots and preview URLs; the open-source beta9 runtime is self-hostable.

- **Isolation:** gvisor, container
- **Capabilities:** beta9 pkg/runtime selects runc or runsc (gVisor) per config, with gVisor platform kvm, systrap or ptrace; "Sandboxes cold boot in 1-3 seconds, even with dependencies included" (vendor docs); image caching for faster reboots; Filesystem snapshots and restart; memory snapshots for fork and resume; GPU attachment (A10G, H100 or other supported GPUs) in the sandbox constructor; Docker-in-Docker; pull from any registry and run containers inside the sandbox; Network isolation with CIDR allow lists; preview URLs expose ports behind SSL-terminated authenticated endpoints; Python, Node.js and arbitrary shell commands; configurable auto-shutdown or indefinite runtime; BYOC on AWS/GCP/Azure/Hetzner and self-hosting of beta9 (vendor blog)
- **Requirements:** Beam account for the managed cloud; Own infrastructure to self-host beta9
- **Limitations:** Isolation runtime is vendor-stated in a Beam blog post ("gVisor + runc"), not in the Sandbox product docs; the beta9 source confirms both backends exist but not which the hosted service uses; BYOC is described in a blog post; no dedicated BYOC page was found in the sandbox docs; beta9 is AGPL-3.0, which constrains network-service redistribution for self-hosters; Managed control plane is proprietary; open_source refers to the beta9 runtime

_Notes: Nearest to Modal (serverless functions plus sandboxes) but with an open-source, AGPL runtime you can run yourself, which Modal lacks; unlike E2B and Daytona the isolation is gVisor/runc containers rather than Firecracker microVMs. SOC 2 Type II is shown in the site footer; YC-backed; $30 free credit refreshed monthly. Blog posts state the gVisor+runc choice was made for lighter operation than microVMs._

<a id="ref-blaxel"></a>
### Blaxel

**Maintainer:** Blaxel · **License:** Closed source · [Home](https://blaxel.ai)

Managed microVM sandboxes for agents with a tmpfs/OverlayFS writable root over an EROFS base image, standby snapshots preserving memory state, persistent volumes and a shared Agent Drive filesystem.

- **Isolation:** microvm
- **Capabilities:** "MicroVM-based sandboxes" that "resume in ~25ms" with memory state intact (vendor); Automatic standby after roughly 15 s of inactivity; standby is billed for snapshot/volume storage only; Writable root filesystem lives in memory (tmpfs, about 50% of RAM reserved) and is wiped when the sandbox is destroyed; Snapshots persist indefinitely; archive mode stores the filesystem without memory state; Volumes persist independently of sandbox lifecycle; Agent Drive mounts one filesystem across many sandboxes; Sandboxes built from Docker images; MCP servers can be hosted the same way; TypeScript and Python SDKs; region selection; CPU allocated proportionally to memory (8GB = 4 cores)
- **Requirements:** Blaxel account (up to $200 free credits, no card)
- **Limitations:** Proprietary platform; hypervisor behind "microVM" is not named in docs; About half of RAM is reserved for the in-memory filesystem; Starter quotas enforce TTL-based deletion; unlimited persistence only on higher tiers; Reserved ports 80, 443 and 8080 cannot be used by workloads

_Notes: Competes directly with E2B and Daytona; the differences are the memory-preserving standby (idle sandboxes cost storage only and resume with process state) and the multi-sandbox Agent Drive. Compliance claims on the homepage: SOC 2 Type II, HIPAA, ISO 27001. Named customers include Webflow, Strapi and Shortwave. YC-backed, San Francisco, founded 2024. SDK repositories were not checked; repo_url left null._

<a id="ref-box-ascii-dev"></a>
### Box (ascii.dev)

**Maintainer:** ASCII (ascii.dev) · **License:** Closed source · [Home](https://box.ascii.dev)

Persistent Ubuntu VMs for agents, each with SSH/SCP, Docker, a dedicated public IP and a streamed virtual desktop, forked at disk level from snapshots and driven by an HTTP API and Python/TypeScript SDKs.

- **Isolation:** kvm
- **Capabilities:** Persistent Ubuntu VM with Docker, VS Code, Chrome, Ghostty, GitHub CLI, Rust, Node.js and Bun preinstalled; SSH and SCP access for humans and agents; Dedicated public IPv4 or IPv6 address per machine; Virtual desktop streamed at 60fps (vendor); Disk-level forking from a snapshot to clone machines; Three sizes (2vCPU/4GB, 4vCPU/8GB, 8vCPU/16GB) billed per second; HTTP API, Python and TypeScript SDKs, CLI with JSON output
- **Requirements:** ASCII account with prepaid balance ($20/month minimum)
- **Limitations:** EU-only regions (Germany, Finland, France); Virtualization stack is not documented; kvm is assumed from the full-VM positioning; Single small vendor with no compliance certifications listed; ascii.dev redirects to the Box product page; Prepaid minimum applies even for light use

_Notes: Full VMs like Freestyle and Fly Sprites, but the differentiators are a routable public IP per VM and a built-in desktop stream, which puts it partway toward cua and pixels (GUI desktop VMs) without their computer-use tooling. Forking is disk-level from a snapshot rather than the live-memory fork Freestyle advertises. Maturity is unproven: one product, no public SDK repositories checked, EU-only footprint._

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

<a id="ref-declaw"></a>
### Declaw

**Maintainer:** Declaw · **License:** Closed source · [Home](https://declaw.ai) · [Repo](https://github.com/declaw-ai)

Firecracker microVM sandboxes fronted by a host-side egress proxy in each sandbox's network namespace that enforces IP, SNI and TLS-inspection policy, injects vault-held credentials, redacts PII and writes audit logs.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVMs with independent filesystem, process tree and network namespace; warm-pool restore in "tens of milliseconds" (vendor); Security proxy runs host-side, outside the guest, as the only egress path, so the workload cannot bypass or tamper with it; Network policy from kernel-level IP/CIDR filtering through SNI domain matching (exact, wildcard, regex) to TLS interception on chosen domains using a per-sandbox CA; Credential vault (OpenBao server-side) injects secrets into outbound requests via vault_refs; the value never enters the VM; PII detection (SSNs, cards, emails, phones) with block/strip/log actions and rehydration in responses; Audit events for every egress decision, redaction and policy block, exposed via console and API; Guardrails refuse dangerous commands and block cloud-metadata/IMDS endpoints; Open-source SDKs for Python, TypeScript and Go, CLI, MCP server, n8n and Dify plugins (Apache-2.0) and the cagecheck escape tester (MIT)
- **Requirements:** Declaw account for api.declaw.ai ($300 free credits) or an enterprise on-prem engagement
- **Limitations:** Platform is proprietary; only SDKs, CLI, MCP server and cagecheck are open; Homepage advertises Terraform modules for AWS and GCP self-hosting, but the deployment docs describe on-prem as a sales-led enterprise engagement; SOC 2 and HIPAA appear only in a sales contact card; no certification is stated; Response bodies are passed through without injection scanning (security-proxy docs); guardrails fall back to a regex scanner if the guardrails service is unreachable

_Notes: The proxy-side secret injection resembles sandcat (Docker tier) and the credential proxy in nono, but Declaw pairs it with Firecracker isolation and moves the proxy off the guest entirely, adding TLS interception, PII redaction and a queryable audit trail. cagecheck, a static binary that reports escape vectors from inside any sandbox, is usable independently of the platform. All GitHub org repositories date from 2026; young vendor._

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

<a id="ref-freestyle"></a>
### Freestyle

**Maintainer:** Freestyle · **License:** Closed source · [Home](https://www.freestyle.sh) · [Repo](https://github.com/freestyle-sh)

Full Linux VMs for agents with root and nested KVM, live-forked while running, hibernated with memory preserved and billed for storage only while paused, controlled through SDKs and a bash API.

- **Isolation:** kvm
- **Capabilities:** Root access; docs list nested virtualization, FUSE, eBPF and full networking; homepage states "full KVM support" for VMs inside VMs and Docker; Vendor claims "65ms from API request to ready machine" (homepage) and "p99s under 400ms" (docs); Live forking: "Clone a running VM without pausing it" (vendor); Hibernation keeps exact memory state; a paused VM bills only for storage; Snapshots with minimal interruption for branching and cloning; shared base snapshots do not count toward quota; Up to 32 vCPU, 64 GiB RAM and 256 GB disk on Pro; larger via enterprise; Free plan includes 200 vCPU-hours, 400 GiB-memory-hours and 60,000 GiB-storage-hours per month as hard allowances
- **Requirements:** Freestyle account
- **Limitations:** Platform proprietary; the open repositories (rigkit CLI/SDK, Adorable, Cloudstate, all MIT) are adjacent tooling rather than the VM runtime; Provisioning figures differ between homepage (~65ms) and docs (p99 under 400ms); neither was measured here; Nested KVM and live fork are verified only as vendor statements on the homepage and docs overview; Free tier is capped with no overage; usage stops when allowances are exhausted

_Notes: Same shape as Fly Sprites and Box (full VMs rather than microVM sandboxes) but with two claims the others do not make: nested KVM inside the guest and forking a VM without pausing it. Compared with E2B the unit is a long-lived machine you hibernate, not an ephemeral sandbox. Customers named on the homepage include Onlook, Wordware and HeroUI; investors Floodgate, Y Combinator, Hustle Fund and Two Sigma Ventures._

<a id="ref-instavm"></a>
### InstaVM

**Maintainer:** InstaVM · **License:** Closed source · [Home](https://instavm.io) · [Repo](https://github.com/instavm)

Hosted microVMs with a dedicated kernel, filesystem and network stack per sandbox, a proxy that injects secrets into outbound requests so keys never enter the VM, and deny-by-default egress with runtime audit logs.

- **Isolation:** microvm
- **Capabilities:** Each sandbox gets its own kernel, filesystem and network stack (vendor); Vendor claims "P95 cold start" of 185 ms and a full Linux microVM booting "in under 200ms without pre-warming"; Secrets injected by proxy at request time; agents never hold API keys; Egress deny-by-default with domain/CIDR allowlists and separate toggles for package managers and HTTP/HTTPS; Read-only mounts; execution logs, network traces and runtime events recorded per run; Python and TypeScript SDKs plus an SSH CLI (ssh instavm.dev); 10 GB volume storage included on Free and Pro tiers
- **Requirements:** InstaVM account ($50 free credits, no card; Pro from $100/month plus usage)
- **Limitations:** Platform proprietary; the hypervisor behind "microVM" is not named; No compliance certifications listed; Technical docs pages could not be fetched; features are taken from the marketing site; Cold-start and isolation figures are vendor statements, not measured

_Notes: Feature set overlaps Declaw (proxy-side secrets, default-deny egress, audit) and E2B (microVM sandboxes) but with fewer policy layers than Declaw and no BYOC option found. The same team publishes CodeRunner (github.com/instavm/coderunner, Apache-2.0), a local runner using Apple container on Apple Silicon macOS with an MCP server; that is the open-source part, the cloud platform is not._

<a id="ref-islo"></a>
### Islo

**Maintainer:** Islo Labs (team behind Incredibuild) · **License:** Closed source · [Home](https://islo.dev) · [Repo](https://github.com/islo-labs/skills)

Hosted computers for autonomous coding agents, each a dedicated microVM behind an egress gateway that injects credentials into outbound requests so secrets never enter sandbox memory, with orchestration for ticket-to-PR workflows.

- **Isolation:** microvm
- **Capabilities:** Dedicated microVM per computer (docs comparison table lists "Hardware-level – dedicated microVM" against "shared kernel" dev environments); Egress gateway credential injection: sandbox sends a placeholder (Bearer $GITHUB_TOKEN) and the gateway substitutes the real token at egress, with per-request audit; Egress allowlists/blocklists (e.g. allow a preview stack, block production APIs) and content filters on egress; Persistent computers that keep state across disconnects; default size 2 vCPU / 4 GB RAM / 10 GB SSD; Multi-stage "factory line" orchestration for unattended agent runs (tests, PR review, bug fixes, migrations); Deployment in Islo cloud, the customer's cloud (BYOC / own VPC), or the customer's customers' cloud; MCP server and agent skills for Cursor, Claude Code, and Codex
- **Requirements:** Islo account (sign-up credits, no credit card)
- **Limitations:** VMM not named anywhere on the site or docs; "dedicated microVM" is the only isolation statement; Platform is proprietary; the only public repo (islo-labs/skills, MIT) contains agent skills and plugin metadata, no runtime code; Billing is usage-based at hourly rates ($0.07/CPU-hour, $0.04/GB-hour, $0.0007/GB-hour storage); the site says "pay only while it runs" but does not state per-second granularity; New product (skills repo created 2026-07); no public adoption figures

_Notes: Closest to nono and agent-glovebox in intent (credentials never reach the agent) but delivered as a hosted service: the gateway rewrites tokens at the network edge, whereas nono proxies from the host and Docker Sandboxes / E2B expose secrets as environment variables. Compared with E2B and Daytona, Islo bundles the orchestration layer (queues, webhooks, PR return) rather than only the sandbox API. Built by the Incredibuild team; the product page lists Incredibuild's enterprise customers, not Islo's._

<a id="ref-leap0"></a>
### Leap0

**Maintainer:** Leap0 · **License:** Closed source · [Home](https://leap0.dev) · [Repo](https://github.com/leap0-dev)

Hosted Firecracker microVM sandboxes with a jailed VMM process, memory-plus-disk snapshots, per-sandbox egress firewall with host-side header injection, and an XFCE desktop for code execution, browser, and desktop automation.

- **Isolation:** microvm, kvm
- **Capabilities:** Firecracker microVM per sandbox with a dedicated Linux 6.1 LTS guest kernel; VMM process hardening (vendor statement): Firecracker launched via the Jailer with chroot, cgroup v2, seccomp filters, and unique UID/GID pairs; Snapshots capture in-memory execution state plus writable disk; restore creates a new sandbox from a named checkpoint; Egress firewall modes allow-all / deny-all / custom with allow_domains, allow_cidrs, and per-domain header transforms that inject credentials host-side; Full XFCE desktop at 1440x900 with screenshot, mouse, keyboard, and screen recording; Python, TypeScript/JavaScript, and Go SDKs; MCP server; LangChain (Python and JS), Google ADK plugin, and a Mastra coding-agent template; Vendor claims sandboxes boot in around 100ms
- **Requirements:** Leap0 account (free during public preview, no credit card)
- **Limitations:** Public preview; no published pricing; Sandboxes run only in the US at inclusion; Default network policy is allow-all when network_policy is omitted; Only connections to domains with transform rules are TLS-terminated; other allowed domains pass as opaque tunnels, so header transforms cannot be applied to them

_Notes: Functionally the nearest hosted peer to E2B (Firecracker, Python/TS SDKs, snapshots), adding a firewall that injects credentials at the host like agent-glovebox's credential scoping, and a bundled desktop like cua and pixels. The jailer hardening statement (chroot, cgroup v2, seccomp, unique UID/GID) is more specific than most hosted vendors publish; it is the Firecracker Jailer's documented feature set and is stated by the vendor, not independently verified. SDKs, MCP server, and integrations are open-source (Apache-2.0) under github.com/leap0-dev; the platform is proprietary._

<a id="ref-modal"></a>
### Modal

**Maintainer:** Modal Labs · **License:** Closed source · [Home](https://modal.com/products/sandboxes)

Serverless cloud platform with sandbox product and best-in-class GPU support.

- **Isolation:** microvm
- **Capabilities:** Sub-second starts; GPU workloads; Network tunnels; Per-sandbox egress policies; 50k+ concurrent sessions
- **Requirements:** Cloud-hosted; Python SDK; Usage-based pricing
- **Limitations:** Closed source; Cloud-only; Python-centric SDK

_Notes: Only major sandbox platform with GPU support — unique differentiator for ML/AI workloads that need compute._

<a id="ref-morph-cloud"></a>
### Morph Cloud

**Maintainer:** Morph Labs · **License:** Closed source · [Home](https://cloud.morph.so) · [Repo](https://github.com/morph-labs/morph-python-sdk)

Hosted VM instances whose "Infinibranch" snapshots capture memory and disk of a running machine, so one instance can be branched into many clones that resume from the same point for parallel agent runs.

- **Isolation:** kvm
- **Capabilities:** Full VM instances started from immutable snapshots; snapshots capture memory and disk state including running processes; Branch a running instance into N clones (instance.branch(count=3)) via SDK or CLI; Vendor claims <250 ms snapshot, branch, and restore of a running VM; Devboxes (persistent workspaces) with SSH, VS Code/Cursor attach, tmux automation, and shareable preview URLs; scale-to-zero preserving memory state; Morph EFS persistent filesystem attachable to instances; Python and TypeScript SDKs, morphcloud CLI, REST API; GitHub Actions runners billed from the same credits
- **Requirements:** Morph Cloud account (free tier: 300 MCU credits)
- **Limitations:** Hypervisor/VMM not named in docs or blog; "VM" is the only mechanism term; morph.so landing page is near-empty; product information lives at cloud.morph.so; Billing uses an abstract unit (1 MCU = 1 vCPU-hour + 4 GB RAM-hours + 16 GB disk-hours, $0.05) that complicates comparison; Small public footprint (Python SDK 3 stars, TypeScript SDK 4 stars at inclusion)

_Notes: Differs from E2B, Daytona, and Modal in making memory-inclusive branching of a live VM the core primitive rather than a feature: the intended workflow is to fork one agent state into many and compare outcomes. Runloop and Fly Sprites offer snapshots but not documented fan-out of a running machine's memory. SDKs open-source (Apache-2.0); platform proprietary._

<a id="ref-northflank"></a>
### Northflank

**Maintainer:** Northflank · **License:** Closed source · [Home](https://northflank.com)

Production-grade sandbox infrastructure using Kata Containers and gVisor at 2M+ isolated workloads/month.

- **Isolation:** kata, gvisor
- **Capabilities:** MicroVM via Kata + gVisor; Unlimited session duration; Any OCI image; BYOC (bring your own cloud) deployment; Resource limits; Network controls
- **Requirements:** Cloud-hosted or BYOC; Paid platform
- **Limitations:** Closed source; More complex setup than simpler platforms

_Notes: BYOC option is unusual in this space — most cloud sandboxes are single-provider. Production-proven at scale (2M+ workloads/month)._

<a id="ref-novita-sandbox"></a>
### Novita Sandbox

**Maintainer:** Novita AI · **License:** Closed source · [Home](https://novita.ai/sandbox) · [Repo](https://github.com/novitalabs/NovitaBox)

Hosted agent runtime that runs each session in a dedicated Firecracker microVM with its own kernel, offering code execution, browser use, desktop control with live VNC view, and pause/resume with memory preserved.

- **Isolation:** microvm, kvm
- **Capabilities:** Dedicated Firecracker microVM per session with its own kernel, isolated memory boundary, and ephemeral filesystem (vendor press release, 2026-04); Pause/resume preserving filesystem and memory state; vendor states resume takes about a second; Code execution (Python, JavaScript, C++), browser use, and computer use with a live VNC session view; Secured access on by default since SDK v2.0.0; per-sandbox secrets; SSH access and interactive terminal; Agent Runtime deploys LangGraph, OpenAI Agents SDK, AutoGen, and Google ADK agents into sandboxes via an AgentRuntimeApp entrypoint; Python and JS/TS SDKs (novita-sandbox on PyPI and npm) and a CLI (novita-sandbox-cli); templates and snapshots; NovitaBox local edition runs the same SDK against Firecracker, gVisor, or Cloud Hypervisor on the developer's machine
- **Requirements:** Novita AI account ($100 free credit for 90 days, no credit card)
- **Limitations:** Landing page describes isolation only as "system-level separation"; the microVM-per-session detail appears in a press release and third-party coverage, not in the docs pages checked; "Memory sanitized on termination" could not be located in Novita docs or the press release; only "ephemeral filesystem" and "isolated memory boundary" are stated; AgentCore compatibility not stated; the Agent Runtime API shape (AgentRuntimeApp, @app.entrypoint) mirrors AWS Bedrock AgentCore's but no compatibility claim was found; Landing page says "AICPA SOC 2 Certified"; Type I/II not stated

_Notes: Positioned like E2B (Firecracker, E2B-style SDK/CLI, templates) with two additions: an Agent Runtime deployment layer for framework agents and an open-source local edition (NovitaBox, Apache-2.0) that shares the SDK, a pairing similar to Tencent Cloud AGS with CubeSandbox. Free tier limits are 5 concurrent sandboxes, 1-hour sessions, 2 vCPU / 4 GB each. Provider press release is datelined San Francisco; the brief's "Asia-based" was not confirmed from public pages._

<a id="ref-omnirun"></a>
### OmniRun

**Maintainer:** A14A B.V. · **License:** Closed source · [Home](https://omnirun.io) · [Repo](https://github.com/a14a-org/omnirun-claude-managed-agents-worker)

Hosted ephemeral Firecracker microVMs on KVM with a dedicated guest kernel per sandbox, destroyed after each run, with a self-hostable worker that executes Claude Managed Agents tool calls inside them.

- **Isolation:** microvm, kvm
- **Capabilities:** Isolation stack: userspace, dedicated guest kernel, Firecracker VMM, KVM, hardened host OS; each sandbox boots its own Linux kernel; Sandboxes destroyed completely on termination; no state carried between executions by design; File upload/download via signed, time-bound URLs scoped to a single sandbox; No internet access by default; optional SNI egress proxy allowlists hosts by TLS handshake inspection; TypeScript (@omnirun/sdk) and Python (omnirun) SDKs, CLI, REST API, LangChain and LlamaIndex integrations; Self-hosted worker (AGPL-3.0) polls Anthropic's Claude Managed Agents queue and runs tool calls in fresh microVMs on your own KVM host; Vendor claims boot times from 247ms (landing example) to 842ms median (1,000 cold starts on Hetzner AX102 bare metal)
- **Requirements:** OmniRun account (free tier 25 sandbox-hours/month, no credit card); For self-hosted worker executor: Linux host with /dev/kvm, Firecracker, LVM thin provisioning
- **Limitations:** Small team (A14A B.V., Amsterdam; worker repo has 2 contributors and 0 stars at inclusion); no public members listed; No compliance certifications (SOC 2, HIPAA, ISO) per the worker README; Worker README states egress is open by default for the Claude Managed Agents worker, in contrast to the platform default of no internet; Solutions page says one microVM per tool call; the worker README describes one microVM per session; which applies was not resolved

_Notes: Overlaps with Tensorlake as a Claude Managed Agents execution backend, but OmniRun's worker is the open-source piece (AGPL-3.0) and runs on the customer's own KVM host, while Tensorlake hosts the sandbox. Statelessness is a deliberate contrast with Morph Cloud and Leap0, whose snapshots carry state forward. Platform proprietary; SDKs (MIT) at github.com/a14a-org._

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

<a id="ref-tencent-cloud-agent-sandbox-ags"></a>
### Tencent Cloud Agent Sandbox (AGS)

**Maintainer:** Tencent Cloud · **License:** Closed source · [Home](https://cloud.tencent.com/product/ags)

Managed Tencent Cloud service running agent workloads in per-sandbox KVM microVMs with dedicated guest kernels, exposing E2B-compatible APIs across code-execution, browser, Android, Windows, and computer-use sandbox types.

- **Isolation:** microvm, kvm
- **Capabilities:** Per-sandbox microVM with a dedicated guest kernel (KVM hardware virtualization); eBPF network segmentation; E2B-compatible API, Python/Go/Node SDKs, and an agr CLI; Code-execution, browser, mobile (Android/Appium), Windows, and computer-use sandbox types; Custom container images; Vendor claims <60ms cold start, <5MB per-sandbox memory overhead, 2,000+ sandboxes per 96-vCPU host
- **Requirements:** Tencent Cloud (mainland China) account
- **Limitations:** Closed beta; one documented region (ap-guangzhou); no published pricing; Chinese-only product and docs pages (English exists only in the GitHub cookbook)

_Notes: The only cloud-managed entry offering managed Android and Windows sandboxes. Press coverage indicates the engine is Tencent's open-source CubeSandbox (also listed) — inferred, not stated on the product page. Samples at github.com/TencentCloudAgentRuntime/ags-cookbook._

<a id="ref-tensorlake"></a>
### Tensorlake

**Maintainer:** Tensorlake · **License:** Closed source · [Home](https://tensorlake.ai) · [Repo](https://github.com/tensorlakeai/tensorlake)

Hosted Firecracker and Cloud Hypervisor microVM sandboxes for agent harnesses and tool calls, with memory snapshots, auto suspend/resume, hosted Git, cloud volumes, and a serverless orchestration runtime for agent CI.

- **Isolation:** microvm, kvm
- **Capabilities:** MicroVMs backed by Firecracker and Cloud Hypervisor; vendor states each tool call and harness runs in its own microVM with no shared kernel; Snapshots of memory and filesystem; clone running sandboxes across machines; auto suspend/resume (vendor states ~0.6s resume); Per-sandbox network policy (no-internet, allowlist by host) via tl sbx update; Hosted Git repositories, cloud volumes, and repository mounts inside sandboxes; Serverless orchestration (endpoints, durability, fan-out, retries) for long-running agent workflows; Integrations: Claude Managed Agents orchestrator in-sandbox, Harbor environment provider for evals/RL, OpenCode tool routing, Devin Outposts; Python and TypeScript SDKs, tl CLI, HTTP API; BYOC on AWS
- **Requirements:** Tensorlake account (self-serve free tier at cloud.tensorlake.ai)
- **Limitations:** The tensorlakeai/tensorlake repo (Apache-2.0) contains SDKs, CLI, function-agent-core, and filesystem client crates; the control plane and VM scheduler (Lattice) are not in it; Landing page claims one microVM per tool call, but the Claude Managed Agents docs describe a single per-session sandbox running all tool calls; Custom environments must be registered Sandbox Images; arbitrary Docker image references are not supported; SQLite I/O benchmark vs Vercel, E2B, Modal, Daytona is vendor-run

_Notes: Closest to Modal in scope (compute plus orchestration) and to E2B/Daytona in the sandbox API, with the Harbor eval integration and hosted Git as distinguishing pieces. SOC 2 Type II, HIPAA, EU data residency, and zero data retention are stated on the docs introduction. Backed by Redpoint and Amplify per the landing page; repo has 996 stars and daily commits at inclusion. Open-source components are the SDKs/CLI (Apache-2.0); platform proprietary._

<a id="ref-vercel-sandbox"></a>
### Vercel Sandbox

**Maintainer:** Vercel · **License:** Closed source · [Home](https://vercel.com) · [Repo](https://github.com/vercel/sandbox)

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

<a id="ref-onecli"></a>
### OneCLI

**Maintainer:** OneCLI · **License:** Apache-2.0 · [Home](https://onecli.sh) · [Repo](https://github.com/onecli/onecli)

Per-employee agent platform that runs each agent in a Docker container on an internal network whose only route out is a Rust MITM gateway that injects credentials and enforces team policy.

- **Isolation:** container
- **Capabilities:** Runner starts, parks, and reaps agent containers on an internal Docker network (no route out) pinned with no-new-privileges, CapDrop ALL, and the default seccomp profile; Rust gateway intercepts outbound HTTP and HTTPS (MITM) and injects credentials matched by host and path pattern; agents hold only Proxy-Authorization access tokens; Bitwarden or 1Password vault integration for on-demand injection with nothing stored on the server; Deterministic human-in-the-loop approvals in chat for designated actions; Identity-provider provisioning of one agent per employee; dashboard and per-agent Slack app; Secret store encrypted AES-256-GCM at rest; SSH front door with short-lived certificates into sandboxes; Runner is outbound-only, so sandboxes can run on a laptop, homelab, or VPC behind NAT
- **Requirements:** Docker host for the runner plus PostgreSQL; pnpm run setup or the install script generates Docker Compose configuration; Company account on onecli.sh for the hosted variant
- **Limitations:** Docker is the only shipped runtime backend (RUNNER_BACKEND=docker or fake); the runner README lists Fly, k8s, and microVMs as future substrates; Nested containers inside a sandbox are deliberately inert under the Docker backend; the README says they work only on the hosted microVM substrate; ee/ directories are under the OneCLI Enterprise License, requiring a subscription for production use; contributions require a CLA; Created 2026-03; the sandboxing model relies on Docker's shared kernel plus network egress control rather than VM isolation

_Notes: OneCLI began as a Rust credential vault for agents and pivoted (v2) to a team platform; the company also sells a hosted version. Its credential-injecting egress gateway is the same mechanism as nono's credential proxy and agent-glovebox's credential scoping, applied at team scale with IdP provisioning and approvals. The isolation boundary is a hardened Docker container on an internal network, weaker than Docker Sandboxes' microVM or the microVM entries; the value is the policy and secrets plane rather than the sandbox itself._

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

## Standalone / Local Tools

<a id="ref-agent-safehouse"></a>
### Agent Safehouse

**Maintainer:** eugene1g · **License:** OSS · [Home](https://github.com/eugene1g/agent-safehouse)

macOS sandbox-exec profile system with deny-first policy, composable profiles, and pre-built agent configurations.

- **Isolation:** seatbelt
- **Capabilities:** macOS Seatbelt profile generation; Deny-first policy; Composable profile system; Pre-built profiles for major coding agents; Policy builder web tool; Fine-grained HOME access control; Symlink-aware path resolution
- **Requirements:** macOS only; brew install eugene1g/safehouse/agent-safehouse
- **Limitations:** macOS only (permanently — sandbox-exec is Apple-specific); sandbox-exec deprecation risk

_Notes: More mature than it appears — has CI tests, docs site, and thoughtful profile composition. The most polished macOS-specific sandboxing option._

<a id="ref-agent-glovebox"></a>
### agent-glovebox

**Maintainer:** AlexanderMattTurner · **License:** Apache-2.0 · [Home](https://github.com/AlexanderMattTurner/agent-glovebox)

Security wrapper that runs Claude Code sessions inside a Docker sbx microVM with an egress allowlist, a second-model monitor gating tool calls, per-repo credential scoping, and a tamper-evident audit log.

- **Isolation:** microvm
- **Capabilities:** Hypervisor-isolated microVM via Docker's sbx runtime (Linux/KVM, Apple Silicon macOS, WSL2); Project-directory-only bind mount; read-only system filesystems; unprivileged user; ephemeral per-session volumes; Network egress restricted to an allowlist firewall; Second-model monitor gates flagged tool calls, sends phone push notifications, and can halt the agent remotely; Per-repository GitHub tokens generated outside the sandbox and never mounted into it; Tamper-evident audit log stored outside the sandbox; panic command captures a forensics snapshot; Edits returned on a glovebox/* branch for manual approval; Privacy modes routing inference to open-weights or TEE-hosted providers
- **Requirements:** Docker with the sbx sandbox runtime; Claude Code
- **Limitations:** Very new (created 2026-05-24; ~10 weeks at inclusion); Monitor and sanitization layers are best-effort filters on top of the hard boundaries

_Notes: Clears the container-tier bar on three axes at once — per-repo credential scoping, second-model threat detection with human-in-the-loop halt, and an external tamper-evident audit trail — a combination none of the other Claude Code wrappers offer. Ships a written threat model and heavy security CI (gitleaks, grype, mutation testing), unusual at its size._

<a id="ref-agent-infra-sandbox"></a>
### agent-infra/sandbox

**Maintainer:** agent-infra (community) · **License:** OSS · [Home](https://github.com/agent-infra/sandbox)

All-in-one sandbox combining Browser, Shell, File management, MCP, and VSCode Server in a single Docker container.

- **Isolation:** container
- **Capabilities:** Browser automation; Shell access; File management; MCP integration; VSCode Server
- **Requirements:** Docker
- **Limitations:** Container isolation only (shared kernel); Monolithic design

_Notes: Kitchen-sink approach — good for prototyping and development, less suitable for security-critical production use._

<a id="ref-agent-sandbox-nix"></a>
### agent-sandbox.nix

**Maintainer:** archie-judd · **License:** MIT · [Home](https://github.com/archie-judd/agent-sandbox.nix)

Nix library and flake templates that wrap an agent binary in bubblewrap (Linux) or sandbox-exec (macOS) with declared paths, an ephemeral home, a domain- and method-filtering HTTP proxy, and read-only git hooks and config.

- **Isolation:** user-namespace, seatbelt
- **Capabilities:** Declarative mkSandbox arguments for rwDirs/rwFiles/roDirs/roFiles, allowedPackages (PATH allowlist), and env passthrough; allowedDomains routes HTTP/HTTPS through a filtering proxy with per-domain HTTP method lists; DNS and WebSockets blocked when active; Host loopback blocked by default; allowedLocalPorts opens specific TCP ports; Ephemeral tmpfs $HOME; host environment cleared except declared variables; Git .git/hooks, config, config.worktree, and worktree/submodule pointer files mounted read-only to prevent host code execution via git; Symlinks in declared paths resolve only to already-permitted targets, preventing sandbox expansion between sessions; Per-launch session directory logging bwrap args, seatbelt profile, firewall rules, and blocked proxy requests; Flake templates for Claude Code and GitHub Copilot CLI
- **Requirements:** Nix with flakes (or nix-shell) on Linux or macOS; bubblewrap-capable Linux (unprivileged user namespaces) or macOS with sandbox-exec
- **Limitations:** Requires adopting Nix; the wrapper is built per-project via flake.nix or shell.nix; The README states the agent can edit flake.nix inside the writable project directory and weaken its own next session, and that a launch from $HOME exposes the whole home; On macOS, gh and other Go tools reject the proxy certificate when allowedDomains is set; sandbox-exec is deprecated; All of /nix/store is readable (allowedPackages restricts execution only); allowNix exposes the daemon socket and weakens the sandbox

_Notes: Same bwrap/Seatbelt plus domain-proxy shape as Anthropic sandbox-runtime srt, but expressed as Nix derivation arguments so the sandbox definition is reproducible and version-pinned with the agent binary itself. Specific to this entry are HTTP-method filtering per domain, read-only git metadata against hook injection, and the symlink-target check. The README's own similar-projects list names srt, jail.nix, jailed-agents, and ai-jail. About 150 GitHub stars at inclusion; sole maintainer, pushes in the week of review; v1.x renamed several arguments from v0.x._

<a id="ref-agent-sandbox"></a>
### agent_sandbox

**Maintainer:** katosh · **License:** MIT · [Home](https://github.com/katosh/agent_sandbox)

Kernel-enforced user-space sandbox for AI coding agents with multi-backend isolation (bubblewrap, firejail, Landlock LSM) and a Slurm "chaperon" proxy that propagates sandboxing onto HPC compute nodes.

- **Isolation:** user-namespace, landlock, seccomp
- **Capabilities:** Bubblewrap primary backend (user namespaces + bind mounts, no setuid required); Firejail and Landlock LSM fallback backends; Generated seccomp-BPF filters per syscall (x86_64 and aarch64); Slurm chaperon proxy wrapping sbatch/srun/squeue/scancel/scontrol/sacct/sacctmgr; In-sandbox Slurm stubs talk to outside chaperon via named pipes; Whitelist validation of Slurm flags; denies --pty/--container/--uid/--prolog/--bcast/--get-user-env; Sandbox-exec wrapping injected onto allocated compute nodes; Supports Claude Code, Codex, Gemini, Aider, OpenCode, pi-mono
- **Requirements:** Linux; Bubblewrap (or firejail/Landlock-capable kernel)
- **Limitations:** Linux-only — no macOS path; No egress allowlist or credential proxy (acknowledged in landscape doc); Author flags as "best-effort user-space isolation, not a security product"; Young project (2 critical / 3 high pentest findings documented and addressed)

_Notes: Only sandbox surveyed with first-class HPC/Slurm awareness — the chaperon proxy intercepts Slurm submission and wraps job commands so an agent cannot escape by submitting an unsandboxed job to a compute node. Munge auth is deliberately blocked inside the sandbox so only the outside chaperon can submit. Bind-mount filesystem isolation returns ENOENT rather than EACCES, which sidesteps the ld-linux and /proc/self/root evasions that have hit Landlock-allowlist sandboxes. Ships with a 32 KB threat model and a documented pentest cycle._

<a id="ref-agentbox"></a>
### agentbox

**Maintainer:** madarco · **License:** MIT · [Home](https://agent-box.sh) · [Repo](https://github.com/madarco/agentbox)

Node CLI that runs Claude Code, Codex, or OpenCode in parallel Docker containers with a FUSE overlay workspace, locally, over SSH, or on Hetzner, Daytona, Vercel, E2B, or DigitalOcean, keeping git credentials on the host.

- **Isolation:** container
- **Capabilities:** One command per box (agentbox claude) creating a Docker container with a FUSE overlay over the project workspace; Git credentials stay on the host; pushes go through a host relay with a permission prompt per push; Providers for local Docker, remote Docker over SSH, Hetzner, Daytona (partial), Vercel Sandbox, E2B, and DigitalOcean, plus a provider-plugin SDK; Checkpoints of warm box state to start new boxes from; pause/unpause; docker commit snapshots on remote Docker; In-box browser over noVNC (agentbox screen), VS Code/Cursor attach via Dev Containers, persistent tmux-style shells; Copies host Claude Code, Codex, and OpenCode settings, skills, and plugins into the box; Preview URLs via portless or OrbStack; dashboard and live resource monitor across boxes; Host relay and optional macOS menu-bar app
- **Requirements:** macOS (arm64 or Intel) or Linux with Docker Desktop or OrbStack; Node 20.10+; first run builds a ~1 GB image; cloud providers need their own accounts and tokens
- **Limitations:** Local isolation is a Docker container (the README calls boxes VMs, but the local backend is Docker plus FUSE overlay); no gVisor, seccomp customization, or egress allowlist documented in the README; Vendor claims sub-second box startup from a checkpoint; not independently measured; Daytona support marked partial and its live snapshots experimental in the provider table; Solo maintainer; contributions require a CLA

_Notes: Distinct from the listed agentbox-sdk. Nearest entries are Docker Sandboxes and agent-glovebox for the local Docker workflow, and the hosted E2B, Daytona, and Vercel Sandbox entries, which agentbox treats as interchangeable backends behind one CLI. The differentiator is the developer workflow around many parallel boxes (checkpoints, dashboard, IDE and VNC attach) and the host-side git relay with per-push approval, rather than a stronger isolation boundary. About 380 GitHub stars at inclusion; pushes on the day of review._

<a id="ref-agentsh"></a>
### agentsh

**Maintainer:** canyonroad · **License:** Apache-2.0 · [Home](https://github.com/canyonroad/agentsh)

Policy-enforced execution gateway that intercepts file, network, process, and signal syscalls for agent commands with allow/deny/approve/redirect decisions and structured audit.

- **Isolation:** process, landlock, seatbelt
- **Capabilities:** Syscall interception (file, network, process, signal); Subprocess tree coverage; Allow/deny/approve/redirect policy decisions; Structured audit events; Pairs with containers; Cross-platform (Linux LSM/FUSE, macOS ESF+NE, Windows minifilter); Linux is production-ready; macOS alpha; Windows pending driver signing
- **Requirements:** Linux (production), macOS (alpha), or Windows (pending); Homebrew, .deb, .rpm, or .apk install
- **Limitations:** macOS support is alpha; Windows support pending driver signing

_Notes: Real runtime enforcement, not just wrapping. The "redirect" policy decision is unusual — can transparently steer agent network calls or out-of-workspace writes to scratch dirs without the agent knowing it was redirected._

<a id="ref-ai-jail"></a>
### ai-jail

**Maintainer:** akitaonrails · **License:** GPL-3.0-only · [Home](https://github.com/akitaonrails/ai-jail)

Rust launcher that runs coding agents under bubblewrap plus Landlock, seccomp, and rlimits on Linux, or sandbox-exec on macOS, with an ephemeral tmpfs home and opt-in credential mounting.

- **Isolation:** user-namespace, landlock, seatbelt
- **Capabilities:** Fresh tmpfs $HOME per launch; agent credential state (~/.claude, ~/.claude.json) mounted only with --agent-state; Network, GPU, display, X11, host /dev/shm, Docker socket, SSH, and systemd user bus all default off with paired --x/--no-x flags; Minimal environment allowlist; --env forwards single variables, env_pass in trusted global config; --mask replaces project secrets (.env, *.pem) with empty placeholders; --deny-path hides them entirely; Layered config where project ./.ai-jail can only tighten policy and ~/.ai-jail is the trusted layer that can grant capabilities; Isolated browser profiles (--browser), copy-on-write overlay maps on Linux, mise toolchain activation inside the sandbox; Terminal output filtered through a VT parser by default; raw passthrough is opt-in; Ships via Homebrew, AUR, crates.io, Nix flake, and signed GitHub releases
- **Requirements:** Linux with bubblewrap installed (unprivileged user namespaces enabled), or macOS with sandbox-exec; Rust 1.97 to build from source; no Windows support (WSL2 only)
- **Limitations:** The README states it is "a useful layer, not a replacement for a disposable VM when running hostile code" and does not protect against kernel, driver, or terminal-emulator vulnerabilities; GPL-3.0-only copyleft; relevant if embedding in a distributed product; macOS backend uses the deprecated sandbox-exec interface and has no mount namespace, so /tmp is the host's; --allow-tcp-port fails closed by design; network is all-or-nothing (--network), with no domain or port allowlist

_Notes: Same bwrap-plus-Seatbelt base as Anthropic sandbox-runtime srt and fence, but ai-jail's distinguishing choices are a default private tmpfs home with credentials excluded unless requested, a monotonic project config that a repository cannot use to loosen policy, and secret masking for files inside the writable project tree. Unlike srt it has no domain proxy, so network is either off or unrestricted. About 1,180 GitHub stars at inclusion; maintained by Fabio Akita (akitaonrails) with pushes in the week of review._

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

<a id="ref-axern"></a>
### axern

**Maintainer:** cofy-x (Chen Yingwei) · **License:** Apache-2.0 · [Home](https://github.com/cofy-x/axern)

Self-hostable sandbox platform running untrusted agent code under gVisor and trusted long-lived services under runc, behind one PostgreSQL-backed control plane with Go/Python/TypeScript SDKs.

- **Isolation:** gvisor, container
- **Capabilities:** gVisor (runsc) user-space kernel as the untrusted-code boundary; Dual runtime — runc containers for trusted durable services under the same lifecycle APIs; Control plane owns placement, leases, replicas, health, storage, and rollouts across restarts; OCI and Nydus (lazy-loading rootfs) image paths; Docker Compose local mode and a cloud-neutral Helm chart; Axrun agent-task harness with verification, trajectories, and typed artifacts
- **Requirements:** Docker Compose (local) or Kubernetes (Helm); Linux hosts for runsc
- **Limitations:** Six days of public history at inclusion; single maintainer; pre-1.0; README disclaims multi-tenant production safety of default deployments

_Notes: The only self-hostable platform entry using gVisor as its untrusted-code boundary — the peers are plain-container (OpenSandbox, EdgeBox, agent-infra) or microVM (microsandbox). Included with strong maturity caveats: the scaffolding (docs site, three SDKs, Helm chart, governance files) far exceeds its public age, implying prior private development; sustainability unproven._

<a id="ref-boxlite"></a>
### boxlite

**Maintainer:** boxlite-ai · **License:** Apache-2.0 · [Home](https://github.com/boxlite-ai/boxlite)

Embeddable, daemonless microVM runtime that boots any OCI image under KVM or Hypervisor.framework, wraps the VMM process in seccomp or sandbox-exec, and keeps per-box state across agent turns.

- **Isolation:** microvm, kvm, seccomp
- **Capabilities:** Runs unmodified Docker/OCI images (e.g. python:slim, node:alpine) as hardware-isolated microVMs; Embeds as a library with no root and no background service; optional server mode with REST API; OS-level sandbox (seccomp on Linux, sandbox-exec on macOS) around the VMM process for defense in depth; Egress allow-list via allow_net; Secret injection: real values never enter the VM; Per-box QCOW2 copy-on-write disk; boxes persist across stop/restart; SDKs for Python, Node.js, Go, Rust, and C plus a boxlite CLI
- **Requirements:** macOS 12+ on Apple Silicon, Linux with /dev/kvm, or WSL2 with KVM support; Language SDK or CLI install
- **Limitations:** macOS Intel (x86_64) listed as "Coming soon"; No boot-time figures in the README; performance claims unverified; Secret-injection mechanism (proxy vs. env substitution) not described in the README; unverified

_Notes: Nearest peer is microsandbox (libkrun, local-first): boxlite differs by running OCI images directly rather than a custom image format, by the seccomp/sandbox-exec wrapper around the VMM process, and by a five-language SDK surface. AgentScope Runtime (listed) ships a boxlite_client.py container backend, the main adoption signal at inclusion. Roughly 2.3k GitHub stars (2026-09)._

<a id="ref-brood-box"></a>
### brood-box

**Maintainer:** Stacklok · **License:** Apache-2.0 · [Home](https://github.com/stacklok/brood-box)

CLI that runs coding agents inside hardware-isolated microVMs with COW workspace snapshots and interactive per-file diff review before changes land.

- **Isolation:** kvm, microvm
- **Capabilities:** Hardware VM isolation (libkrun/KVM on Linux, Hypervisor.framework on macOS); COW workspace snapshots; Interactive per-file diff review (VM stopped before review, TOCTOU-resistant); DNS-aware egress firewall; Ephemeral SSH keys; Non-overridable secret exclusions; Permission stripping on flush
- **Requirements:** Linux (KVM) or macOS (Apple Silicon, Hypervisor.framework)
- **Limitations:** Experimental

_Notes: From Stacklok (founded by Luke Hinds of Sigstore). Hardware VM isolation like cleanroom, but adds TOCTOU-resistant diff review — the VM is stopped before the user reviews changes, preventing the agent from modifying files during review. DNS egress firewall and non-overridable secret exclusions are strong default posture._

<a id="ref-bx-mac"></a>
### bx-mac

**Maintainer:** holtwick · **License:** MIT · [Home](https://github.com/holtwick/bx-mac)

macOS CLI that launches GUI apps and agent CLIs under a generated Seatbelt profile denying access to everything in the home directory except the specified project directories.

- **Isolation:** seatbelt
- **Capabilities:** Kernel-enforced filesystem isolation via sandbox-exec with generated SBPL profiles; Sandboxes full GUI IDEs (VSCode, Cursor, Xcode, Zed), terminals, and arbitrary commands; Electron detection that disables Chromium's internal sandbox to avoid Seatbelt conflicts; Multi-directory sessions; gitignore-style .bxignore per-project secret blocking; Hardcoded denies for ~/.ssh, ~/.gnupg, ~/.docker, and sensitive ~/Library paths; Dry-run mode to preview the generated profile
- **Requirements:** macOS; Node >= 22 (Homebrew tap or npm install bx-mac)
- **Limitations:** Filesystem only — no network or process isolation; Allow-first blocklist model — $HOME is scanned at launch; files created after launch are not blocked, and paths outside $HOME are broadly allowed; Relies on deprecated sandbox-exec; single maintainer; Repository archived 2026-08-18; README declares the CLI discontinued in favor of the proprietary BX.app (bx-ai.eu). The npm package still installs and runs, but receives no fixes

_Notes: The only Seatbelt wrapper here that targets whole GUI IDEs rather than CLI agent processes. Weaker guarantee than the deny-first wrappers (fence, hazmat, jailoc, sand): the profile is a launch-time snapshot of $HOME with deny rules, and the README states plainly that this is protection against accidental or misguided file access, not airtight isolation._

<a id="ref-chamber"></a>
### chamber

**Maintainer:** Cirrus Labs · **License:** AGPL-3.0 · [Home](https://github.com/cirruslabs/chamber)

Prefix command that runs Claude Code or Codex inside an ephemeral Tart macOS virtual machine on Apple Virtualization.framework, mounting the current directory and destroying the VM on exit.

- **Isolation:** microvm
- **Capabilities:** macOS guest VM via Tart (Apple Virtualization.framework); Current working directory mounted into the guest; VM destroyed after each run; every session starts from a clean seed image; Automatically appends the agents' permission-skipping flags inside the VM; Seed image initialized from an OCI registry: `chamber init ghcr.io/cirruslabs/macos-sequoia-base:latest`
- **Requirements:** Apple Silicon Mac with Tart installed; Homebrew install
- **Limitations:** Last commit 2025-12; 9 months idle at inclusion; AGPL-3.0 for chamber; Tart dependency is Fair Source (royalty-free only on personal devices and workstations); Only Claude and Codex are named as supported agents; macOS guest images are multi-GB downloads; no network or credential controls documented

_Notes: The only entry sandboxing an agent inside a macOS guest; vibe, shuru, arcbox, and matchlock all run Linux guests on the same Apple Virtualization.framework substrate. That matters for agents that need Xcode or other macOS-only toolchains. Cirrus Labs maintains Tart for CI, and chamber is a thin wrapper over it (45 GitHub stars at inclusion). Idle since 2025-12; treat as a reference design rather than an actively developed tool._

<a id="ref-clampdown"></a>
### clampdown

**Maintainer:** 89luca89 · **License:** GPL-3.0-only · [Home](https://github.com/89luca89/clampdown)

Launcher by the distrobox author that confines Claude Code, Codex, or OpenCode in a zero-capability Podman/Docker container with Landlock, seccomp, iptables egress rules, and OCI hooks that re-apply the same restrictions to nested tool containers.

- **Isolation:** container, landlock, seccomp
- **Capabilities:** Agent container with cap-drop=ALL, read-only rootfs, no-new-privileges, and a seccomp profile blocking about 150 syscalls (io_uring, userfaultfd, BPF, namespace creation, mount); Landlock ruleset applied by sandbox-seal before exec (workdir RW, system dirs RO); Landlock V3 (kernel 6.2+) is a hard requirement; Sidecar-owned iptables egress; agent default-deny with domain allowlist, tool containers default-allow with private CIDRs always blocked; rules changed live with clampdown network; OCI precreate and createRuntime hooks validate every nested podman run against 17 checks and derive Landlock policy from its bind mounts; no opt-out; Auth proxy in a FROM scratch container holds real API keys; the agent receives a dummy sk-proxy key; Sidecar seccomp-notify supervisor with SHA-256 exec allowlist, mount and firewall-modification blocking; Protected workdir paths (.git/hooks, .git/config, .claude, .mcp.json) read-only; .env, .npmrc, .clampdownrc masked; optional inotify tripwire kills the session on tamper; Structured audit log per session (policy PASS/BLOCKED, proxy requests, firewall changes) persisted after container removal
- **Requirements:** Linux kernel 6.2+ with Landlock (6.12+ recommended), natively or inside podman machine or colima; Rootless podman (preferred), Docker, or nerdctl; Go 1.23+ to build; Docker Desktop on macOS unsupported
- **Limitations:** GPL-3.0-only copyleft (COPYING.md), relevant if redistributing; Egress domains resolve to IPs when a rule is applied, so rotating CDN addresses can break allowed hosts or require wider CIDRs; no HTTP path or method scoping; Build from source with make all (five container images); the sidecar runs with 16 capabilities including SYS_ADMIN and NET_ADMIN; Under 100 GitHub stars at inclusion; young project despite the maintainer's distrobox track record

_Notes: Combines what agent-glovebox does with Docker and credential scoping and what nono does with Landlock plus a key proxy, and adds a layer neither has, which is OCI hooks and a sidecar supervisor that apply identical confinement to containers the agent itself spawns for builds and tests. That nested-container enforcement, the FROM scratch sidecar and proxy images, and the seccomp-notify exec allowlist are the distinguishing mechanisms. Written by Luca Di Maio (distrobox); pushes on the day of review._

<a id="ref-clawker"></a>
### clawker

**Maintainer:** schmitthub · **License:** AGPL-3.0-or-later · [Home](https://docs.clawker.dev) · [Repo](https://github.com/schmitthub/clawker)

Go CLI that runs Claude Code or Codex in capability-less Docker containers behind a deny-by-default egress stack of Envoy, a custom CoreDNS, and eBPF cgroup redirection, with domain, path, and method rules enforced via TLS MITM.

- **Isolation:** container
- **Capabilities:** Agent containers run with no Linux capabilities; clawkerd as PID 1 drops to an unprivileged user; eBPF cgroup programs attached from outside the container redirect TCP to Envoy and DNS to CoreDNS; unlisted domains return NXDOMAIN; Per-domain TLS MITM certificates enabling HTTP path- and method-level allow rules and a per-request audit log; Per-host control plane container owning firewall lifecycle, eBPF programs, agent identity registry, and mTLS gRPC to each clawkerd; Live firewall add/remove/refresh, per-agent disable, and timed bypass (clawker firewall bypass 5m); SSH and GPG agent forwarding over muxrpc instead of copying credentials; host proxy relays browser OAuth flows back into the container; Git worktree per agent with .git/hooks and .git/config masked read-only; harness bundles for adding other agent CLIs; Optional OpenTelemetry stack (OTel Collector, OpenSearch, Dashboards, Prometheus) on the same Docker network
- **Requirements:** Docker on macOS or Linux; Homebrew, install script, or Go 1.26+ to build; Docker network with control-plane, Envoy, and CoreDNS containers running alongside agents
- **Limitations:** AGPL-3.0-or-later with a commercial dual license and CLA; network-use clause applies to hosted modifications; Heavy footprint (control plane, Envoy, CoreDNS, eBPF loader, optional four-service monitoring stack) for a local single-user tool; README states early development stage with breaking changes expected, and that Linux is less exercised than macOS; No seccomp, Landlock, or AppArmor confinement inside the container; the README lists syscall filtering as roadmap

_Notes: Occupies the same Docker-wrapper slot as agent-glovebox and clampdown but inverts their emphasis by putting all enforcement at the network edge, with name-based rules matched at request time rather than IPs pinned in iptables (clampdown) and no kernel syscall filtering. The README's comparison table rates competitors including nono, Anthropic sandbox-runtime srt, and Docker Sandboxes, so treat its own column with the usual caution. Solo maintainer, about 50 GitHub stars at inclusion, pushes in the week of review; a Claude Code support plugin ships separately under MIT._

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

<a id="ref-cplt"></a>
### cplt

**Maintainer:** NAV (Norwegian Labour and Welfare Administration) · **License:** MIT · [Home](https://github.com/navikt/cplt)

Single static Rust binary that runs AI coding agent CLIs under OS sandbox primitives — Seatbelt on macOS, Landlock plus seccomp-BPF on Linux — with default-deny credential paths, a domain-filtering egress proxy, and a version-controlled per-repo policy file.

- **Isolation:** seatbelt, landlock, seccomp, user-namespace
- **Capabilities:** Kernel-enforced filesystem, network, and syscall restrictions with no Docker or VM; Runs Copilot CLI, OpenCode, Gemini CLI, Antigravity, Pi, Claude Code, or a plain shell; Default-deny on ~/.ssh, ~/.gnupg, ~/.aws, ~/.kube, .env*, key files, and 15+ credential dirs; Kernel-blocked writes to .git/hooks, .git/config, and .gitmodules (persistence vectors); CONNECT proxy with domain allow/block lists and egress auditing; localhost outbound kernel-blocked; Committed .cplt.toml policy — deny rules auto-apply and only tighten; proposals require developer sign-off via cplt trust accept; Env-var allowlisting (blocks AWS_*, *_TOKEN, *_SECRET); npm postinstall scripts disabled by default; Optional bubblewrap namespace isolation on Linux
- **Requirements:** macOS, or Linux kernel 5.13+ (full network filtering needs 6.7+)
- **Limitations:** Linux enforcement self-described as weaker than macOS; gh/git guard wrappers are soft barriers, not kernel-enforced; Container isolation explicitly out of scope

_Notes: Backed by NAV, Norway's national welfare agency — rare institutional provenance in this space. The differentiator is the governance model: the policy file lives in version control, deny rules can only tighten, and loosening requires an explicit trust-acceptance workflow, making agent policy team-auditable in a way no other wrapper here offers._

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

**Maintainer:** Tusk · **License:** Apache-2.0 · [Home](https://github.com/fencesandbox/fence)

Container-free CLI sandbox using OS-native primitives for network domain allowlisting, filesystem access control, and command deny-lists.

- **Isolation:** seatbelt, user-namespace
- **Capabilities:** macOS sandbox-exec (Seatbelt); Linux bubblewrap + socat for network bridging; Network domain allowlisting; Filesystem access control; Command deny-lists; Built-in templates for Claude Code, Codex, Amp, Gemini CLI, Copilot; Go library for programmatic use
- **Requirements:** macOS or Linux; Homebrew, Nix, or Go install
- **Limitations:** macOS sandbox-exec deprecation risk; Process-level isolation (shared kernel)

_Notes: Lightest-weight option for wrapping agent processes with real isolation — no container runtime needed. Inspired by Anthropic's srt. Built-in agent templates mean zero config for common agents. Well-documented security model and architecture. Moved from the Use-Tusk org to fencesandbox in 2026-08 (old URL redirects). GreyhavenHQ/greywall is a fork adding an allow-by-default observe mode, a live network dashboard, and a learning mode that generates least-privilege profiles from syscall traces; it is not listed separately because the enforcement core is fence's._

<a id="ref-gbash"></a>
### gbash

**Maintainer:** ewhauser · **License:** Apache-2.0 · [Home](https://github.com/ewhauser/gbash)

Pure-Go in-process bash interpreter that executes agent shell scripts against a virtual filesystem and ~90 built-in command implementations, with no fork/exec path to host binaries.

- **Isolation:** process
- **Capabilities:** Registry-backed command resolution — unknown commands exit 127 and never reach host binaries; Virtual in-memory filesystem; host mounts opt-in and read-only under a copy-on-write overlay; Network off by default; allowlist-based HTTP client with redirect revalidation and response-size caps; Execution budgets — command count, loop iterations, glob expansion, substitution depth, output caps; Go library, CLI, JSON-RPC server mode, persistent sessions, and a wasm build
- **Requirements:** Go (library) or single binary
- **Limitations:** Alpha; single maintainer; No kernel boundary — explicitly not hardened against interpreter bugs or DoS beyond the budgets; Host-directory and workspace modes expose real host paths; server mode is unauthenticated (loopback/Unix-socket defaults)

_Notes: The interpreter-level sandbox class of monty, applied to bash — nothing else on the list sandboxes the shell itself. Ships a detailed THREAT_MODEL.md with per-boundary data-flow analysis and a published coreutils-compatibility report; the README is explicit that OS- or process-level isolation should wrap it when containment against interpreter bugs matters._

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

<a id="ref-hull"></a>
### hull

**Maintainer:** Artalis · **License:** AGPL-3.0 · [Home](https://github.com/artalis-io/hull)

Single-binary application runtime executing Lua, QuickJS, and WASM code under manifest-declared capability allowlists enforced by a userspace capability layer plus kernel sandboxes (seccomp-bpf and Landlock, Seatbelt, or pledge/unveil).

- **Isolation:** seccomp, landlock, seatbelt, wasm
- **Capabilities:** Kernel enforcement per platform — seccomp-bpf + Landlock on Linux (violation SIGKILL), deny-default Seatbelt SBPL on macOS, pledge/unveil on OpenBSD and Cosmopolitan APE builds; Manifest-declared allowlists for filesystem paths, outbound hosts, env vars, and DB access; Two-phase sandbox lifecycle (before app load, after manifest resolution); WASM compute modules in WAMR — no WASI, single host call, gas metering, 2 MiB default heap; QuickJS instruction-count gas metering; W^X enforcement; Apps compile to Ed25519-signed static executables with hull verify and JSON audit logging; libhull.a lets native C/Rust/Zig programs link just the sandbox and capability layer
- **Requirements:** Linux, macOS, or OpenBSD (single binary; Cosmopolitan builds run cross-platform)
- **Limitations:** Sandboxes code written for its runtime, not arbitrary processes; Solo maintainer; ~5 months old at inclusion; pre-stable APIs; Security audits are self-authored; dual AGPL-3.0/commercial with copyright-assignment CLA

_Notes: No other entry combines a multi-language app runtime with a process-level kernel sandbox: the wasm-runtime entries isolate only WASM, and the kernel-primitive wrappers (nono, cplt) wrap existing commands rather than providing the runtime. Aimed at running AI-generated application code where the signed manifest is the verifiable capability declaration._

<a id="ref-jailoc"></a>
### jailoc

**Maintainer:** Seznam · **License:** MIT · [Home](https://github.com/seznam/jailoc)

Per-workspace Docker Compose sandbox for OpenCode agents with iptables egress filtering, dropped capabilities, and a DinD sidecar to avoid host socket mounting.

- **Isolation:** container
- **Capabilities:** Per-workspace Docker Compose sandboxes; iptables egress filtering (blocks RFC 1918, link-local, CGNAT by default); UID 1000, dropped capabilities, no_new_privs; DinD sidecar instead of mounting docker.sock; OpenCode agent integration; Renovate-pinned base image
- **Requirements:** Docker; Linux
- **Limitations:** OpenCode-specific defaults (sandboxing model is general); Container isolation only (shared kernel)

_Notes: Backed by Seznam (Czech search engine). Network isolation via iptables allowlist prevents pivot to internal infra. The DinD sidecar approach avoids the common docker.sock mount escape vector._

<a id="ref-landrun"></a>
### landrun

**Maintainer:** Zouuup · **License:** MIT · [Home](https://github.com/Zouuup/landrun)

Go CLI that wraps a single Linux command in a Landlock ruleset with per-path read/write/exec rules and TCP bind/connect port restrictions, without root, containers, or seccomp.

- **Isolation:** landlock
- **Capabilities:** Per-path filesystem rules (--ro, --rox, --rw, --rwx), accepting files or directories; TCP bind and connect restricted to listed ports (Landlock ABI v4, kernel 6.7+); IPC scoping of abstract UNIX sockets and signals on by default (ABI v6+); pathname UNIX socket connect allowlist via --unix (ABI v9+); Landlock denial audit logging flags (ABI v7+); --best-effort degrades to the highest Landlock ABI the running kernel supports; Empty environment by default; --env passes variables individually; --ldd and --add-exec auto-add the target binary and its shared libraries to the exec allowlist; Packaged in Ubuntu (26.04), Debian forky, AUR, and SlackBuilds
- **Requirements:** Linux kernel 5.13+ with Landlock enabled (6.7+ for TCP rules, 6.12+ for IPC scoping); Go 1.24+ to build from source, or a distro package
- **Limitations:** Landlock only; no seccomp syscall filtering, no PID or mount namespaces, no UDP or ICMP control; Not agent-specific; no agent profiles, credential handling, or audit chain, so the caller must compose full path lists by hand; No hostname- or HTTP-level network rules; network control is by TCP port only

_Notes: General-purpose Landlock wrapper (the README positions it as a lighter firejail) rather than an agent tool. It sits between the Landlock LSM entry, which is the raw kernel primitive, and nono, which layers Landlock and seccomp with agent profiles, a credential proxy, and rollback. landrun's value for agent use is a one-line, dependency-free confinement of any command on stock distro kernels, and it is now in Debian and Ubuntu archives. About 2,300 GitHub stars at inclusion; sole maintainer._

<a id="ref-leash"></a>
### Leash

**Maintainer:** StrongDM · **License:** Apache-2.0 · [Home](https://leash.strongdm.ai/) · [Repo](https://github.com/strongdm/leash)

Docker/Podman wrapper from StrongDM that runs a coding agent in a container while a sidecar container observes syscalls and enforces Cedar policies on file, exec, network, and MCP tool-call activity.

- **Isolation:** container
- **Capabilities:** Cedar policies (permit/forbid) transpiled at load time into eBPF LSM rules and HTTP MITM proxy rules; forbid rules block, not just log; Policy actions cover FileOpen (ro/rw), ProcessExec by path, NetworkConnect by host or IP:port, HttpRewrite, and McpCall; MCP observer records and enforces tool calls on supported transports, correlated with file and network telemetry; Full filesystem and network telemetry with a Control UI (localhost:18080) including a Monaco Cedar editor with completion and validation; Live policy updates over HTTP API or the UI without restarting the agent; Default coder image ships claude, codex, gemini, qwen, and opencode; custom images supported; Prompted, remembered decisions on mounting host agent config directories and forwarding provider API keys; Experimental native macOS mode via Endpoint Security and Network Extension system extensions (no container)
- **Requirements:** Docker, Podman, or OrbStack on macOS or Linux (WSL supported); Install via npm (@strongdm/leash), Homebrew cask, or release binary
- **Limitations:** Last commit 2026-04; 5 months idle at inclusion; Starts with a permissive policy; enforcement is opt-in by authoring Cedar rules; McpCall forbid is enforced but permit is informational only (v1); ProcessExec matches by path with no argument filtering; hostname rules require the proxy (kernel enforces IP only); IPv6 literals and CIDR unsupported in v1; Native macOS mode is described by the project as highly experimental and requires approving system extensions and Full Disk Access

_Notes: The Cedar question is settled by docs/design/CEDAR.md, which states policies are transpiled to Leash IR and loaded into eBPF LSM programs and the MITM proxy, so forbid rules deny actions rather than only log them, with the MCP permit exception noted above. Compared with agent-glovebox (Docker plus monitor and credential scoping) Leash's distinguishing pieces are a formal policy language with a linted subset and the MCP tool-call layer; compared with clampdown it enforces via eBPF LSM from a sidecar rather than via Landlock and seccomp inside the agent container. Ships from a commercial vendor (StrongDM) under Apache-2.0 with a binary-distribution disclaimer stating no support or maintenance is provided._

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

<a id="ref-matchlock"></a>
### matchlock

**Maintainer:** Jingkai He (jingkaihe) · **License:** MIT · [Home](https://github.com/jingkaihe/matchlock)

CLI and Go/Python/TypeScript SDKs running agents in ephemeral microVMs (Firecracker on Linux, Virtualization.framework on macOS) with runtime-editable host allow-lists and a MITM proxy that injects secrets the VM never sees.

- **Isolation:** microvm, kvm
- **Capabilities:** Firecracker/KVM backend on Linux; Virtualization.framework backend on Apple Silicon macOS; Network allow-list via --allow-host, editable while the VM runs (`allow-list add/delete`); MITM proxy substitutes real credentials for placeholders on outbound requests; FUSE-backed /workspace overlay mounts that vanish when the sandbox exits; Go, Python, and TypeScript SDKs; Homebrew, .deb, .rpm, and script installers
- **Requirements:** Linux with /dev/kvm or macOS on Apple Silicon; Package or script install
- **Limitations:** README: "Experimental: This project is still in active development and subject to breaking changes"; 497 of ~516 commits by one author at inclusion; effectively a solo-maintained project; Last push 2026-07

_Notes: Closest existing entry is nono (Landlock/seccomp process sandbox with a credential proxy): matchlock moves the same credential-proxy idea into a microVM boundary and adds runtime allow-list edits. Unlike shuru it supports x86_64 Linux hosts via Firecracker, and unlike smolvm it has no portable machine artifact or CoW forking. Roughly 620 GitHub stars (2026-09)._

<a id="ref-mcp-runner"></a>
### mcp-runner

**Maintainer:** Tangier AI (abir-taheer) · **License:** Apache-2.0 · [Home](https://github.com/abir-taheer/mcp-runner)

NestJS service that deploys dockerized MCP servers into gVisor (runsc) containers with dropped capabilities, isolated networks, and unprivileged users, exposing each over Streamable HTTP/SSE including STDIO-only servers.

- **Isolation:** container, gvisor
- **Capabilities:** Every deployment container is created with Runtime runsc; setup.sh installs gVisor and registers it in the Docker daemon; Drops SYS_ADMIN, NET_ADMIN, SYS_PTRACE, SYS_MODULE; no-new-privileges and apparmor docker-default; Per-deployment bridge network with inter-container communication disabled; DNS pinned to 8.8.8.8 and 1.1.1.1; Each container runs as a unique unprivileged Linux user created on the host; Memory and CPU limits and deleteAfterSeconds per deployment via REST API with X-API-Key auth and Swagger docs; Converts STDIO MCP servers to remote Streamable HTTP or SSE endpoints; Full cleanup of containers, networks, users, and logs on deletion
- **Requirements:** Ubuntu 24.04 VM (2 GB RAM minimum) provisioned by setup.sh with Docker and runsc; The runner itself runs as a privileged container with the Docker socket and host /etc mounted
- **Limitations:** Last commit 2025-12 (last push 2026-01); 7 months idle at inclusion; gVisor is required, not optional; the runtime is hardcoded to runsc in container.service.ts and there is no compose file or flag to select another runtime; Deployment containers run with seccomp:unconfined (gVisor filters syscalls instead); the control service needs --privileged, host networking, and docker.sock; Around 30 GitHub stars; single-company project (Tangier AI) with the image published as tangierai/mcp-runner

_Notes: Sandboxes MCP servers rather than the agent, the same target as Kilntainers but with the opposite direction of trust, since here untrusted third-party MCP servers are the workload and the agent connects to them remotely. Nearest listed isolation primitive is gVisor; nearest products are E2B and Modal style hosted runners, which this replaces with a single self-managed VM. The privileged control container and host /etc mount mean the runner host itself is a trusted single-tenant machine._

<a id="ref-microsandbox"></a>
### microsandbox

**Maintainer:** zerocore-ai · **License:** OSS · [Home](https://github.com/superradcompany/microsandbox)

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

_Notes: NVIDIA backing gives visibility. OPA/Rego policy support targets enterprise governance workflows. Announced at GTC 2026. An ecosystem has formed on top of it rather than beside it: NVIDIA/NemoClaw (22k stars) is the agent-facing reference stack that runs OpenClaw, Hermes, and LangChain Deep Agents inside OpenShell sandboxes; lensapp/openshell-k8s-operator exposes OpenShell sandboxes as Kubernetes CRDs over the kubernetes-sigs Agent Sandbox controller; openshift-online/hypershell manages OpenShell gateway fleets across clouds. None adds isolation of its own, so they are noted here rather than listed._

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

<a id="ref-sandlock"></a>
### sandlock

**Maintainer:** multikernel · **License:** Apache-2.0 · [Home](https://github.com/multikernel/sandlock)

Rust process sandbox for Linux combining Landlock, seccomp-BPF, and a seccomp user-notification supervisor to confine agent code with HTTP-level network ACLs and a copy-on-write working directory, without root or containers.

- **Isolation:** landlock, seccomp, process
- **Capabilities:** Landlock filesystem, TCP port, and IPC scoping rules plus a seccomp-BPF deny filter applied before exec; Outbound network allowlist or denylist by host, IP, CIDR, port, and protocol (tcp, udp, icmp), enforced at connect/sendto via seccomp notification; HTTP-level ACLs (method + host + path) through a transparent proxy; HTTPS via an ephemeral CA injected into the trust bundle or a user-supplied CA; Credential injection in the proxy after the ACL check, so the child never holds the API key; Copy-on-write working directory via syscall interception (no mount namespace), with --dry-run to preview file changes and discard them; Port virtualization so multiple sandboxes bind the same port; named sandboxes with ps/inspect/kill; Dynamic policy callbacks (policy_fn) in Python or Rust evaluated at syscall time on execve, connect, bind, and openat; Memory and process-count limits, frozen time and seeded randomness, and an OCI runtime shim (sandlock-oci) for containerd/CRI-O
- **Requirements:** Linux 6.12+ for full features (Landlock ABI v6); 5.13+ for filesystem rules only; Rust 1.70+ to build (cargo install); no root, no cgroups
- **Limitations:** Build from source only; no prebuilt binaries or distro packages documented; Vendor claims ~5 ms startup and ~1,900 COW forks/sec in the README comparison table; not independently measured; Shared host kernel; the README lists a TOCTOU caveat for seccomp-notify and excludes path strings from policy_fn events for that reason; Full network and IPC confinement requires a 6.12+ kernel, newer than many LTS distros ship

_Notes: Closest to nono (Landlock + seccomp, credential proxy) and to Anthropic sandbox-runtime srt (domain proxy), but sandlock adds a seccomp user-notify supervisor that implements the COW filesystem, resource limits, port remapping, and runtime policy callbacks without namespaces, and its HTTP ACL scopes by method and path rather than by domain alone. It also ships Python, Go, and C FFI bindings and an OCI shim, so the same core can back an SDK or a Kubernetes runtime class. Active repository at inclusion (about 1,090 commits, pushes on the day of review); the multikernel org is the maintainer._

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

<a id="ref-shuru"></a>
### shuru

**Maintainer:** superhq-ai · **License:** Apache-2.0 · [Home](https://github.com/superhq-ai/shuru)

Apple Virtualization.framework microVM launcher whose rootfs resets on every run, forwarding ports over vsock without a guest network device and substituting API keys through a host-side credential proxy.

- **Isolation:** microvm
- **Capabilities:** Linux guest on Apple Virtualization.framework (macOS); experimental KVM backend for Linux ARM64; Ephemeral rootfs reset per run; Host-to-guest port forwarding over vsock, working without --allow-net (no guest network device); Disk checkpoints saved and branched across runs; Secrets stay on the host: guest receives a placeholder token; proxy substitutes the real value only on HTTPS requests to specified hosts; CLI, TypeScript SDK (@superhq/shuru), and agent skills for Claude Code, Cursor, and Copilot
- **Requirements:** macOS 14 (Sonoma)+ on Apple Silicon; Homebrew tap or install script
- **Limitations:** Linux builds are "not ready for production use yet" per the README; ARM64 only, x86_64 Linux absent; No Intel Mac support; Only a TypeScript SDK; no Python or Go

_Notes: The placeholder-token credential proxy is the same design as nono's credential proxy and matchlock's MITM injection, applied to a Virtualization.framework VM instead of a process sandbox or Firecracker. Differs from vibe (also Apple VZ) in being ephemeral-by-default with checkpoints rather than a persistent disk image, and in shipping an SDK. Last push 2026-08. Roughly 850 GitHub stars (2026-09)._

<a id="ref-skilllite"></a>
### skilllite

**Maintainer:** EXboys · **License:** MIT · [Home](https://github.com/EXboys/skilllite)

Rust single-binary agent engine with a built-in OS-native sandbox using macOS Seatbelt and Linux bubblewrap/seccomp for skill execution isolation.

- **Isolation:** seatbelt, user-namespace, seccomp
- **Capabilities:** OS-native sandbox (Seatbelt on macOS, bubblewrap + seccomp on Linux); Filesystem, network, and IPC lockdown; Process-exec whitelisting; Resource limits via rlimits; Three-layer defense (install-time scan, pre-exec auth, runtime sandbox); Zero-dependency single binary; Sandbox component usable independently of the agent engine
- **Requirements:** macOS or Linux
- **Limitations:** Early project; Smaller community

_Notes: The skilllite-sandbox component is independently usable — you don't have to use the agent engine to get the sandbox. Three-layer defense model (install scan + pre-exec auth + runtime sandbox) is more depth than most standalone tools offer._

<a id="ref-smolvm"></a>
### smolvm

**Maintainer:** smol machines (@binsquare) · **License:** Apache-2.0 · [Home](https://smolmachines.com) · [Repo](https://github.com/smol-machines/smolvm)

libkrun microVM CLI that packs a stopped Linux VM into a portable .smolmachine file and forks running machines copy-on-write, isolating agent workloads on macOS, Linux, and Windows hosts.

- **Isolation:** microvm
- **Capabilities:** libkrun VMM on Hypervisor.framework (macOS), KVM (Linux), and Windows Hypervisor Platform (Windows); Portable .smolmachine artifact packs a stopped VM's state and pushes to any OCI registry; Copy-on-write fork of a running machine's live RAM and disk state into independent children; Network off by default (opt-in with --net); per-machine host allow-lists; virtio-gpu/Venus (Vulkan) GPU acceleration and CUDA API remoting over vsock from a driverless guest; SSH-agent forwarding so private keys stay on the host; Smolfile declarative machine definition (image, init commands); `smolvm pack` builds self-contained executables
- **Requirements:** macOS 11+ (Apple Silicon or Intel), Linux x86_64/aarch64 with /dev/kvm, or Windows x86_64 with WHP enabled; Single-binary install (curl script; Windows zip bundles krun.dll)
- **Limitations:** CLI-first; no language SDK documented in the README; Vendor claims "sub-second cold start" and "<200ms" boot for packed executables; not independently measured; Windows host support depends on libkrun's WHP backend, which is newer than the macOS/Linux paths; GPU/CUDA remoting is a host-process shim, not passthrough; coverage of the CUDA API is not documented

_Notes: Successor to BinSquare/ERA, whose README now reads "DEPRECATED: Please visit smol machines - smolvm"; same author (@binsquare). Unrelated to CelestoAI/SmolVM (listed here as "SmolVM (Celesto)") despite the name collision. Nearest peer is microsandbox (also libkrun, local-first); smolvm adds the portable .smolmachine artifact, live-state CoW forking for parallel agent runs, and a Windows host backend that microsandbox lacks. Roughly 5.9k GitHub stars at inclusion (2026-09)._

<a id="ref-smolvm-celesto"></a>
### SmolVM (Celesto)

**Maintainer:** CelestoAI · **License:** Apache-2.0 · [Home](https://github.com/CelestoAI/SmolVM)

Python SDK and CLI launching agent sandboxes as microVMs through pluggable VMM backends (Firecracker on Linux, QEMU on macOS, libkrun in source), including Windows 11 guests and a browser sandbox with live view.

- **Isolation:** microvm, kvm
- **Capabilities:** Unified API over Firecracker (Linux/KVM) and QEMU (macOS); libkrun backend present under src/smolvm/runtime/; Windows 11 guests on Linux/KVM hosts with PowerShell execution, file upload, and parallel sandboxes; Browser sandbox exposing a CDP endpoint, a web viewer URL for live watching, and a VNC display URL; Pause/resume snapshots preserving memory, disk, and running processes; Egress restriction via internet_settings.allowed_domains; One-command agent environments: `smolvm claude start`, Codex, and Pi, with git credentials forwarded; Persistent state across sessions
- **Requirements:** Linux with /dev/kvm (full feature set) or macOS (QEMU backend); Python (`pip install smolvm`) or curl install script
- **Limitations:** Host mounts, network controls, and snapshots are Linux-only per the README; Windows guests require a Linux host with KVM; macOS desktop sandbox marked "(preview)"; libkrun backend exists in source but is not documented in the README; treat as unverified

_Notes: Name collision with smol-machines/smolvm (listed as "smolvm"); the two projects share no code or authors. Compared with E2B or Daytona it is local-first with no hosted control plane, and compared with the other local microVM launchers here (smolvm, boxlite, shuru, matchlock) it is the only one offering Windows guests and a built-in browser sandbox with live view. Backend choice per host OS (QEMU on macOS) means macOS runs a full emulator-based VM rather than a microVM; the microvm tier reflects the Linux Firecracker path. Roughly 870 GitHub stars at inclusion (2026-09)._

<a id="ref-temps"></a>
### temps

**Maintainer:** gotempsh (David Viejo) · **License:** Apache-2.0 · [Home](https://github.com/gotempsh/temps)

Self-hosted Rust PaaS whose sandbox subsystem exposes a Vercel-Sandbox-compatible API with hardened Docker containers by default and opt-in Firecracker microVMs.

- **Isolation:** container, microvm, kvm
- **Capabilities:** Vercel Sandbox SDK-compatible API with per-sandbox backend selection; Hardened Docker default (CapDrop=ALL, minimal capability adds); Opt-in Firecracker backend — pinned guest kernel, rootfs built from the OCI image, vsock guest agent, TAP/NAT networking with guest-to-host and cloud-metadata paths dropped; Requesting Firecracker on a non-KVM host fails with 422 rather than silently downgrading; Full PaaS around it — git-push deploys, observability, analytics, email, AI gateway
- **Requirements:** Self-hosted (Rust binary); Linux with /dev/kvm for the Firecracker backend; Docker as the image toolchain
- **Limitations:** Sandboxing is one subsystem of a much larger platform; Firecracker backend ~2 weeks old at inclusion; jailer deferred (VMM runs as the server's user); egress restriction deferred (restricted mode fails closed to no-network); Effectively single-maintainer

_Notes: The only self-hostable entry offering drop-in Vercel Sandbox SDK compatibility on your own hardware. The Firecracker backend is real in-repo code (vsock agent, e2e test, design ADR), not a wrapper over an external sandbox API — but it is weeks old; the Docker path is the battle-tested default._

<a id="ref-vetto"></a>
### vetto

**Maintainer:** shleder · **License:** Apache-2.0 · [Home](https://github.com/shleder/vetto)

Daemon-less Rust single binary that wraps any agent CLI in Landlock, namespaces, and a hand-built seccomp-BPF filter on Linux, or a Seatbelt profile on macOS, with a host-side DNS broker for per-domain network allowlists.

- **Isolation:** landlock, seccomp, user-namespace, seatbelt
- **Capabilities:** Landlock rulesets built via raw syscalls with ABI 1-6 probing, including read-path denial and IPC scoping; Hand-built seccomp-BPF filter blocking non-Unix socket(), mount-family syscalls, and io_uring; User, mount, PID, network, and IPC namespaces without bwrap or root; Network modes off / per-domain allowlist / open; a host-side broker resolves DNS, checks the allowlist and forbidden CIDRs, connects, and passes the socket fd into the sandbox over SCM_RIGHTS; In-project secret paths masked with /dev/null bind mounts or empty tmpfs; PATH shims (vetto enable claude|codex|cursor), Git Guard intercepting destructive git commands, and vetto mcp wrap for third-party MCP servers; Ephemeral run-and-rollback mode, session snapshots and diff review, PTY secret redactor
- **Requirements:** Linux 5.13+ (Landlock) or macOS; cargo install vetto or npm i -g @shledery/vetto
- **Limitations:** Repository created 2026-08 with a single author and no external audit at inclusion; the git history shows ~600 commits in three weeks (renamed from codex-rescue); macOS profile enforces write and network restrictions only; the README attributes missing read denial to an Apple SBPL regression, which conflicts with srt, nono, and fence all denying reads via Seatbelt unprivileged — unverified; Windows backend (Job Objects / AppContainer) is experimental; Bundles a large non-isolation feature set (TUI, reports, token-burn watchdog) alongside the sandbox

_Notes: Author-submitted (PR #62); the isolation code was read before inclusion: landlock.rs, seccomp_netblock.rs, namespaces.rs, and net_relay.rs implement what the README claims. Nearest entries are nono (Landlock+seccomp with a credential proxy and rollback) and srt/fence (bwrap or Seatbelt with an HTTP-level domain proxy). What differs is the network path: the broker connects on the host and hands a connected socket across the boundary, so no resolver or raw socket exists inside the sandbox. No new kernel property — a denser native combination of existing ones, from a very young codebase._

<a id="ref-vibe"></a>
### vibe

**Maintainer:** Kevin Lynagh (lynaghk) · **License:** MIT · [Home](https://github.com/lynaghk/vibe)

Roughly 2000-line Rust CLI booting a Debian VM on macOS through Virtualization.framework, mounting the project directory and agent config dirs so coding agents can run with --yolo inside the guest.

- **Isolation:** microvm
- **Capabilities:** Apple Virtualization.framework Linux guest; ~10 s boot on an M1 MacBook Air per the author; Bundled user-mode networking helper (vibe-usernet, Go); no root or kernel extension; Project directory plus ~/.claude, ~/.codex, ~/.gemini, ~/.pi, and package caches mounted read-write into the guest; Provisioning templates from built-in (@rust, @codex) and custom scripts saved as raw disk images; Per-project persistent instance disk (.vibe/instance.raw) until deleted; Dependencies limited to objc2 interop crates and lexopt
- **Requirements:** ARM-based Mac running macOS 13 (Ventura)+; Single binary from GitHub releases or mise
- **Limitations:** No formal releases or changelog; author recommends pinning to a commit; No network allow-list or credential proxy; agent config directories are mounted read-write, so tokens are visible in the guest; Apple Silicon only

_Notes: Minimalist counterpart to shuru and chamber: same Virtualization.framework substrate, but a persistent disk per project and no secret handling, with the design rationale spelled out in the README (VMs over containers because containers on macOS need a VM anyway). Suited to reading the whole implementation before trusting it. Roughly 950 GitHub stars (2026-09)._

## Self-Hosted Sandbox Platforms

<a id="ref-agentenv"></a>
### AgentENV

**Maintainer:** kvcache-ai (Moonshot AI) · **License:** MIT · [Home](https://kvcache-ai.github.io/AgentENV/latest/) · [Repo](https://github.com/kvcache-ai/AgentENV)

Distributed Firecracker microVM environment platform, built to serve agentic RL training for Kimi K3, with lazy overlaybd image loading, incremental snapshot/fork, and an E2B-compatible HTTP API.

- **Isolation:** microvm, kvm
- **Capabilities:** Firecracker microVMs scheduled across machines; single-node install via script or Docker image; OCI images loaded on demand through overlaybd with local disk as a bounded cache; Incremental memory and filesystem snapshots; running environments fork into independent sandboxes; Snapshots persist to S3-compatible object storage or a shared distributed filesystem; Memory ballooning returns reclaimable guest memory to the host; E2B-compatible HTTP API; standard E2B Python and TypeScript SDKs work by pointing E2B_API_URL at the server; aenv CLI (pull, start, exec, pause, resume, timeout, delete) for Linux and macOS
- **Requirements:** Linux kernel 6.8+ with /dev/kvm on sandbox hosts (a PVM deployment guide covers hosts without KVM); API key generated on first server start; Docker Compose or Kubernetes for cluster deployment
- **Limitations:** Vendor claims from the Kimi K3 tech report: 1.5 million images in production, 9.6x memory overcommit, boot or resume under 50 ms, incremental snapshot under 100 ms; none independently verified; README warns the API authenticates but does not encrypt traffic; HTTPS must be terminated at a reverse proxy; Created 2026-07; open-source release is recent relative to its claimed internal production use

_Notes: Provenance is the kvcache-ai group (KTransformers, Mooncake) at Moonshot AI; the README states it powers Kimi K3 agentic RL training. It is the second open-source E2B-API-compatible Firecracker control plane in this list after E2B's own infra, and unlike Dormice (single machine, gVisor) and k8e (Kubernetes) it targets multi-host clusters with object-storage-backed snapshots. The lazy overlaybd image path and balloon-driven overcommit are the design points that distinguish it from CubeSandbox and forkd, both of which assume images resident on the node._

<a id="ref-arrakis"></a>
### Arrakis

**Maintainer:** abshkbh (Abhishek Bhardwaj) · **License:** AGPL-3.0 · [Home](https://github.com/abshkbh/arrakis)

Self-hosted Cloud Hypervisor microVM sandbox server with overlayfs-protected rootfs, snapshot-and-restore for agent backtracking, and a VNC desktop with Chrome for computer use.

- **Isolation:** microvm, kvm
- **Capabilities:** arrakis-restserver daemon with REST API to start, stop, snapshot, restore, destroy VMs; Go CLI client; Snapshot-and-restore preserves running processes and modified files for backtracking; Each guest runs Ubuntu with a code-execution service and VNC server at boot; Chrome preinstalled; Automatic host port forwarding to guest services including the VNC GUI; Python SDK (py-arrakis) and a separate MCP server repo (arrakis-mcp-server); Dockerfile-based rootfs customization; prebuilt kernel or bring your own; Per-sandbox tap device on a host Linux bridge; ssh into guests
- **Requirements:** Linux host with /dev/kvm (Cloud Hypervisor); GCP setup guide provided; Root to run arrakis-restserver
- **Limitations:** Last commit 2025-06; 15 months idle at inclusion; AGPL-3.0 with a commercial license offered by email; contributors must sign a CLA granting dual licensing; Restored VMs reuse the original IP, so the original must be stopped or destroyed before restoring on the same host; Solo maintainer (239 of 240 commits); guest ships a default ssh password in the rootfs Dockerfile

_Notes: One of the earliest (2024-08) self-hosted microVM sandboxes built specifically around agent backtracking; its snapshot-and-restore predates the fork primitives in forkd, k7 and cocoon sandbox. It pairs a code-execution sandbox with a GUI desktop in one VM, which puts it nearer cua and pixels than E2B. The 15-month gap in commits and the AGPL plus CLA arrangement are the two reasons to prefer an actively maintained alternative for new deployments._

<a id="ref-cocoon-sandbox"></a>
### cocoon sandbox

**Maintainer:** cocoonstack · **License:** AGPL-3.0 · [Home](https://cocoonstack.github.io/sandbox/) · [Repo](https://github.com/cocoonstack/sandbox)

Bare-metal microVM control plane (sandboxd) with an in-guest Rust daemon (silkd) reached over vsock, running Cloud Hypervisor guests from EROFS layers with warm pools, fork, and hibernate.

- **Isolation:** microvm, kvm
- **Capabilities:** Per-node sandboxd with warm pools refilled from golden snapshot exports; memberlist mesh redirects claims to the owning node; silkd in-guest daemon over vsock 2048 provides exec, persistent shell sessions, streaming fs, tar push/pull, watch, pty, structured git, port relay, and an LSP broker; net=none default has no NIC (vsock-only I/O); net=egress attaches a bridge/CNI NIC; Claim, release, hibernate, fork, promote, checkpoint HTTP API; usage and audit journals; /metrics; Guest boots from a PVH ELF kernel and static Rust initramfs mounting EROFS layers under overlayfs with ext4 COW; Go SDK, stdlib-only Python SDK, MCP stdio server, OpenAI Agents SDK provider, LangChain toolkit; Read-only or writable operator-catalog dataset volumes; signed preview URLs
- **Requirements:** Linux bare-metal node with KVM running cocoon (cocoonstack/cocoon, MIT) and Cloud Hypervisor; Go toolchain (or prebuilt sandboxd) for the node; Docker to build boot and OS images
- **Limitations:** Created 2026-07; ~50 stars and two contributors (one with 316 of 321 commits) at inclusion; Vendor claims: warm pool hit 0.2-0.7 ms, golden clone 26-39 ms, cold boot 215-400 ms, measured by the maintainers on a 16-core AMD bare-metal node; docs state nested-virt hosts are much slower; Server stack (sandboxd, silkd, boot chain, OS images, MCP server) is AGPL-3.0; only the client SDKs are Apache-2.0; Node pool retuning is Go-SDK only; Python SDK covers the guest and data-plane surface

_Notes: The vsock-only default is the distinguishing security posture: a sandbox with no network device at all, with every byte relayed through sandboxd, whereas Arrakis, forkd and k7 give each guest a tap or CNI NIC by default. The underlying cocoon engine (Cloud Hypervisor, reflink snapshot and clone, MIT) is a separate repo created 2026-02. Fork and checkpoint branching from LangChain tools overlap Arrakis's snapshot-and-restore backtracking, on a much newer and less adopted codebase._

<a id="ref-containarium"></a>
### Containarium

**Maintainer:** FootprintAI · **License:** Apache-2.0 · [Home](https://containarium.dev) · [Repo](https://github.com/FootprintAI/Containarium)

Self-hostable agent runtime that gives each agent a persistent, SSH-reachable LXC/Incus box with per-tenant network isolation and an in-box MCP server; Kubernetes and LXC backends with GPU passthrough.

- **Isolation:** container
- **Capabilities:** Persistent, SSH-reachable LXC/Incus box per agent; Per-tenant network isolation (agent holds an SSH key, not a kube-apiserver token); Userspace SOCKS5 egress proxy for network policy; MCP-native admin CLI plus a second MCP server running inside the box; Kubernetes and LXC/Incus backends; GPU passthrough; Port exposure to the public internet
- **Requirements:** Linux with LXC/Incus, or Kubernetes; Go 1.25 to build; Self-hosted
- **Limitations:** eBPF egress policy is experimental (under experimental/); the enforced egress path is the SOCKS5 proxy; In-box file-ops sandbox (AGENTBOX_ROOT) is opt-in, default-off; Container isolation (shared kernel)

_Notes: SSH-native per-tenant LXC/Incus boxes; blast radius is bounded by an SSH key rather than a cluster token. Ships two MCP servers (host admin and an in-box shell_exec). The tagline advertises eBPF egress, but that code is experimental — the shipping egress control is a userspace SOCKS5 proxy._

<a id="ref-cubesandbox"></a>
### CubeSandbox

**Maintainer:** Tencent Cloud · **License:** Apache-2.0 · [Home](https://github.com/TencentCloud/CubeSandbox)

Self-hostable microVM sandbox service built on RustVMM and KVM, E2B-SDK-compatible, creating hardware-isolated sandboxes in under 60ms with copy-on-write snapshot, clone, and rollback.

- **Isolation:** microvm, kvm
- **Capabilities:** RustVMM + KVM microVM per sandbox (hardware-level isolation); Sandbox creation <60ms with <5MB memory overhead (vendor benchmarks); E2B-compatible SDK (PyPI cubesandbox); CubeCoW copy-on-write engine — event-level snapshots, instant clone, rollback to any saved state; Credential vault — agents call external APIs while keys never enter the sandbox; Per-sandbox traffic tokens and policy-routing egress; AutoPause/AutoResume for idle sandboxes; Single-node, multi-node cluster, Kubernetes, and Terraform deployment; ARM64 support
- **Requirements:** Linux hosts with KVM; Self-hosted
- **Limitations:** v0.x (first open-source release April 2026); fast-moving surface; License is Tencent's Apache-2.0 variant with third-party carve-outs (SPDX NOASSERTION on GitHub)

_Notes: Missed by keyword discovery despite ~10.9k stars — surfaced while investigating Tencent's managed AGS service, which press coverage says runs on this engine. Combines three properties usually found separately: hardware VM isolation, credential brokering, and sub-second CoW snapshot/rollback — the closest self-hosted analog to mitos's fork model, at much larger scale and with an E2B-compatible API._

<a id="ref-dormice"></a>
### Dormice

**Maintainer:** BitMiracle-AI · **License:** Apache-2.0 · [Home](https://github.com/BitMiracle-AI/Dormice)

Single-machine sandbox daemon running agent sandboxes as Docker containers under gVisor (runsc), with an idle-cooling lifecycle (active, frozen, stopped, S3-archived) and an E2B-compatible API.

- **Isolation:** container, gvisor
- **Capabilities:** acquireSandbox(userKey) is idempotent; the same key returns the same sandbox from any lifecycle state; Lifecycle active to frozen to stopped to archived, with any acquire bringing the sandbox back; Frozen sandboxes suspend processes mid-flight and resume them; memory swapped out via vm.swappiness=100; Optional cold archive to any S3-compatible bucket as tar plus zstd, with restore progress reported on acquire; E2B protocol served on /e2b/api and /e2b/envd; the unmodified official e2b npm package works with two URL changes; TypeScript SDK, dor CLI, web console, and an installable Agent Skill (npx skills add BitMiracle-AI/Dormice); Single daemon with a SQLite ledger; no Kubernetes or external database
- **Requirements:** Bare Ubuntu/Debian x86_64 host with root, Docker, and gVisor runsc; swap enabled with vm.swappiness=100; Node 22+ for the daemon; zstd for archiving
- **Limitations:** README: Status: early development ... Nothing here is ready for production yet; Single-machine only by design; no multi-node scheduling; E2B template builds (e2b template build) are not implemented; templates are Docker images registered with dor template add; Network hardening (blocking the cloud metadata range, disabling inter-container traffic) is left to the operator; the README calls it not optional

_Notes: Created 2026-07 with one primary committer (182 of 197 commits). The design inverts the disposable-sandbox model of E2B, Daytona and Modal: sandboxes are permanent and get cheaper the longer they idle, which suits one resident agent per user. Compared with AgentENV and k8e, the other E2B-API-compatible self-hosted entries, Dormice uses gVisor containers rather than microVMs and runs on one box; the README's measured figures (freeze to ~5 MiB RSS, ~50 ms wake) are the maintainers' own._

<a id="ref-forkd"></a>
### forkd

**Maintainer:** deeplethe · **License:** Apache-2.0 · [Home](https://github.com/deeplethe/forkd)

Firecracker fork server that spawns child microVMs from a paused, warmed parent snapshot via MAP_PRIVATE kernel copy-on-write, for fan-out of KVM-isolated agent sandboxes.

- **Isolation:** microvm, kvm
- **Capabilities:** Children mmap the parent memory image MAP_PRIVATE; pages are shared until written; BRANCH pauses a running sandbox, snapshots in-flight state, and forks it mid-execution (Diff and v0.4 live modes); Diff-snapshot chains with parent_tag and content-hash edges; snapshot-compact flattens a chain; Per-child network namespace, cgroup v2 memory.max, vmgenid-reseeded /dev/urandom; REST API with bearer-token auth, Python and TypeScript SDKs, MCP server (pip install forkd-mcp); Prometheus /metrics, append-only JSON audit log, systemd unit; Snapshot Hub registry for pulling prebuilt portable snapshots
- **Requirements:** x86_64 Linux with KVM (Ubuntu 22.04 or newer); cgroup v2; Live BRANCH: Linux >= 5.7 with vm.unprivileged_userfaultfd=1 (or CAP_SYS_PTRACE) and the vendored deeplethe/firecracker fork; Root (sudo) for fork and network setup
- **Limitations:** Vendor claims: 100 microVMs forked in 101 ms wall-clock and live BRANCH pause window of 56 ms p50 on a 1.5 GiB source; measured by the maintainers on their own host, not independently reproduced; Diff-snapshot chains add a per-link spawn cost the maintainers measure at roughly 450-700 ms per layer on a 512 MiB base (SHA-256 verification); flat spawn is 59 ms; Snapshots are not portable across Firecracker versions or host CPU microarchitectures; live BRANCH requires a patched Firecracker rather than upstream; CLI daemon-side spawn and live BRANCH do not yet compose (README cites issue 209); default branch is dev

_Notes: Created 2026-05; two primary committers account for nearly all commits. The distinguishing primitive is fork-from-warm at the VMM level: Modal offers the same primitive as a closed service, and CubeSandbox and Firecracker itself offer only cold boot. Compared with microsandbox (libkrun, local-first) and agent-glovebox (Docker sbx microVM), forkd targets many short-lived children sharing one warmed parent rather than one long-lived sandbox per user. The README publishes its own comparison benchmark against CubeSandbox, OpenSandbox, gVisor and Docker; treat all figures as vendor-run._

<a id="ref-judge0"></a>
### Judge0

**Maintainer:** Herman Zvonimir Dosilovic (judge0) · **License:** GPL-3.0 · [Home](https://judge0.com) · [Repo](https://github.com/judge0/judge0)

Self-hostable online code-execution system running each submission under ioi/isolate (namespaces plus cgroups) inside Docker worker containers, behind a queued REST API supporting 90+ languages.

- **Isolation:** container, user-namespace
- **Capabilities:** HTTP JSON API for submissions with configurable time, memory, and output limits; webhooks on completion; ioi/isolate sandbox per submission with limits set through judge0.conf; Network access per submission disabled by default and toggleable (ENABLE_NETWORK, ALLOW_ENABLE_NETWORK); Multi-file program (project) submissions and additional files alongside the user program; Docker Compose deployment with PostgreSQL and Redis; official Python SDK (pip install judge0); Hosted Judge0 Cloud available via RapidAPI or direct contract
- **Requirements:** Linux host with Docker and Docker Compose; README recommends Ubuntu 22.04 with systemd.unified_cgroup_hierarchy=0 (cgroup v1)
- **Limitations:** CHANGELOG v1.13.1 (2024-04) fixes three sandbox vulnerabilities in versions <= 1.13.0, CVE-2024-28185, CVE-2024-28189 (symlink handling) and CVE-2024-29021; Last tagged release v1.13.1 dated 2024-04-18; commits continue through 2026-08 but no release has shipped since; Isolation is namespaces plus cgroups on a shared host kernel, weaker than the microVM entries; the deployment requires legacy cgroup v1; Self-hosted instances collect telemetry by default (TELEMETRY.md)

_Notes: Judge0 predates the agent-sandbox category (2017) as an online-judge backend and now markets itself for AI-generated code; the README lists many educational and interview platforms as adopters. MCP servers exist only as community projects, not in the judge0 org. Its nearest entries are llm-sandbox (Docker/Podman per snippet) and nsjail-style process isolation; unlike both it ships a queue, database, and multi-language compiler image as a complete service._

<a id="ref-k7"></a>
### k7

**Maintainer:** Katakate · **License:** Apache-2.0 · [Home](https://docs.katakate.org) · [Repo](https://github.com/Katakate/k7)

Self-hosted K3s-based platform provisioning lightweight VM sandboxes through three switchable backends (Kata+Firecracker, Kata+QEMU, custom k7d VMM) with CLI, REST API, and Python SDK.

- **Isolation:** kata, microvm, kvm
- **Capabilities:** Backends selectable per sandbox with k7 create --backend kfd|kql|k7d; k7 install provisions K3s, Kata, Firecracker+jailer, QEMU, Longhorn, k7d; k7d backend forks a running sandbox's disk and memory copy-on-write (k7 fork) and pauses/resumes VMs in place; kql backend stores root disks on replicated Longhorn PVCs with named snapshots, restore, and cross-node mobility; Cilium CNI with FQDN egress policies; per-sandbox egress_whitelist in k7.yaml; Docker build/run inside sandboxes via a docker sidecar on all three backends; Multi-node clustering through Ansible inventories (2-node and 3-node HA shapes); REST API (Docker Compose) and pip install k7-sdk sync/async client
- **Requirements:** Ubuntu host (amd64 or arm64; k7d is amd64 only) with /dev/kvm; kfd needs a spare raw disk for the devmapper thin-pool; Ansible for the installer; Docker and Docker Compose for the API
- **Limitations:** README: Katakate is currently in beta and under security review. Use with caution for highly sensitive workloads; Vendor claims: k7d VM CoW fork in ~5 ms at the VMM and ~2.4 s end-to-end to a Ready pod; kql fork 46.7 s; measured by the maintainer on one Hetzner AX41 node; Installation may overwrite existing K3s, Kata, Firecracker, QEMU/Kata, or Longhorn installations on the node; Single primary committer (26 of 29 contributions)

_Notes: Reached number one on Show HN in 2025-10. It sits between kubernetes-sigs Agent Sandbox (CRDs only, bring your own cluster) and netclode (a fixed Kata+Cloud Hypervisor stack for coding agents): k7 installs the cluster itself and lets the operator pick the VMM per sandbox. The k7d backend (separate Katakate/k7d repo) is a custom KVM VMM added for warm fork, the same primitive forkd builds on Firecracker; k7 wraps it in a containerd shim so Kubernetes still schedules the sandbox._

<a id="ref-opensandbox"></a>
### OpenSandbox

**Maintainer:** Alibaba · **License:** Apache-2.0 · [Home](https://github.com/opensandbox-group/OpenSandbox)

Universal sandbox for AI apps with multi-language SDKs, Docker + K8s runtimes, covering coding agents, GUI agents, evaluation, and RL training.

- **Isolation:** container
- **Capabilities:** Multi-language SDKs (Python/Java/JS/C#/Go planned); Unified API; Dual runtime (Docker for dev, K8s for prod); Evaluation and RL training support
- **Requirements:** Docker or Kubernetes; Self-hosted
- **Limitations:** Very new (created December 2025)

_Notes: Broadest scope of any sandbox — covers evaluation and RL training environments, not just agent sandboxing._

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

<a id="ref-dam"></a>
### DAM

**Maintainer:** dam-agents (IBM) · **License:** Apache-2.0 · [Home](https://github.com/dam-agents/dam)

Self-hostable Kubernetes platform for running headless coding-agent harnesses, each in an isolated pod with deny-all-egress NetworkPolicy, pod SecurityContextConstraints, a policy-enforced access gateway, and zero-trust credential injection.

- **Isolation:** container
- **Capabilities:** Isolated Kubernetes pod per agent; Deny-all egress NetworkPolicy per agent; OpenShift SecurityContextConstraints (pod hardening); Policy-enforced gateway for all agent access; Zero-trust credential injection (credentials never exposed to the runtime); CRDs (agents/forks/runs) with an operator; Web UI, CLI, Slack, and scheduled triggers; ACP-compatible bring-your-own harness (Claude Code, Pi, Bob, Codex)
- **Requirements:** Kubernetes (Helm chart); Self-hosted (a hosted option is waitlist-gated)
- **Limitations:** Very new (~2 months, 10 stars at inclusion); Hosted service is waitlist-gated

_Notes: Brings a credential proxy plus a policy-enforced egress gateway to the Kubernetes tier — most k8s sandbox entries isolate pods but do not proxy credentials. IBM-backed (ibm.biz docs; the bundled "Bob" harness targets IBM workflows). Runs any ACP-compatible harness, not just the bundled ones._

<a id="ref-gke-agent-sandbox"></a>
### GKE Agent Sandbox

**Maintainer:** Google Cloud · **License:** Closed source · [Home](https://cloud.google.com)

Managed Kubernetes service for AI code isolation on GKE using gVisor and kubernetes-sigs/agent-sandbox.

- **Isolation:** gvisor, kata
- **Capabilities:** Managed gVisor/Kata runtime; GKE integration; Warm pools; Persistent storage; Cloud IAM
- **Requirements:** Google Cloud account; GKE cluster
- **Limitations:** GKE-only; Vendor lock-in

_Notes: Managed wrapper around the open-source agent-sandbox project. If you're already on GKE, this is the path of least resistance._

<a id="ref-k8e"></a>
### k8e

**Maintainer:** xiaods (Deshi Xiao) · **License:** Apache-2.0 · [Home](https://k8e.sh) · [Repo](https://github.com/xiaods/k8e)

Single-binary Kubernetes distribution built on K3s components that adds a sandbox gateway, warm pod pools, snapshots, and Cilium egress policy for agent sessions under gVisor, Kata, or Firecracker runtime classes.

- **Isolation:** gvisor, kata, container
- **Capabilities:** Sandbox gateway over gRPC with mTLS plus an E2B-compatible HTTP surface (pkg/sandbox/e2b) for sessions, exec, files, PTY terminals, expose, and snapshots; Auto-detects installed runsc, Kata, or firecracker-containerd shims and registers RuntimeClasses; gVisor is the recommended default; Warm pool of pre-booted sandbox pods with adaptive sizing; Content-addressed snapshots (SHA-256 layerstore, zstd, incremental restore, server-side registry); Per-session Cilium toFQDNs egress policy and live allow-hosts changes; k8e-sandbox-cli standalone binary for Linux, macOS, Windows that installs a /k8e-sandbox skill into Claude Code, Codex, and Pi; Prometheus metrics, NDJSON event stream, file-backed exec transcripts
- **Requirements:** Linux host (x86_64, ARM64, RISC-V); gVisor runsc for the default runtime, nested virt or bare metal for Kata, /dev/kvm for Firecracker; API key created on the server with k8e sandbox-apikey create
- **Limitations:** Solo maintainer (1586 of ~1660 commits); the sandbox layer is recent relative to the 2020 repo; Vendor claims: sub-500ms warm-pool claims and per-runtime boot times (gVisor ~10 ms, Kata ~500 ms, Firecracker ~125 ms) are README figures without published methodology; Firecracker setup is manual (firecracker-containerd shim, devmapper snapshotter, kernel and rootfs placed by hand); go.mod replaces containerd, cadvisor, and cri-dockerd with k3s-io forks, so it tracks K3s upstream rather than vanilla Kubernetes

_Notes: k8e differs from kubernetes-sigs Agent Sandbox in that it is the cluster: one binary installs K3s, containerd, the runtime classes, and the gateway, whereas Agent Sandbox is a set of CRDs and controllers you add to an existing cluster (k8e states it is compatible with them). Against OpenSandbox and AgentScope Runtime it is closer to E2B's surface, since the official E2B SDKs are the intended client. The repository began in 2020 as a K3s-inspired distribution and was rebranded to the agent-sandbox use case; adoption signals for the sandbox features specifically are thin._

<a id="ref-mitos"></a>
### mitos

**Maintainer:** mitos-run · **License:** Apache-2.0 · [Home](https://github.com/mitos-run/mitos)

Kubernetes-native runtime that gives each agent a Firecracker microVM and live copy-on-write forks a running VM into N siblings in tens of milliseconds, with durable versioned workspaces and declarative CRDs.

- **Isolation:** microvm, kvm
- **Capabilities:** Firecracker microVM per agent (KVM hardware isolation); Live copy-on-write fork of a running VM into N siblings (tens of ms); Restore from memory snapshots in milliseconds; Durable, versioned workspaces; Declarative CRDs with a Kubernetes operator; KVM device-plugin for scheduling microVMs; Go SDK
- **Requirements:** Kubernetes; Nodes with KVM (bare-metal or nested virtualization); Self-hosted
- **Limitations:** Very new (created May 2026); prerelease tags; Alpha — features split across "husk" and "engine" paths mid-migration; Linux/KVM only

_Notes: Distinct from raw Firecracker (already listed): a live copy-on-write fork of a warm, running microVM plus a Kubernetes operator, CRDs, and a KVM device-plugin. Fast memory-snapshot restore suits parallel agent exploration and RL-style environment resets._

<a id="ref-netclode"></a>
### netclode

**Maintainer:** angristan (Stanislas Lange) · **License:** OSS · [Home](https://github.com/angristan/netclode)

Self-hosted coding-agent service running each Claude Code, Codex, Copilot, or OpenCode session in a Kata Containers microVM on Cloud Hypervisor under k3s, with a native iOS and macOS client.

- **Isolation:** kata, microvm
- **Capabilities:** Warm pool of pre-booted Kata VMs claimed per session; default 4 vCPU and 4 GB RAM per VM; JuiceFS on S3 (Redis metadata) holds workspace, Docker data, and SDK session; pause deletes the VM and resume remounts the storage; Secret proxy outside the sandbox injects API keys for allowed hosts so keys never enter the VM; Tailscale operator for ingress, preview URLs, and port forwarding; Kubernetes NetworkPolicy for sandbox egress; Auto-snapshots after each turn with rollback of workspace and chat to any prior point; GitHub App integration with per-repo scoped tokens and an @mention bot for PRs and issues; Optional local inference via Ollama; Docker available inside the VM
- **Requirements:** Linux VPS or server with nested virtualization (README lists DigitalOcean and Vultr as working, Hetzner Cloud not); k3s provisioned by the included Ansible playbooks; S3 bucket, Tailscale OAuth, and LLM API keys
- **Limitations:** No LICENSE file (all rights reserved by default); Solo maintainer (833 of 898 non-bot commits); built as a personal tool per the README; Native client is SwiftUI targeting iOS 26 and macOS; no web client; JuiceFS over S3 has low small-file IOPS without the documented writeback and virtiofs caching

_Notes: netclode is an end-to-end product (control plane, agent runner, bot, mobile app) rather than a sandbox primitive, so it compares with Fly Sprites or a self-hosted Claude Code web rather than with Kata or k7 directly. Its secret proxy applies the same idea as nono's credential proxy and Anthropic sandbox-runtime's domain proxy at the cluster edge. The missing license means the code can be read but not legally redistributed or modified without the author's permission._

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

<a id="ref-arcbox"></a>
### arcbox

**Maintainer:** arcboxlabs · **License:** MIT OR Apache-2.0 · [Home](https://arcbox.dev) · [Repo](https://github.com/arcboxlabs/arcbox)

Rust container and VM runtime for macOS that exposes a Docker-compatible socket, runs k3s and Linux/macOS guests, and boots disposable agent sandboxes as Firecracker microVMs nested inside a Hypervisor.framework VM.

- **Isolation:** microvm, kvm
- **Capabilities:** Docker-compatible socket proxied to a guest dockerd; Docker CLI and Compose files unchanged; Local k3s cluster managed by the daemon with kubectl host integration; `abctl claude` builds a sandbox from a built-in template and attaches the terminal to Claude Code; Sandbox snapshots (checkpoint/restore) to skip cold boot; Firecracker microVMs nested inside the Linux guest for disposable agent sandboxes; x86-64 binaries translated inside the guest by FEX; macOS guest VMs cloned copy-on-write for throwaway instances
- **Requirements:** Apple Silicon Mac; sandboxes need M3 or newer with macOS 15+ (nested virtualization); Homebrew or install script (get.arcbox.dev); Rust 1.96+ to build
- **Limitations:** "In public beta" per the README; Sandbox feature requires nested virtualization (M3+, macOS 15+), excluding M1/M2 hosts; Vendor claims "Cold boot <1.5 s" and "Warm boot <500 ms"; not independently measured; macOS guests require APFS storage

_Notes: Broader than a sandbox: an OrbStack-style Docker/Kubernetes/VM runtime for macOS with agent sandboxing as one subsystem, which is why it sits under dev-environment rather than standalone. The nested Firecracker-in-Hypervisor.framework design is unique among the macOS entries here (vibe, shuru, chamber all run a single VZ layer). Compare Docker Sandboxes (listed), which also wraps agents in a Docker-adjacent microVM but without k3s or macOS guests. Roughly 2.9k GitHub stars (2026-09)._

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

<a id="ref-kilntainers"></a>
### Kilntainers

**Maintainer:** Kiln AI · **License:** MIT · [Home](https://github.com/Kiln-AI/Kilntainers)

Python MCP server exposing one sandbox_exec tool that gives each MCP connection its own ephemeral Linux sandbox on Docker/Podman, Modal, E2B, or a WASM (go-busybox) backend.

- **Isolation:** container, microvm, wasm
- **Capabilities:** One sandbox per MCP connection, created on first sandbox_exec and destroyed when the connection closes; Backends selectable by flag (--backend docker|e2b|modal|go_busybox|wasm); any OCI image for Docker/Podman, GPU and region options on Modal; stdio transport for a single local sandbox or HTTP transport hosting many sandboxes with idle session timeout; Network disabled in sandboxes by default (--network to enable); per-exec timeout and 2 MiB output cap; Docker CPU and memory limits and passthrough of extra docker run flags; remote Docker host via --docker-host; WASM backends with memory cap and instruction fuel limit; Agent runs outside the sandbox and reaches it only over MCP, so agent API keys and prompts never enter it
- **Requirements:** Python 3.13+ (uv tool install kilntainers); Docker or Podman for the default backend; Modal or E2B account for cloud backends
- **Limitations:** Last commit 2026-03; 6 months idle at inclusion; WASM backend is go-busybox only (grep, awk, sed, and similar), marked experimental, and is not a full Linux environment; Isolation strength is whatever the chosen backend provides; the Docker backend adds no gVisor, seccomp, or capability hardening beyond docker run defaults; Single tool surface (shell exec); no file transfer, port exposure, or snapshot API

_Notes: The agent talks to the sandbox over MCP rather than running inside it, which places Kilntainers beside llm-sandbox and the E2B/Modal SDKs as a code-execution abstraction, not beside the agent wrappers such as nono or Docker Sandboxes. Compared with llm-sandbox it is protocol-level (any MCP client, not a Python API) and adds Modal, E2B, and WASM backends behind one flag. Backed by Kiln AI as a companion to their Kiln product; about 50 GitHub stars at inclusion._

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

<a id="ref-cloud-hypervisor"></a>
#### Cloud Hypervisor

**Maintainer:** Cloud Hypervisor project (Linux Foundation; Intel, Microsoft, Arm, and others) · **License:** Apache-2.0 AND BSD-3-Clause · [Home](https://www.cloudhypervisor.org) · [Repo](https://github.com/cloud-hypervisor/cloud-hypervisor)

Rust VMM on KVM and Microsoft Hypervisor built from rust-vmm crates, with paravirtualized-only devices, CPU/memory/PCI hotplug, live migration, and snapshot/restore for Linux and Windows guests.

- **Isolation:** kvm
- **Capabilities:** Runs on KVM (Linux) and Microsoft Hypervisor (MSHV); x86-64 and AArch64, experimental riscv64; 64-bit Linux and Windows 10 / Windows Server 2019 guests; Hotplug of CPUs, memory, PCI, VFIO passthrough devices, and virtio-{net,block,pmem,fs,vsock}; Machine-to-machine live migration; Snapshot/restore of a running VM; vhost-user device offload; paravirtualized devices only, no legacy device emulation; REST API and OpenAPI spec for VM lifecycle control
- **Requirements:** Linux host with /dev/kvm, or Windows/Linux host with MSHV; Build your own orchestration; consumed as a VMM binary or via a wrapper project
- **Limitations:** Snapshot/restore and live migration not supported across different Cloud Hypervisor versions; No agent-facing features of its own; a substrate for other tools; Windows guest support narrower than Linux (Windows 10 / Server 2019 named); Docs licensed CC-BY-4.0 under REUSE alongside the Apache-2.0 / BSD-3-Clause code

_Notes: Alternative to Firecracker (listed) with a broader device model (VFIO passthrough, PCI hotplug, Windows guests, live migration) at the cost of a larger footprint; Kata (listed) supports it as one of its VMM backends. It is the VMM underneath arrakis, cocoonstack/sandbox, and netclode, all being added alongside this entry. Roughly 6.2k GitHub stars (2026-09); actively developed with pushes the day of inclusion._

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

<a id="ref-amla-sandbox"></a>
#### Amla Sandbox

**Maintainer:** Amla Labs · **License:** MIT AND (AGPL-3.0-or-later OR BUSL-1.1) · [Home](https://github.com/amlalabs/amla-sandbox)

Python package running agent-written JavaScript and shell inside a bundled Rust WASM/WASI runtime where every tool call is checked against explicit capability grants and a parameter-constraint DSL.

- **Isolation:** wasm
- **Capabilities:** pip install amla-sandbox ships the runtime as amla_sandbox.wasm; README states no Docker or VM required; Guest languages JavaScript and shell (language="javascript" / "shell"); Tools are host Python functions exposed only when passed to the sandbox; the guest can call nothing else; ToolCallCap grants match method patterns (e.g. stripe/charges/*) and carry a ConstraintSet DSL such as Param("amount") <= 10000 or Param("currency").is_in([...]); Constraints can also bound call frequency; Sandboxed virtual filesystem; no network access; no shell escape; Integration modules for LangGraph and CodeAct-style agents plus an audit module in the package source
- **Requirements:** Python 3 host with the amla-sandbox package
- **Limitations:** Python package is MIT; the bundled Rust runtime is "AGPL-3.0-or-later OR BUSL-1.1" (README); the amla-sandbox-core repo has no LICENSE file detected by GitHub; Release mirror of a monorepo; README warns pull requests here are clobbered on the next release; Last commit 2026-05; about 3.5 months idle at inclusion (v0.2.8 on 2026-05-15); No Python guest execution documented; only JavaScript and shell examples

_Notes: Inverts the Wassette model: there the tools are compiled to Wasm and the agent calls them; here the agent's own code runs in Wasm and tools stay as host Python functions gated by per-call constraints. Capsule and Eryx bound resources (fuel, memory, files, hosts); Amla's distinctive control is authorization of individual tool arguments. Around 345 stars; the docs directory contains a research report rather than reference docs._

<a id="ref-capsule"></a>
#### Capsule

**Maintainer:** Capsule (capsulerun) · **License:** Apache-2.0 · [Home](https://github.com/capsulerun/capsule)

CLI and SDK that compile Python or TypeScript/JavaScript tasks to WebAssembly and run them on Wasmtime/WASI under CPU-fuel, memory and timeout limits with filesystem and domain allowlists.

- **Isolation:** wasm
- **Capabilities:** Compiles Python 3.13+ and TypeScript/JavaScript (Node.js 22+, npm packages and ES modules) to Wasm modules run on Wasmtime with WASI; CPU limited by Wasmtime fuel metering with LOW/MEDIUM/HIGH presets or a custom value; Per-task memory cap (e.g. 512MB, 2GB) and timeout (e.g. 30s, 5m); optional automatic retries; Filesystem access only to directories in allowed_files, each read-only or read-write; Network access only to domains in allowed_hosts; default is none; Environment variables passed only if listed in env_variables; capsule build precompiles to .wasm/.cwasm so execution skips the compiler; Installable via pip (capsule-run) or npm (@capsule-run/cli); host-side run() API in Python
- **Requirements:** Python 3.13+ and/or Node.js 22+ on the host; Rust toolchain only when building from source
- **Limitations:** Python packages with C extensions need a wasm32-wasi wheel; README states numpy and pandas do not work inside the sandbox; Running .py/.ts source directly adds "a few seconds" of compile latency on first call (README); sub-second start requires a precompiled artifact; Last commit 2026-06; about 2.5 months idle at inclusion, small project (~300 stars)

_Notes: Sits between Wasmtime (a bare runtime with no language toolchain) and Wassette (MCP-served Wasm components you must compile yourself): Capsule bundles the Python and JS-to-Wasm compilers and a per-task policy of files, hosts, env, fuel, memory and timeout. Unlike Pyodide it runs server-side on Wasmtime with fuel metering rather than in a browser. Maintained by a small French team; PyPI at 0.8.x._

<a id="ref-eryx"></a>
#### Eryx

**Maintainer:** Ben Sully (eryx-org) · **License:** MIT OR Apache-2.0 · [Home](https://docs.eryx.run) · [Repo](https://github.com/eryx-org/eryx)

Wasmtime sandbox embedding full CPython 3.14 compiled to WASI, with memory, CPU-fuel and timeout limits, no filesystem or network by default, and host-controlled async callbacks for permitted access.

- **Isolation:** wasm
- **Capabilities:** Full CPython 3.14 (componentize-py WASI build), so the standard library and pure-Python wheels run unmodified; Configurable memory caps, CPU fuel limits and execution timeouts; Isolated virtual filesystem by default with opt-in read-only or read-write host directory mounts; Networking disabled by default; opt-in TCP/TLS with host allowlists, blocklists and connection limits, plus secret substitution only in HTTP requests to authorized hosts; Host callbacks exposed as awaitable Python async functions; concurrent calls via asyncio.gather; Session state persists across executions; dill-based state snapshots for capture and restore; SandboxPool with min/max size, pre-warming and idle eviction; preinit feature captures initialized memory for faster creation; Bindings for Python (pyeryx on PyPI), JavaScript (@bsull/eryx on npm) and Rust (eryx crate); loads .whl/.tar.gz packages including WASI-compiled native extensions
- **Requirements:** Python, Node.js or Rust host toolchain for the respective binding
- **Limitations:** Native extension support (e.g. numpy via late-linking) is marked experimental in the README feature table; No default values for memory, fuel or timeout are documented; you must choose them; Single primary maintainer (473 of roughly 600 commits by one author; the rest are dependency bots); "Used in production at Grafana" is a README self-statement; the maintainer lists Grafana Labs as employer on GitHub, but Grafana has not been asked to confirm

_Notes: Closest in spirit to monty and Pyodide but different from both: monty is a Rust reimplementation of a Python subset, Pyodide is CPython-in-Wasm aimed at browsers, while Eryx runs the real CPython 3.14 on server-side Wasmtime with fuel metering, host-policed sockets and an async callback bridge. Compared with Capsule it offers no JavaScript guest and no CLI, but adds sessions, snapshots and pooling for REPL-style agent loops. Dual MIT and Apache-2.0 license files are present. PyPI 0.6.0; pushed 2026-09._

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

