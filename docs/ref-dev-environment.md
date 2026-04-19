# Development Environments

[Back to main guide](../README.md)

<a id="ref-coder"></a>
## Coder

**Maintainer:** Coder · **License:** AGPL-3.0 · [Home](https://github.com/coder/coder)

Self-hosted remote development platform with container and VM workspaces, RBAC, and audit logging.

- **Isolation:** container
- **Capabilities:** Self-hosted; Container and VM workspaces; Templates; RBAC; Audit logging
- **Requirements:** Self-hosted on Kubernetes or Docker
- **Limitations:** No agent-specific features; No MCP integration

_Notes: Not agent-specific, but good for teams wanting self-hosted isolation without cloud dependency. AGPL license means modifications must be shared._

<a id="ref-devpod"></a>
## DevPod

**Maintainer:** Loft Labs · **License:** OSS · [Home](https://github.com/loft-sh/devpod)

Client-only tool for reproducible, provider-agnostic dev environments using devcontainer.json.

- **Isolation:** container
- **Capabilities:** Provider-agnostic (Docker/SSH/K8s/cloud); devcontainer.json support; Client-only (no server); Open source
- **Requirements:** Docker or cloud provider
- **Limitations:** No agent-specific features; No MCP integration; No managed service

_Notes: Not agent-specific. Good open-source alternative to Codespaces for local-first workflows where you want reproducible isolated environments._

<a id="ref-github-codespaces"></a>
## GitHub Codespaces

**Maintainer:** GitHub / Microsoft · **License:** Closed source · [Home](https://github.com/features/codespaces)

Cloud-hosted dev environments usable for isolating agent execution in a full Linux VM.

- **Isolation:** container
- **Capabilities:** Full Linux VM; devcontainer.json support; Pre-built images; GitHub integration; Port forwarding
- **Requirements:** GitHub account; Usage-based pricing (free tier available)
- **Limitations:** Not agent-specific; Higher startup latency; Dev tool, not a sandbox service

_Notes: Not purpose-built for agents, but accessible to anyone familiar with GitHub. A "good enough" isolation option for personal agent use without learning new tools._

<a id="ref-koyeb"></a>
## Koyeb

**Maintainer:** Koyeb · **License:** Closed source · [Home](https://www.koyeb.com)

Serverless platform with container-based sandbox capabilities and auto-scaling.

- **Isolation:** container
- **Capabilities:** Container isolation; Auto-scaling; CI/CD integration
- **Requirements:** Cloud-hosted; Usage-based pricing
- **Limitations:** Not agent-specific; General-purpose serverless platform

_Notes: General-purpose serverless platform, not purpose-built for agents, but usable for agent isolation out of the box with standard container workflows._

<a id="ref-ona-formerly-gitpod"></a>
## Ona (formerly Gitpod)

**Maintainer:** Ona · **License:** Closed source · [Home](https://ona.com)

Pivoted from CDE to "mission control for AI agents" with sandboxed dev environments, AI agents, and guardrails.

- **Isolation:** container
- **Capabilities:** API-first environments; devcontainer.json support; OS-level isolation; Ona Agents; Ona Guardrails
- **Requirements:** Cloud-hosted; Enterprise tiers
- **Limitations:** Rapid pivot — product still evolving; Less sandbox API focus than E2B/Daytona

_Notes: Major pivot from Gitpod (rebranded Sept 2025). Demonstrated Claude Code sandbox escape (March 2026). Not agent-specific but increasingly agent-oriented._

