# Agent-Integrated Sandboxes

[Back to main guide](../README.md)

<a id="ref-claude-code-sandbox"></a>
## Claude Code Sandbox

**Maintainer:** Anthropic · **License:** Closed source · [Home](https://code.claude.com/docs/en/sandboxing)

Native OS-level sandboxing using bubblewrap (Linux) and Seatbelt/sandbox-exec (macOS), reducing permission prompts by 84%.

- **Isolation:** user-namespace, seatbelt
- **Capabilities:** Filesystem isolation (CWD read/write, block writes elsewhere); Network isolation (proxy-based domain allowlisting); OS-level enforcement
- **Requirements:** Claude Code CLI; macOS or Linux
- **Limitations:** dangerouslyDisableSandbox escape hatch can be triggered by agent itself; macOS sandbox-exec deprecated by Apple; Shared kernel

_Notes: Demonstrated escape by Ona (March 2026) via dangerouslyDisableSandbox flag. Uses bubblewrap on Linux, Seatbelt on macOS — different mechanisms per OS._

<a id="ref-openai-codex-sandbox"></a>
## OpenAI Codex Sandbox

**Maintainer:** OpenAI · **License:** Closed source · [Home](https://developers.openai.com/codex/concepts/sandboxing)

Two modes: cloud (isolated containers, internet disabled during agent phase) and local CLI (Landlock + seccomp on Linux).

- **Isolation:** container, landlock, seccomp
- **Capabilities:** Cloud: isolated containers, two-phase runtime (setup with network, then offline agent); Cloud: per-project network lists, secrets removed before agent; Local: Landlock + seccomp, workspace-only writes
- **Requirements:** Cloud: OpenAI account + GitHub; Local: Linux kernel 5.13+
- **Limitations:** Cloud requires GitHub integration; Local is Linux-only; Network disabled by default in agent phase

_Notes: Only major agent with sandboxing enabled by default. Two-phase model (online setup, offline agent) is a unique security architecture — the agent never has network access during execution._

