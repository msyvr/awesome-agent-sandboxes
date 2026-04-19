# Abstraction Layers

[Back to main guide](../README.md)

<a id="ref-computesdk"></a>
## ComputeSDK

**Maintainer:** ComputeSDK · **License:** Closed source · [Home](https://www.computesdk.com)

Unified API across multiple sandbox providers (E2B, Daytona, Modal, Blaxel, etc.).

- **Isolation:** microvm, container
- **Capabilities:** Provider-agnostic API; Single SDK for multiple backends
- **Requirements:** Account with underlying provider
- **Limitations:** Abstraction adds complexity; Provider-dependent isolation

_Notes: Useful if you want to avoid vendor lock-in. Isolation strength depends entirely on the chosen backend provider._

<a id="ref-langchain-sandboxes"></a>
## LangChain Sandboxes

**Maintainer:** LangChain · **License:** OSS · [Home](https://docs.langchain.com/oss/python/deepagents/sandboxes)

Sandbox integration layer within the LangChain agent framework.

- **Isolation:** container
- **Capabilities:** Framework integration; Provider abstraction; Agent workflow orchestration
- **Requirements:** LangChain framework; Python
- **Limitations:** Framework-dependent; Not standalone

_Notes: Only relevant if already using LangChain. The sandbox capabilities come from the underlying provider, not LangChain itself._

<a id="ref-nanoclaw"></a>
## NanoClaw

**Maintainer:** Lazer and Gavriel Cohen · **License:** MIT · [Home](https://github.com/qwibitai/nanoclaw)

Lightweight containerized agent orchestration wrapping Claude Code with messaging platform integrations.

- **Isolation:** container
- **Capabilities:** Container isolation (Docker/Docker Sandboxes/Apple Container); WhatsApp/Telegram/Slack/Discord/Gmail integration; Memory management; Scheduled jobs
- **Requirements:** Docker or Apple Container
- **Limitations:** Tied to Claude/Anthropic SDK; Container-level isolation unless using Docker Sandboxes

_Notes: More of an agent orchestration framework with sandbox support than a sandbox itself. High adoption. Sandbox capability comes from Docker or Docker Sandboxes underneath._

