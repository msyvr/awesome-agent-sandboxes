# Strategy update — 2026-09-03

Four unreviewed weekly discovery issues (2026-08-10 through 2026-08-31) plus the first full pass over the peer-list cross-check produced the largest single batch since the seed: 203 unique repos and 30 hosted products triaged, 45 entries added (97 → 142). The batch is large enough to show shape, and three shapes are new since the 2026-04-25 and 2026-05-05 updates.

## 1. A self-hosted platform tier has separated from "standalone"

The standalone category held 45 entries and mixed two things: tools you install on one machine to wrap one agent (nono, srt, fence, microsandbox, the Docker wrappers), and control planes you run on your own infrastructure to serve many sandboxes over an API (CubeSandbox, Containarium, warren, OpenSandbox). This batch added seven more of the second kind — forkd, AgentENV, k7, cocoon, Arrakis, Dormice, Judge0 — all E2B-shaped: a daemon, a REST/gRPC API, SDKs, warm pools, snapshots. Several ship an E2B-compatible API surface outright (AgentENV, Dormice, k8e, CubeSandbox), which is the clearest sign a de-facto interface has settled.

Action taken: new category `self-hosted-platform` ("Self-Hosted Sandbox Platforms"), sitting between Standalone and Kubernetes. The four existing entries above moved into it. The distinction from Kubernetes is scheduler ownership: Kubernetes entries need a cluster; platform entries bring their own scheduler or run on bare metal. Standalone's label became "Standalone / Local Tools" and its intro now names the three sub-kinds it still holds (host-native kernel wrappers, local microVM launchers, container wrappers).

## 2. Credential brokering at the egress proxy is becoming the default security property

Twelve of the 45 additions keep secrets out of the sandbox by design: the agent holds a placeholder, and a proxy on the host or at the network edge substitutes the real credential per request. Open-source: matchlock, shuru, boxlite, agentbox (git push only), clampdown (API key), clawker (agent forwarding instead), OneCLI, netclode. Hosted: Declaw, InstaVM, Islo, and Tensorlake's per-tool-call VMs achieve the same effect structurally. Before this batch the list had four such entries (nono, srt, sandcat, agent-glovebox). This is what the 2026-04-25 update called a "novel security property" that clears the container-tier bar; it is no longer novel. The bar for container-tier additions rises accordingly: a credential proxy alone is now table stakes, and a new Docker-tier entry needs it plus something else (nested-container enforcement as in clampdown, request-path egress rules as in clawker, per-push human approval as in agentbox).

The list has no structured field for this property. `capabilities` free text carries it, and the safety-research capability-evaluation table lists a hand-picked subset. A controlled facet (`security_properties: [credential-proxy, egress-allowlist, fork-snapshot, audit-log, ...]`) would let the site filter on it and would keep the safety-research tables honest as the count grows. Not done in this batch; recorded as the next schema change worth making.

## 3. Fork-and-branch of running state is the microVM tier's new differentiator

Boot time was the microVM tier's headline number in April. In this batch the headline is forking a *running* sandbox: forkd (children from a warm parent via CoW, mid-execution branch), smolvm (CoW fork of live machines), AgentENV (incremental snapshot/fork for RL rollouts), k7d (warm CoW fork), Morph Cloud (Infinibranch memory+disk snapshots), Freestyle (live fork), Box (disk-level fork), cocoon (checkpoint/fork/hibernate). The use case is parallel agent rollouts — tree search, N-best sampling, RL — which is the safety-research RL-training table's concern. Zeroboot and mitos already carried this; the RL table gains AgentENV and forkd.

## Rejection patterns confirmed

- **Governance orchestrators keep arriving via author-submitted PRs.** SandBase Harness (#58, #59) matched the 2026-05-05 auto-reject pattern exactly and added a new wrinkle: the submitting org forked this list and seven peer lists on the same day and logs ~40 simultaneous list-submission PRs in its own repo. Source read showed the "local sandbox" is TypeScript path-prefix checks and the Docker backend is `docker run` with no hardening flags. Author-submitted PRs now get the same source-level check vetto received before any YAML is accepted.
- **Wrappers over listed entries** (agent-sandbox/agent-sandbox over kubernetes-sigs Agent Sandbox; philschmid/code-sandbox-mcp and skypilot-code-sandbox over llm-sandbox; microsandbox-rb bindings; the three OpenShell satellites) go in excluded.yaml with a pointer, or into the parent's notes when they are significant on their own (NemoClaw at 22k stars).
- **Hosted products with undisclosed isolation** (hopx, Baponi) are held rather than listed. Tencent AGS set the precedent for listing with an inferred mechanism only because press coverage identified the engine; with nothing to infer from, an entry would be a marketing page in YAML form.

## Discovery mechanics

- The peer-list cross-check resurfaced five already-listed products under different URL paths (modal.com vs modal.com/products/sandboxes, codesandbox.io, coder.com, fly.io/sprites, superserve.ai). Host-level normalization in discover.py is needed; until then, expect the "peer-list projects without a GitHub repo" table to carry a fixed set of false positives.
- Two more peer lists were added to data/peer-lists.yaml: restyler/awesome-sandbox (573 stars, 74 links) and dloss/awesome-agent-sandboxes (43 links).
- GitHub org moves silently break the dedupe: fencesandbox/fence surfaced as new because the listed URL was Use-Tusk/fence. The API follows the redirect (`gh api repos/Use-Tusk/fence` returns the new full_name), so discover.py could resolve listed repo URLs through the API once per run and flag renames instead of surfacing them as candidates.
