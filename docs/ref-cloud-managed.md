# Cloud Managed Sandboxes

[Back to main guide](../README.md)

<a id="ref-bunnyshell-ai-sandboxes"></a>
## Bunnyshell AI Sandboxes

**Maintainer:** Bunnyshell · **License:** Closed source · [Home](https://www.bunnyshell.com/ai-sandbox-environments/)

Firecracker sandboxes with ~100ms cold starts and MCP Server integration for Claude Code/Cursor/Windsurf.

- **Isolation:** microvm
- **Capabilities:** Firecracker isolation; ~100ms cold starts; Multi-language support; MCP server integration; Snapshots; SDK
- **Requirements:** Cloud-hosted; Paid tiers
- **Limitations:** AI sandbox is a newer product line

_Notes: MCP server integration is notable — direct plugin for Claude Code, Cursor, and Windsurf._

<a id="ref-cloudflare-dynamic-workers"></a>
## Cloudflare Dynamic Workers

**Maintainer:** Cloudflare · **License:** Closed source · [Home](https://developers.cloudflare.com/sandbox/)

V8 isolate-based sandboxing at the edge, claiming 100x faster and more memory-efficient than containers.

- **Isolation:** v8-isolate
- **Capabilities:** V8 isolate isolation; Millisecond startup; MB-level memory per isolate; globalOutbound for HTTP interception; Credential injection without agent visibility
- **Requirements:** Cloudflare Workers paid plan; $0.002/unique Worker/day (waived during beta)
- **Limitations:** JS/TS only (V8 runtime); Not for arbitrary Linux binaries; Weaker isolation than microVMs

_Notes: Unique edge-first approach using V8 isolates instead of containers/VMs. Credential injection without agent visibility is a strong security feature. Open beta early 2026._

<a id="ref-codesandbox-sdk"></a>
## CodeSandbox SDK

**Maintainer:** CodeSandbox · **License:** Closed source · [Home](https://codesandbox.io/sdk)

SDK for giving agents sandboxed MicroVM environments with parallel execution support.

- **Isolation:** microvm
- **Capabilities:** MicroVM isolation; Parallel agent execution; Web-dev environments; File operations; Port forwarding
- **Requirements:** Cloud-hosted; SDK integration
- **Limitations:** Primarily web-dev focused

_Notes: Well-established brand from the browser IDE space, expanding to agent use._

<a id="ref-daytona"></a>
## Daytona

**Maintainer:** Daytona · **License:** Apache-2.0 · [Home](https://www.daytona.io) · [Repo](https://github.com/daytonaio/daytona)

Docker/OCI container-based cloud sandboxes with native state management.

- **Isolation:** container
- **Capabilities:** Docker container isolation; <60ms provisioning; Configurable resources; State management (stop/resume/archive); Python/JS/TS SDKs
- **Requirements:** Cloud-hosted managed service; Usage-based pricing
- **Limitations:** Container-based (shared kernel, weaker isolation than microVMs); Newer platform

_Notes: Pivoted from CDE space (Feb 2025). $31M Series A (Feb 2026). State management (pause/resume) is a key differentiator vs. ephemeral-only platforms._

<a id="ref-e2b"></a>
## E2B

**Maintainer:** E2B · **License:** Apache-2.0 · [Home](https://e2b.dev) · [Repo](https://github.com/e2b-dev/E2B)

Cloud sandbox platform for AI agents using Firecracker microVMs via API/SDK.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVM isolation; ~150ms startup; Filesystem isolation; Network control; Python/JS/TS SDKs; Custom templates
- **Requirements:** Cloud-hosted managed service; Free tier available
- **Limitations:** 24-hour session limit; Cloud-only; Ephemeral by default; No GPU support

_Notes: One of the earliest and most widely adopted agent sandbox platforms. Docker MCP Catalog partnership._

<a id="ref-fly-sprites"></a>
## Fly Sprites

**Maintainer:** Fly.io · **License:** Closed source · [Home](https://sprites.dev)

Persistent Firecracker microVMs for AI agent sessions with 100GB NVMe per sprite.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVM isolation; Persistent 100GB NVMe storage; Checkpoint/restore (~300ms warm); Stateful across sessions; ~$0.07/CPU-hour
- **Requirements:** Cloud-hosted; API access; 1-12s cold start
- **Limitations:** Cold starts slower than E2B; Newer product (Jan 2026)

_Notes: Persistence is the key differentiator — most sandboxes are ephemeral. Checkpoint/restore enables warm resumption of long-running agent sessions._

<a id="ref-modal"></a>
## Modal

**Maintainer:** Modal Labs · **License:** Closed source · [Home](https://modal.com/products/sandboxes)

Serverless cloud platform with sandbox product and best-in-class GPU support.

- **Isolation:** microvm
- **Capabilities:** Sub-second starts; GPU workloads; Network tunnels; Per-sandbox egress policies; 50k+ concurrent sessions
- **Requirements:** Cloud-hosted; Python SDK; Usage-based pricing
- **Limitations:** Closed source; Cloud-only; Python-centric SDK

_Notes: Only major sandbox platform with GPU support — unique differentiator for ML/AI workloads that need compute._

<a id="ref-northflank"></a>
## Northflank

**Maintainer:** Northflank · **License:** Closed source · [Home](https://northflank.com)

Production-grade sandbox infrastructure using Kata Containers and gVisor at 2M+ isolated workloads/month.

- **Isolation:** kata, gvisor
- **Capabilities:** MicroVM via Kata + gVisor; Unlimited session duration; Any OCI image; BYOC (bring your own cloud) deployment; Resource limits; Network controls
- **Requirements:** Cloud-hosted or BYOC; Paid platform
- **Limitations:** Closed source; More complex setup than simpler platforms

_Notes: BYOC option is unusual in this space — most cloud sandboxes are single-provider. Production-proven at scale (2M+ workloads/month)._

<a id="ref-runloop"></a>
## Runloop

**Maintainer:** Runloop · **License:** Closed source · [Home](https://runloop.ai)

Enterprise-grade sandbox infrastructure (Devboxes) with SOC 2 compliance and 10k+ parallel instances.

- **Isolation:** microvm
- **Capabilities:** Blueprints and Snapshots; Isolated cloud dev environments; SOC 2 compliance; High concurrency (10k+ parallel)
- **Requirements:** Cloud-hosted; Enterprise pricing
- **Limitations:** Closed source; Enterprise-focused

_Notes: Enterprise compliance focus (SOC 2) differentiates from developer-oriented alternatives. GA May 2025._

<a id="ref-superserve"></a>
## Superserve

**Maintainer:** superserve-ai · **License:** Apache-2.0 · [Home](https://github.com/superserve-ai/superserve)

Cloud sandbox platform using Firecracker microVMs with TypeScript and Python SDKs.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVM isolation; TypeScript and Python SDKs; Managed cloud service
- **Requirements:** Cloud-hosted (superserve.ai sign-up)
- **Limitations:** Beta; SDK is open source but sandbox backend is private

_Notes: Firecracker-based like E2B. SDK is open source (Apache-2.0) but the sandbox backend infrastructure is in a separate private repo. Beta — evaluate maturity before committing to production use._

<a id="ref-vercel-sandbox"></a>
## Vercel Sandbox

**Maintainer:** Vercel · **License:** Closed source · [Home](https://vercel.com)

Firecracker microVM sandboxes for untrusted code, powering v0's code generation runtime.

- **Isolation:** microvm
- **Capabilities:** Firecracker microVMs; Node.js + Python support; Up to 45min execution; Up to 8 vCPUs / 2GB per vCPU
- **Requirements:** Vercel account; Cloud-hosted
- **Limitations:** Node.js and Python only; 45-minute maximum execution; Tightly coupled to Vercel ecosystem

_Notes: Tightly integrated with Vercel deployment pipeline and v0._

