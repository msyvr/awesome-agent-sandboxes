# Sandboxing for AI Safety & Alignment Research

This guide covers sandbox selection for safety and alignment research, including RL training, capability evaluation, and adversarial red-teaming. These contexts have fundamentally different containment requirements — what's overkill for RL training may be dangerously insufficient for red-teaming.

## How safety researchers approach sandboxing now (2026)

The practitioner question — "how do I stop an agent wrecking my machine?" — is only part of the alignment-research picture. Three shifts define how safety researchers use sandboxes today:

- **The sandbox is eval infrastructure.** Dangerous-capability evaluations run agents inside sandboxes so frontier models can be probed without real-world blast radius. The UK AI Security Institute's [Inspect Sandboxing Toolkit](https://www.aisi.gov.uk/blog/the-inspect-sandboxing-toolkit-scalable-and-secure-ai-agent-evaluations) is purpose-built for scalable, secure agent evals — the sandbox is research apparatus, not just a safety net.
- **AI control: the box is one layer, not the mechanism.** [Redwood Research](https://blog.redwoodresearch.org/p/guide)'s control agenda assumes the untrusted model may be actively scheming and designs *protocols* — trusted-model monitoring, interrogation, factored cognition, separation-of-duties — that aim to hold even if the model is adversarial. Evaluated against agentic environments like SHADE-Arena (see [Evaluating Control Protocols for Untrusted AI Agents](https://arxiv.org/abs/2511.02997)) and extended by work such as [TraceGuard](https://arxiv.org/abs/2604.03968) (Apart × Redwood, March 2026) and [Factor(T,U)](https://arxiv.org/abs/2512.02157). Containment is necessary, but the safety claim rests on monitoring as much as on the sandbox wall.
- **Escape and situational awareness are measured, not assumed.** [SandboxEscapeBench](https://arxiv.org/abs/2603.02277) (open source at [UKGovernmentBEIS/sandbox_escape_bench](https://github.com/UKGovernmentBEIS/sandbox_escape_bench)) tests whether frontier models break out of containers *while monitored*, spanning misconfiguration, privilege, kernel, and runtime/orchestration flaws — reinforcing that plain containers are insufficient for highly capable models and pushing high-stakes evals toward gVisor and microVMs. Separately, AISI found a sandboxed agent [reconstructed the institute's identity, operator, and cloud setup from inside the sandbox](https://www.aisi.gov.uk/blog/what-can-sandboxed-ai-agents-learn-about-their-evaluation-environments) (via domain names and TLS certificates) — agents can map their test environment and may [sandbag](https://arxiv.org/abs/2508.00943) (strategically underperform) when they detect evaluation, so environment fidelity is itself a containment concern.

This reframes the **What's missing from the landscape** section below: the gap isn't only adversarial-posture sandboxes, but sandboxes integrated with monitoring/control protocols and resistant to environment-fingerprinting.

## Three research contexts

### RL training

**Goal:** Run many parallel agent instances, reset environments quickly, compute rewards.

**Threat model:** Agents are typically small and early in training. Sophisticated escape attempts are unlikely. The main risks are accidental resource exhaustion and experiment contamination (shared state between runs).

**What matters most:**
- Fast environment reset (sub-second)
- Massive parallelism (thousands of concurrent instances)
- GPU access for training
- Experiment isolation (independent state per run)
- Reward computation outside the sandbox

**Containment level:** Process-level or container isolation is typically sufficient. Hardware VM isolation adds latency and overhead that directly slows training loops.

### Capability evaluation

**Goal:** Test trained agents against benchmarks and tasks in controlled environments.

**Threat model:** The agent is capable and may attempt unexpected actions, but isn't specifically optimized to escape. You need reliable containment and good observability of what the agent tried.

**What matters most:**
- Reliable filesystem and network isolation
- Observability — what did the agent attempt, including denied actions?
- Reproducibility — snapshot and replay scenarios
- Credential isolation — eval environments often need API access, but the agent shouldn't see real keys

**Containment level:** Hardened containers (gVisor, seccomp + read-only rootfs + dropped capabilities) or microVMs. Process-level sandboxing may be insufficient depending on agent capability.

### Adversarial red-teaming

**Goal:** Deliberately probe whether a capable agent can escape containment, exfiltrate data, or subvert its environment.

**Threat model:** The agent is actively trying to escape. This is the hardest containment problem. Research has shown that frontier LLMs can reliably escape *misconfigured* Docker containers — but note the word "misconfigured." Properly hardened containers with gVisor are meaningfully different from default Docker, and the specific configuration matters more than the broad category.

**What matters most:**
- Strongest available isolation boundary
- Escape detection and logging (not just prevention)
- Side-channel awareness — even with perfect filesystem/network isolation, timing, cache state, and resource usage patterns are potential information channels
- Audit trail with integrity guarantees the agent can't tamper with

**Containment level:** Hardware VM isolation (Firecracker, Kata) is the minimum for studying highly capable agents. For the most sensitive work, consider dedicated physical machines or NUMA-domain pinning to limit cache-based side channels — no software-only sandbox fully addresses information leakage.

## Sandbox options by research context

### RL training

| Need | Options | Trade-offs |
|------|---------|------------|
| Fast resets | Firecracker snapshots (~28ms restore), Zeroboot COW forking (~0.8ms), mitos (live COW fork of a warm microVM, tens of ms) | Zeroboot is much faster but unproven — **known CSPRNG concern**: random state is shared across COW forks, so experiments may not be independent unless you explicitly reseed. This can silently invalidate results. mitos forks a *running* Firecracker microVM into N copy-on-write siblings and restores from memory snapshots in milliseconds — hardware-isolated and K8s-native, but very new (alpha); the same shared-random-state caveat applies to its COW forks. |
| GPU + parallelism | Modal (50k+ concurrent, GPU support), openkruise/agents (K8s, GPU memory checkpoint) | Modal is cloud-only, closed source. openkruise/agents is self-hosted K8s with sandbox hibernation that preserves GPU memory state — useful for pausing and resuming training runs. |
| Eval + RL framework | OpenSandbox (Alibaba) | Explicitly designed for evaluation and RL training with multi-language SDKs. Very new (created December 2025) — verify that RL support meets your specific needs before committing. |
| Self-hosted scale | Firecracker + custom orchestration, mitos (K8s-native Firecracker), openkruise/agents (K8s) | Firecracker is battle-tested (powers AWS Lambda) but requires building your own orchestration — mitos supplies exactly that: a K8s operator, CRDs, and a KVM device-plugin for scheduling Firecracker microVMs (alpha, so not yet a production bet). openkruise/agents provides K8s-native lifecycle management with E2B API compatibility. |
| HPC / Slurm | agent_sandbox | Only sandbox surveyed with first-class Slurm awareness — a chaperon proxy wraps sbatch/srun/squeue/scancel so sandbox configuration propagates to allocated compute nodes and agents can't escape by submitting an unsandboxed job. Relevant when RL training runs on shared HPC clusters where unprivileged users can't run Docker. Linux-only; no egress allowlist or credential proxy. |

**Reward computation architecture:** The reward signal must be computed in a trusted environment that observes sandbox state, not inside the sandbox where the agent could influence it. An agent that can affect its own reward — directly or via side effects visible to the reward function — is a fundamental alignment failure mode. Design your sandbox architecture with a clear trust boundary: the agent runs inside; the reward function runs outside, reading only a defined observation interface.

### Capability evaluation

| Need | Options | Trade-offs |
|------|---------|------------|
| Syscall-level observability | gVisor | Intercepts every syscall in user space via its Sentry kernel. You can instrument and log all agent-OS interaction. Practical caveat: logs are verbose — you'll need filtering infrastructure to extract meaningful signals. |
| Credential isolation | nono, cleanroom (Buildkite), sandcat (VirtusLab) | All keep API keys outside the sandbox via a host-side / proxy boundary. nono adds L7 API endpoint filtering; cleanroom adds a microVM isolation boundary (stronger than nono's process-level); sandcat substitutes secrets at a transparent mitmproxy so a container running in bypass mode never sees real credential values (container-tier, so weaker containment than the other two). Directly tests whether agents attempt credential exfiltration. |
| Audit trail | nono | Cryptographic audit chain with Sigstore attestation. The agent cannot tamper with the record of what it did. |
| Observability / intervention | sevorix-lite, gVisor, loop | sevorix-lite's "Yellow Lane" dashboard lets researchers observe and intervene in real time (approve/deny/redirect). loop traps syscalls via seccomp RET_USER_NOTIF and routes each trap to a three-button Slack/Discord card with once/session/deny caching — same human-in-the-loop pattern, different operator surface (chat vs. dashboard). gVisor logs denied syscalls for post-hoc analysis. |
| Reproducibility | Firecracker snapshots, Fly Sprites (persistent) | Snapshot before evaluation, restore to replay. Fly Sprites offers persistent 100GB NVMe if you need durable eval environments. |
| Controlled capability exposure | nono (L7 API filtering), gondolin (programmable egress hooks), Wasm/WASI (capability grants) | Gradually increase what the agent can access and study behavioral changes at each level. gondolin's TypeScript control plane lets you script per-secret, per-destination credential injection — useful for testing whether an agent misuses credentials when given access to specific endpoints. |

### Adversarial red-teaming

| Need | Options | Trade-offs |
|------|---------|------------|
| Hardware VM containment | Firecracker (with jailer), Kata Containers, cleanroom (Buildkite), brood-box (Stacklok) | Separate kernel per sandbox. Firecracker's jailer adds defense in depth. cleanroom and brood-box both provide ready-to-use tools with hardware VM isolation on Linux and macOS. brood-box adds TOCTOU-resistant diff review — the VM is stopped before the user reviews changes, preventing the agent from modifying files during review. |
| Escape detection | gVisor (denied syscall logging), sevorix-lite (eBPF syscall interception), nono (boundary violation recording), code-on-incus (nftables threat detection + auto-kill) | Most sandboxes silently block forbidden actions. gVisor, sevorix-lite, and nono record them. code-on-incus goes further — actively detects escape-like network behavior (reverse shells, C2 callbacks, DNS tunneling) and auto-pauses or kills the container. |
| Network monitoring | nono (L7 filtering + logging), cleanroom (deny-by-default egress + policy allowlists), sandcat (transparent WireGuard→mitmproxy over all HTTP/S, DNS, TCP/UDP), Anthropic srt (proxy with interactive approval) | See exactly what network endpoints the agent attempts to reach, including denied requests. cleanroom's deny-by-default posture means nothing gets through unless explicitly allowed. sandcat captures *all* container traffic transparently — no per-tool proxy config — with an allow/deny engine over the full flow. |
| Side-channel mitigation | Dedicated physical machines, NUMA pinning | Software-only sandboxes share CPU cache hierarchy. For studying highly capable agents, consider hardware-level isolation. No sandbox in this repo fully addresses information leakage. |

## Maturity vs. security properties

Several tools with excellent *design* for safety research have immature *implementations*. Both facts deserve equal weight:

| Tool | Security properties | Maturity caveat |
|------|-------------------|-----------------|
| nono | Credential proxy, atomic rollback, cryptographic audit, capability-based isolation | Early alpha, not yet security-audited. Using an unaudited tool to contain agents whose behavior you're studying because it's uncertain is a tension worth acknowledging. |
| cleanroom | MicroVM isolation, credential proxy, deny-by-default egress, per-repo policy | Early project, no LICENSE file. Backed by Buildkite (established company), but the tool itself is new and untested at scale. |
| sevorix-lite | eBPF syscall interception, mount namespace shell override, human-in-the-loop dashboard | "Lite" edition of a commercial product (Sevorix). AGPL license. macOS support is reduced (no eBPF/seccomp). Full enforcement is Linux-only. |
| openkruise/agents | K8s sandbox lifecycle, GPU memory checkpoint, E2B API compatibility | CNCF-affiliated via OpenKruise, but the agent sandbox operator itself is early. |
| Zeroboot | Sub-millisecond VM creation, hardware isolation | Not production-hardened. CSPRNG state sharing across forks is a research-correctness risk for RL. |
| OpenSandbox | RL + evaluation framework, multi-language SDKs | Very new (created December 2025). RL support claims are from Alibaba's documentation — verify independently. |
| agent_sandbox | Multi-backend kernel isolation (bubblewrap/firejail/Landlock), generated seccomp filters, HPC/Slurm chaperon | Young project (~2 months at inclusion). Ships a 32 KB threat model and a documented pentest cycle with 14 findings (2 critical, 3 high) addressed. Author honestly classifies it as "best-effort user-space isolation, not a security product" and acknowledges no egress allowlist and no credential proxy. |
| mitos | K8s-native Firecracker microVM per agent, live COW fork of a warm VM, memory-snapshot restore | Very new (created May 2026), prerelease/alpha — features split across "husk" and "engine" paths mid-migration. Hardware-isolated (Firecracker) but the orchestration layer is unproven. COW forks share random state unless reseeded (same RL-independence caveat as Zeroboot). |
| sandcat | Transparent full-traffic capture (WireGuard→mitmproxy), allow/deny egress, proxy-level secret substitution | Container-tier (shared kernel), not VM isolation. Backed by VirtusLab (established). Brings the credential-proxy pattern down from VM tier to a devcontainer — convenient, but a weaker containment boundary than nono or cleanroom. |
| Firecracker | Hardware VM, snapshot/restore, jailer | Mature and battle-tested (AWS Lambda/Fargate). The safest bet for production safety research infrastructure. |
| gVisor | Syscall interception, user-space kernel | Mature (Google, GKE). Production-proven. Observability requires custom instrumentation — it's a security runtime, not a research tool. |

## What's missing from the landscape

1. **Few sandboxes default to an adversarial posture.** Most assume the agent is trying to be helpful. cleanroom's deny-by-default egress and credential proxy come closest to treating the agent as potentially adversarial, but even it doesn't monitor for escape attempts or alert on anomalous behavior. A purpose-built safety research sandbox would combine deny-by-default containment with escape detection and behavioral alerting.

2. **Escape study tooling doesn't exist.** Researchers studying escape behavior need to observe and replay escape attempts, not just prevent them. gVisor's syscall logging is the closest thing, but there's no turnkey "escape research sandbox."

3. **Capability escalation isn't a built-in feature.** Safety research often involves gradually increasing capabilities to study behavioral transitions. You'd need to script this yourself using nono's capability model or WASI grants.

4. **Side channels are unaddressed.** Every software sandbox in this repo shares some hardware state with the host. For the most capable agents, this may matter.
