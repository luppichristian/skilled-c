---
name: skilled-c
description: Use when working on C code or C projects that need consistent coding conventions, project rules, and development tools.
---

# Skilled C

These references describe C tools, patterns, and conventions. Apply the guidance relevant to the task while respecting the user's instructions and existing project conventions. Platform support depends on the actual compiler, libraries, and target.

## MCP setup

Check which bundled MCP tools are available when they are useful for the task. Follow [MCP integration](references/mcp.md) for server-specific guidance and fallbacks. If a server is unavailable, continue with suitable local tools; do not assume that installing the plugin also installed its external toolchain.

## References

Read relevant references:

- [Project conventions](references/project.md): targets, licensing, project layout, and ignore files.
- [Build and tools](references/build.md): tool selection, compiler options, builds, and dependencies.
- [Clang tooling](references/tooling.md): project formatter and analyzer configuration, defaults, and invocation.
- [Code conventions](references/code.md): modules, types, memory, APIs, diagnostics, comments, and assertions.
- [Arena allocation](references/arenas.md): allocation, lifetimes, and allocator interfaces.
- [Table-driven code generation](references/code-generation.md): shared metadata, generated C, and build integration.
- [Testing](references/testing.md): unit and end-to-end tests, Unity, and build integration.
- [Debugging](references/debugging.md): GDB, in-process stack traces, and graphics debugging with RenderDoc.
- [Concurrency](references/concurrency.md): shared state, thread-local storage, task systems, and multithreading.
- [Runtime loops](references/runtime-loops.md): simulation steps, presentation, input timing, and snapshots.
- [Performance](references/performance.md): optimization, layout, assembly, intrinsics, and SIMD.
- [Portability](references/portability.md): platform implementations, serialization, architecture differences, and SIMD fallbacks.
- [CI and releases](references/ci-releases.md): artifact version format, GitHub workflows, runners, and cross-compilation.

Some design guidance adapts Ryan Fleury's [general programming essays](https://www.dgtlgrove.com/p/index?open=false#%C2%A7general-programming-essays).
