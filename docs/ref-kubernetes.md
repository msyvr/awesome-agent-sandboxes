# Kubernetes-Native

[Back to main guide](../README.md)

<a id="ref-agent-sandbox-kubernetes-sigs"></a>
## Agent Sandbox (kubernetes-sigs)

**Maintainer:** Kubernetes SIG · **License:** Apache-2.0 · [Home](https://github.com/kubernetes-sigs/agent-sandbox)

Kubernetes CRD and controller for isolated agent workloads with gVisor or Kata runtime and warm pod pools.

- **Isolation:** gvisor, kata
- **Capabilities:** Declarative CRD; gVisor + Kata support; Warm pod pool for <1s cold start; Persistent storage; Stable pod identity
- **Requirements:** Kubernetes cluster; gVisor or Kata runtime
- **Limitations:** Kubernetes required; Still maturing; No standalone mode

_Notes: Official Kubernetes SIG project (launched KubeCon Atlanta Nov 2025). Likely to become the standard for K8s agent sandboxing._

<a id="ref-gke-agent-sandbox"></a>
## GKE Agent Sandbox

**Maintainer:** Google Cloud · **License:** Closed source · [Home](https://cloud.google.com)

Managed Kubernetes service for AI code isolation on GKE using gVisor and kubernetes-sigs/agent-sandbox.

- **Isolation:** gvisor, kata
- **Capabilities:** Managed gVisor/Kata runtime; GKE integration; Warm pools; Persistent storage; Cloud IAM
- **Requirements:** Google Cloud account; GKE cluster
- **Limitations:** GKE-only; Vendor lock-in

_Notes: Managed wrapper around the open-source agent-sandbox project. If you're already on GKE, this is the path of least resistance._

<a id="ref-openkruise-agents"></a>
## openkruise/agents

**Maintainer:** OpenKruise (Alibaba / CNCF) · **License:** Apache-2.0 · [Home](https://github.com/openkruise/agents)

Kubernetes operator for agent sandbox lifecycle management with resource pooling, hibernation, checkpoint/restore, and E2B API compatibility.

- **Isolation:** container
- **Capabilities:** Sandbox pod lifecycle management; Resource pooling; Sandbox hibernation and checkpoint (memory + RW layer + GPU memory); E2B API compatibility on self-hosted K8s; Configurable runtime (container, gVisor, Kata)
- **Requirements:** Kubernetes cluster
- **Limitations:** Early project; Kubernetes required

_Notes: CNCF-affiliated via OpenKruise (Alibaba). The E2B API compatibility is notable — lets you use existing E2B SDK integrations against self-hosted K8s instead of E2B's cloud. Sandbox hibernation with GPU memory checkpoint is unusual._

<a id="ref-sandbox0"></a>
## sandbox0

**Maintainer:** sandbox0-ai · **License:** Apache-2.0 · [Home](https://github.com/sandbox0-ai/sandbox0)

Kubernetes-native agent sandbox platform with warm pod pools, JuiceFS persistent storage, network policy enforcement, and in-pod process manager.

- **Isolation:** container, gvisor
- **Capabilities:** Warm pod pools; JuiceFS persistent storage; Configurable runtimeClass (gVisor/Kata); L4/L7 network enforcement via dedicated netd daemon; Egress auth proxy (credential injection outside sandbox); procd in-pod process manager (PID 1) with REPL session management
- **Requirements:** Kubernetes cluster; Self-hosted
- **Limitations:** Early project; Small community

_Notes: The procd process manager inside pods provides REPL session management — unusual for a K8s sandbox. Egress credential injection keeps secrets outside the sandbox boundary, similar to nono's credential proxy model but at the K8s level._

<a id="ref-treadstone"></a>
## treadstone

**Maintainer:** earayu · **License:** Apache-2.0 · [Home](https://github.com/earayu/treadstone)

Self-hostable Kubernetes sandbox control plane that provisions gVisor-isolated pods from templates, with CLI, Python SDK, REST API, and built-in browser handoff for human intervention.

- **Isolation:** gvisor
- **Capabilities:** Kubernetes CRD-based provisioning (built on kubernetes-sigs/agent-sandbox); gVisor isolation; Warm pod pools; CLI + Python SDK + REST API; Browser handoff — short-lived links to hand a running session to a human; MCP-over-data-plane routing; Data plane proxy for outbound traffic
- **Requirements:** Kubernetes cluster (self-hosted); or managed service at treadstone-ai.dev
- **Limitations:** Solo maintainer; Maturity unclear; Full SDK/CLI surface suggests active development

_Notes: Built on kubernetes-sigs/agent-sandbox as the underlying CRD. Browser handoff is an unusual feature — enables smooth transitions from autonomous agent execution to human intervention. Offered both as open source and as a hosted service._

