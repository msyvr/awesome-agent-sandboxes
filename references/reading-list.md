# Reading List: Agent Sandboxing

Curated articles, papers, and discussions on sandboxing AI agents.

## Technical Deep Dives

- [Wrote a deep dive on sandboxing for AI agents: containers vs gVisor vs microVMs vs Wasm](https://www.reddit.com/r/devops/comments/1q4pvy6/wrote_a_deep_dive_on_sandboxing_for_ai_agents/) — Comparison of isolation mechanisms with security/performance trade-offs
- [A field guide to sandboxes for AI](https://www.luiscardoso.dev/blog/sandboxes-for-ai) — Landscape overview covering the major approaches and when to use each
- [Why sandboxing coding agents is harder than you think](https://martinalderson.com/posts/why-sandboxing-coding-agents-is-harder-than-you-think/) — Real-world challenges beyond "just use a container"
- [Local AI Agent Sandboxes Compared](https://rywalker.com/research/local-agent-sandboxes) — Head-to-head comparison of local sandboxing options

## Practical Guides

- [How to sandbox Claude Code with nono](https://nono.sh/blog/how-to-sandbox-claudecode-with-nono) — Step-by-step setup with the nono kernel-enforced sandbox
- [Your Coding Agent Needs a Sandbox: Docker Sandbox vs Native vs DevContainers](https://shanedeconinck.be/posts/docker-sandbox-coding-agents/) — Comparison of Docker Sandboxes, native sandboxing, and devcontainers
- [How to Safely Run AI Agents Like Cursor and Claude Code Inside a DevContainer](https://codewithandrea.com/articles/run-ai-agents-inside-devcontainer/) — DevContainer-based approach to agent isolation
- [Running Agents on Kubernetes with Agent Sandbox](https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/) — Official K8s blog post on the kubernetes-sigs/agent-sandbox project

## Architecture and Design

- [Sandboxing Agents at the Kernel Level](https://www.greptile.com/blog/sandboxing-agents-at-the-kernel-level) — Traces the Linux `open()` syscall through three kernel enforcement layers (permission bits, mount masking, chroot/namespaces) to explain why kernel-level isolation is the only reliable constraint for agent filesystem access
- [LangChain's Approach To Sandboxing — Native Isolation vs Docker Containers](https://cobusgreyling.medium.com/langchains-approach-to-sandboxing-native-isolation-vs-docker-containers-746a60b265c1) — Framework-level sandboxing design decisions
- [Sandboxing AI agents, 100x faster](https://blog.cloudflare.com/dynamic-workers/) — Cloudflare's V8 isolate approach to agent sandboxing
- [How we made sandboxed coding agents 10x faster to start](https://imbue.com/product/containers/) — Performance engineering for sandbox startup latency

## Research

- [Fault-Tolerant Sandboxing for AI Coding Agents: A Transactional Approach to Safe Autonomous Execution](https://arxiv.org/abs/2512.12806) — Academic paper on transactional safety for agent sandboxes
- [LLM Agent Harness Survey](https://github.com/Gloriaameng/LLM-Agent-Harness-Survey) — Survey of 110+ papers across 23 agent harness systems with a taxonomy. Different scope from this repo (harnesses, not sandboxes), but the "Security & Sandboxing" section cites sandbox-relevant papers (SandboxEscapeBench, AEGIS, PRISM)

## Discussions

- [Ask HN: Why are so many rolling out their own AI/LLM agent sandboxing solution?](https://news.ycombinator.com/item?id=46699324) — Community discussion on the proliferation of sandbox solutions

## Related Lists

- [awesome-ai-coding-sandboxes](https://github.com/fhiltscher/awesome-ai-coding-sandboxes) — Security-posture-first peer list: a 37-provider comparison matrix ranking on isolation tier, egress control (deny-default vs configurable vs open), and secrets brokering (credentials kept out via proxy vs injected). Complementary scope to this repo — it covers many hosted/proprietary providers with no GitHub presence — and a useful cross-check for coverage gaps.
