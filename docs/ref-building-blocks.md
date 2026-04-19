# Building Blocks

[Back to main guide](../README.md)

The underlying technologies that sandbox products are built on.

## VM & Container Runtimes

<a id="ref-firecracker"></a>
### Firecracker

**Maintainer:** AWS · **License:** Apache-2.0 · [Home](https://github.com/firecracker-microvm/firecracker)

Lightweight microVM monitor using KVM with <5MB overhead, powering Lambda, Fargate, E2B, Vercel, Bunnyshell, and Fly Sprites.

- **Isolation:** kvm, microvm
- **Capabilities:** KVM hardware isolation; <125ms boot; <5MB memory per VM; Snapshot/restore (~28ms); Rate limiters; Jailer for additional containment
- **Requirements:** Linux with KVM; x86_64 or aarch64
- **Limitations:** Linux only; No GPU passthrough; Minimal device model; Must build own orchestration layer

_Notes: The foundation most cloud sandbox platforms build on. Battle-tested at AWS scale (Lambda, Fargate). If you're building a sandbox product, this is likely your starting point._

<a id="ref-gvisor"></a>
### gVisor

**Maintainer:** Google · **License:** Apache-2.0 · [Home](https://github.com/google/gvisor)

User-space kernel that intercepts and re-implements Linux syscalls, providing container isolation without hardware virtualization.

- **Isolation:** gvisor
- **Capabilities:** Syscall interception in user space; No hardware virtualization needed; OCI-compatible (drop-in runsc runtime); Sentry kernel + Gofer file proxy architecture
- **Requirements:** Linux; OCI runtime (runsc)
- **Limitations:** Performance overhead on syscall-heavy workloads; Not all syscalls implemented

_Notes: Used by GKE and kubernetes-sigs/agent-sandbox. Good middle ground between container and VM isolation — stronger than containers, lighter than full VMs._

<a id="ref-kata-containers"></a>
### Kata Containers

**Maintainer:** OpenInfra Foundation · **License:** Apache-2.0 · [Home](https://github.com/kata-containers/kata-containers)

VM-level isolation per container, OCI/CRI compatible, supporting QEMU, Cloud Hypervisor, and Firecracker VMMs.

- **Isolation:** kata, kvm
- **Capabilities:** Hardware VM per container; OCI/CRI compatible; Multiple VMM backends (QEMU/Cloud Hypervisor/Firecracker); Kubernetes integration
- **Requirements:** Linux with KVM
- **Limitations:** Higher overhead than gVisor; Requires KVM; More complex setup

_Notes: Production-proven at scale via Northflank (2M+ workloads/month). Good for Kubernetes environments that need VM-level isolation per pod._

<a id="ref-libkrun"></a>
### libkrun

**Maintainer:** Containers project (Red Hat) · **License:** Apache-2.0 · [Home](https://github.com/containers/libkrun)

Library-based KVM virtualization with container-competitive startup, supporting Apple Virtualization.framework on macOS.

- **Isolation:** kvm
- **Capabilities:** Library-embeddable (no daemon); KVM isolation; Fast startup; Apple Virtualization.framework on macOS
- **Requirements:** Linux (KVM) or macOS (Virtualization.framework)
- **Limitations:** Less tooling than Firecracker; Smaller community

_Notes: macOS support via Apple Virtualization.framework is unique among VM runtimes — Firecracker and Kata are Linux-only. Used by microsandbox._

<a id="ref-zeroboot"></a>
### Zeroboot

**Maintainer:** Zeroboot (community) · **License:** OSS · [Home](https://github.com/zerobootdev/zeroboot)

Sub-millisecond VM sandboxes via COW forking of Firecracker snapshots (~0.8ms fork creation).

- **Isolation:** kvm, microvm
- **Capabilities:** KVM isolation; Firecracker snapshot COW forking; ~0.8ms sandbox creation; Self-hostable; Managed API also available
- **Requirements:** Linux with KVM
- **Limitations:** Very new; Small community

_Notes: 0.8ms sandbox creation via COW forking is remarkable if verified at scale. Worth watching as a potential next-gen approach to sandbox provisioning._

## OS-Level Sandboxing

<a id="ref-bubblewrap-bwrap"></a>
### bubblewrap (bwrap)

**Maintainer:** Containers project (Flatpak origin) · **License:** LGPL-2.0+ · [Home](https://github.com/containers/bubblewrap)

Unprivileged user-namespace sandbox for Linux requiring no root, used by Claude Code and Flatpak.

- **Isolation:** user-namespace
- **Capabilities:** User namespaces; Mount namespaces; Network namespace; No root required
- **Requirements:** Linux with user namespace support
- **Limitations:** Linux only; Low-level (must compose with other tools)

_Notes: Years of hardening via Flatpak. Claude Code's Linux sandbox builds on this. The go-to unprivileged sandbox primitive on Linux._

<a id="ref-firejail"></a>
### Firejail

**Maintainer:** netblue30 (community) · **License:** GPL-2.0 · [Home](https://github.com/netblue30/firejail)

SUID sandbox combining namespaces, seccomp, and capabilities with desktop-aware features (audio, display).

- **Isolation:** user-namespace, seccomp
- **Capabilities:** Namespace isolation; seccomp-BPF filtering; Filesystem whitelisting; Network filtering; Desktop app support (audio, display); Pre-built profiles for common apps
- **Requirements:** Linux; Setuid binary
- **Limitations:** SUID is a larger attack surface; Desktop-focused; Linux only

_Notes: Primarily for desktop app sandboxing, but applicable to agent processes. SUID requirement is a trade-off — convenience vs. attack surface._

<a id="ref-landlock-lsm"></a>
### Landlock LSM

**Maintainer:** Linux kernel community · **License:** GPL-2.0 · [Home](https://landlock.io)

Unprivileged filesystem access control at kernel level, used by Codex CLI and NVIDIA OpenShell.

- **Isolation:** landlock
- **Capabilities:** Filesystem access restrictions per path; Unprivileged (no root); Stackable with other LSMs; Kernel-level enforcement
- **Requirements:** Linux kernel 5.13+ (network support in 6.7+)
- **Limitations:** Filesystem only in early kernel versions; Must combine with seccomp for full coverage; Linux only

_Notes: The modern Linux answer to unprivileged sandboxing. Network support in kernel 6.7 makes it much more complete. Used by Codex CLI and OpenShell._

<a id="ref-linux-namespaces-cgroups"></a>
### Linux Namespaces + cgroups

**Maintainer:** Linux kernel community · **License:** GPL-2.0

Foundation of all container technology — PID, mount, network, user, UTS, and IPC namespaces plus cgroups for resource limits.

- **Isolation:** user-namespace
- **Capabilities:** Process isolation (PID namespace); Filesystem isolation (mount namespace); Network isolation (network namespace); User isolation (user namespace); CPU/memory/IO limits (cgroups)
- **Requirements:** Linux
- **Limitations:** Building blocks only — must compose into usable tools; Shared kernel; Linux only

_Notes: Everything in the container and VM space builds on these primitives. Understanding namespaces and cgroups is foundational to evaluating any Linux-based sandbox's isolation claims._

<a id="ref-macos-seatbelt-sandbox-exec"></a>
### macOS Seatbelt / sandbox-exec

**Maintainer:** Apple · **License:** Closed source

macOS mandatory access control using SBPL policies for filesystem, network, and process restrictions.

- **Isolation:** seatbelt
- **Capabilities:** Filesystem access control; Network control; Process restrictions; Kernel-level enforcement
- **Requirements:** macOS only
- **Limitations:** sandbox-exec deprecated by Apple; SBPL policy language poorly documented

_Notes: Deprecated but still the only game in town for macOS process sandboxing. Used by Claude Code, Agent Safehouse, and srt on macOS. No replacement announced by Apple._

<a id="ref-nsjail"></a>
### nsjail

**Maintainer:** Google · **License:** Apache-2.0 · [Home](https://github.com/google/nsjail)

Process isolation tool combining namespaces, seccomp, and resource limits with the Kafel policy language.

- **Isolation:** user-namespace, seccomp
- **Capabilities:** Namespace isolation; seccomp-BPF filtering; cgroup resource limits; chroot/pivot_root; Network filtering; Kafel policy language
- **Requirements:** Linux
- **Limitations:** Linux only; Less actively maintained; CLI only

_Notes: Google-maintained. Kafel policy language is more ergonomic than raw seccomp-BPF. Used by competitive programming judges for untrusted code execution._

<a id="ref-seccomp-bpf"></a>
### seccomp-BPF

**Maintainer:** Linux kernel community · **License:** GPL-2.0

Syscall filtering using BPF programs to kill, trap, or errno on forbidden syscalls.

- **Isolation:** seccomp
- **Capabilities:** Syscall-level filtering; BPF programmability; Kill/trap/errno on forbidden syscalls
- **Requirements:** Linux kernel 3.5+
- **Limitations:** Syscall-level only (no file path awareness); Complex BPF filter authoring; Linux only

_Notes: Building block, not standalone. Almost always used alongside Landlock or namespaces to provide full sandbox coverage._

## WebAssembly Runtimes

<a id="ref-pyodide"></a>
### Pyodide

**Maintainer:** Pyodide community (Mozilla origin) · **License:** MPL-2.0 · [Home](https://github.com/pyodide/pyodide)

CPython compiled to WebAssembly providing browser-grade sandbox security for Python execution.

- **Isolation:** wasm
- **Capabilities:** Full CPython in Wasm; Browser-grade isolation; Supports NumPy, Pandas, and other scientific packages
- **Requirements:** Browser or Wasm runtime
- **Limitations:** Python only; Not all C extensions supported; No native filesystem or network access; Performance overhead vs. native CPython

_Notes: Good for sandboxing Python-only agent code execution where you need browser-grade isolation guarantees without running a VM._

<a id="ref-wasmcloud"></a>
### wasmCloud

**Maintainer:** wasmCloud community · **License:** Apache-2.0 · [Home](https://github.com/wasmCloud/wasmCloud)

Application platform for building distributed Wasm applications with capability-based security.

- **Isolation:** wasm
- **Capabilities:** Distributed Wasm applications; Capability-based security model; Provider-based extensibility; Lattice networking
- **Requirements:** Cross-platform; NATS for messaging
- **Limitations:** Must compile to Wasm; More complex than standalone runtimes; Application platform, not just a runtime

_Notes: Higher-level than Wasmtime or WasmEdge — it's an application platform, not just a runtime. Useful if building distributed agent systems with Wasm isolation._

<a id="ref-wasmedge"></a>
### WasmEdge

**Maintainer:** CNCF · **License:** Apache-2.0 · [Home](https://github.com/WasmEdge/WasmEdge)

Cloud-native WebAssembly runtime optimized for edge, AI, and serverless workloads.

- **Isolation:** wasm
- **Capabilities:** Memory-safe execution; WASI support; AI/ML inference extensions; Kubernetes integration; Edge deployment focus
- **Requirements:** Cross-platform; Must compile tools to Wasm
- **Limitations:** Must compile to Wasm; Not for arbitrary Linux binaries

_Notes: CNCF project. Differentiates from Wasmtime with AI/ML inference extensions and edge deployment focus._

<a id="ref-wasmtime"></a>
### Wasmtime

**Maintainer:** Bytecode Alliance · **License:** Apache-2.0 · [Home](https://github.com/bytecodealliance/wasmtime)

Fast, secure WebAssembly runtime with WASI capability-based security and linear memory isolation.

- **Isolation:** wasm
- **Capabilities:** Memory-safe execution; WASI capability-based security; Multi-tenant isolation; Thousands of concurrent instances; Cross-platform
- **Requirements:** Cross-platform; Must compile tools to Wasm
- **Limitations:** Must compile to Wasm; Not for arbitrary Linux binaries; Ecosystem still maturing

_Notes: The reference Wasm runtime from Bytecode Alliance. Architecturally elegant sandboxing but requires toolchain buy-in — you can't run arbitrary binaries._

<a id="ref-wassette"></a>
### Wassette

**Maintainer:** Microsoft (Azure Core Upstream) · **License:** OSS · [Home](https://github.com/microsoft/wassette)

Wasm Components exposed via MCP, using Wasmtime runtime with agents fetching Wasm tools from OCI registries.

- **Isolation:** wasm
- **Capabilities:** Wasm Component Model; MCP interface; Deny-by-default security; Wasmtime runtime (browser-grade isolation); OCI registry integration
- **Requirements:** Rust toolchain; MCP-compatible agent
- **Limitations:** Wasm only (must compile tools to Wasm); Early ecosystem

_Notes: Interesting intersection of MCP and Wasm — agents discover and load sandboxed tools via MCP from OCI registries. Microsoft backing. Released Aug 2025._

