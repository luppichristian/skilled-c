---
name: skilled-c
description: Use when working on C code or C projects needing consistent coding conventions, project rules, and tools.
---

# Skilled C

Apply relevant guidance; respect user instructions and existing project conventions. Platform support depends on compiler, libraries, and target.

## MCP setup

Follow [MCP integration](references/mcp.md). If a server is unavailable, use suitable local tools; plugin installation does not imply its external toolchain is installed.

## References

Read relevant references:

- [Project conventions](references/project.md): targets, licensing, layout, and ignore files.
- [Build and tools](references/build.md): Clang builds, cross-platform CMake, and pinned FetchContent dependencies.
- [Clang tooling](references/tooling.md): formatter and analyzer configuration, defaults, and invocation.
- [Code conventions](references/code.md): modules, types, memory, APIs, containers, diagnostics, comments, and assertions.
- [Arena allocation](references/arenas.md): allocation, lifetimes, and allocator interfaces.
- [Table-driven code generation](references/code-generation.md): shared metadata, generated C, and build integration.
- [Testing](references/testing.md): unit and end-to-end tests, Linux distribution checks, Unity, and build integration.
- [Debugging](references/debugging.md): GDB, in-process stack traces, and graphics debugging with RenderDoc.
- [Concurrency](references/concurrency.md): shared state, thread-local storage, task systems, and multithreading.
- [Parallel execution](references/parallelism.md): CPU workers, GPU compute, synchronization, and workload tradeoffs.
- [Runtime loops](references/runtime-loops.md): simulation steps, presentation, input timing, and snapshots.
- [Graphics](references/graphics.md): library selection, GPU resource lifetimes, shaders, and image composition.
- [User interfaces](references/ui.md): immediate-mode UI, layout, interaction, and Clay for complex interfaces.
- [Audio](references/audio.md): library selection, real-time callbacks, stream formats, and mixing.
- [Performance](references/performance.md): optimization, layout, assembly, intrinsics, and SIMD.
- [Portability](references/portability.md): platform implementations, serialization, architecture differences, and SIMD fallbacks.
- [CI and releases](references/ci-releases.md): artifact version format, GitHub workflows, Linux container matrices, and cross-compilation.
