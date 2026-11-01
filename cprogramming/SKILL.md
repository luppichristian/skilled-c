---
name: cprogramming
description: Use when creating, editing, reviewing, debugging, building, or testing C code or C projects.
---

# C Programming

Inspect the request and existing project before making changes. Identify the supported targets, toolchain, build and test setup, established conventions, and project stage when there is evidence for them. Always consider thread safety.

For new projects, target Windows, Linux, and macOS by default; add WebAssembly when requested. Distinguish intended platform support from platforms actually built or tested.

Use these conventions when creating new C projects and apply them throughout existing projects where feasible. Follow more specific user instructions and essential project requirements when they conflict, and explain material incompatibilities.

For new projects, add a root `LICENSE` file containing the project's complete chosen license text and applicable copyright notice. For existing projects, preserve their canonical license file, including alternative filenames; if it is missing and the owner confirms the terms, add a root `LICENSE`. Ask for the license and any required copyright details when missing or unclear. Do not choose or change license terms yourself, and preserve third-party license and copyright notices.

Start each project-owned `.h` and `.c` file in scope with the project's complete license text and applicable copyright notice in a C-style comment. Protect headers with `#pragma once` instead of macro include guards.

Check that the selected compiler, target, and tools support the requested options. Explain limitations rather than claiming unverified support. Reuse existing type definitions; do not invent meanings for unspecified aliases. Treat debug symbols and static CRT linkage as separate settings.

## Workflow

1. Identify the program's intended behavior, supported targets, project stage, and any existing build, tests, and tool configuration. Ask for a decision when a missing requirement would materially change the implementation.
2. When creating or modifying a project with no root `.gitignore`, copy the skill's [default `.gitignore`](assets/.gitignore) to the project root. Preserve an existing `.gitignore`. Review the copied patterns and adjust them if they would hide project files that need to be tracked. For a new project, select a build system and define its development and release configurations. Place build artifacts under `build`; add optional dependencies and test infrastructure when needed for the requested work.
3. Design module interfaces before implementing them. Specify ownership and lifetime of returned data, how callers check validity or errors, and thread-safety expectations. Organize dynamic memory around arenas and document when their allocations become invalid.
4. Implement the requested behavior using the relevant code, concurrency, performance, and portability references. For each missing project Clang configuration, copy the corresponding default as described in [Clang tooling](references/tooling.md); preserve configuration files already present. Validate external inputs and handle expected failures; use assertions for internal execution invariants.
5. Build the applicable configuration and run available checks that exercise the change. When unit tests are requested, integrate Unity as described in the testing reference. Verify platform-specific behavior on the targets actually available, and report unavailable toolchains or checks.
6. Report what changed, which builds or checks ran, and any material limitations or unresolved decisions. Distinguish intended target support from support verified by execution.

## Project stage

| Stage | Priority |
| --- | --- |
| Early Development | Keep it simple and reach a first working build. |
| Deep Development | Prioritize quality and performance. |
| Closed Release | Start versioning; large changes are still allowed. |
| Public Release | Use strict versioning and be careful with large changes. |

Before Public Release, do not preserve backward compatibility by default. Preserve it when explicitly required. If the stage is unknown and it would change the work, do not assume one.

## References

Read the references relevant to the current task:

- [Build and tools](references/build.md): selecting or using development tools; compiler options; configuring builds and dependencies.
- [Clang tooling](references/tooling.md): project formatter and analyzer configuration, default files, and tool invocation.
- [Code conventions](references/code.md): modules, naming, types, memory allocation, comments, API documentation, and assertions.
- [Testing](references/testing.md): deciding on tests, designing unit or end-to-end tests, and integrating them with the build.
- [Concurrency](references/concurrency.md): persistent or shared state, thread-local storage, task systems, and multithreading patterns.
- [Performance](references/performance.md): optimization, layout, assembly, intrinsics, and SIMD.
- [Portability](references/portability.md): platform-specific implementations, serialization, architecture differences, and SIMD fallbacks.
- [CI and releases](references/ci-releases.md): artifact version format, GitHub workflows, runners, and cross-compilation.
