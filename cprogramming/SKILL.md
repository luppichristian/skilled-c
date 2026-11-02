---
name: cprogramming
description: Use when creating, editing, reviewing, debugging, building, or testing C code or C projects.
---

# C Programming

Inspect the request and project: identify intended behavior, targets, toolchain, build and test setup, conventions, and project stage where evidenced. Ask when a missing decision would materially change the work. Always consider thread safety.

Apply these conventions to new C projects and, where feasible, throughout existing projects. Follow more specific user instructions and essential project requirements when they conflict; explain material incompatibilities. Distinguish intended target support from platforms actually built or tested.

## Workflow

1. For project creation or modification, licensing, or stage-dependent decisions, read [Project conventions](references/project.md).
2. Before implementing, design module interfaces with ownership, lifetimes, validity or error checks, and thread safety in mind. Apply the relevant references below; for code changes, use the code conventions and Clang tooling guidance.
3. Build the applicable configuration, run available checks that exercise the change, and verify platform-specific behavior where possible.
4. Report changes, builds and checks run, material limitations, unavailable toolchains or checks, and unresolved decisions.

## References

Read relevant references:

- [Build and tools](references/build.md): tool selection, compiler options, builds, and dependencies.
- [Clang tooling](references/tooling.md): project formatter and analyzer configuration, defaults, and invocation.
- [Code conventions](references/code.md): modules, types, memory, APIs, diagnostics, comments, and assertions.
- [Arena allocation](references/arenas.md): allocation, lifetimes, and allocator interfaces.
- [Testing](references/testing.md): unit and end-to-end tests, Unity, and build integration.
- [Debugging](references/debugging.md): GDB and in-process stack traces.
- [Concurrency](references/concurrency.md): shared state, thread-local storage, task systems, and multithreading.
- [Performance](references/performance.md): optimization, layout, assembly, intrinsics, and SIMD.
- [Portability](references/portability.md): platform implementations, serialization, architecture differences, and SIMD fallbacks.
- [CI and releases](references/ci-releases.md): artifact version format, GitHub workflows, runners, and cross-compilation.
