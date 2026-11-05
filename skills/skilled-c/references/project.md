# Project conventions

## Targets

For new projects, target Windows, Linux, and macOS by default; add WebAssembly on request. Distinguish intended support from platforms built or tested.

## Licensing and source files

For new projects, use a root `LICENSE` with the complete chosen license text and applicable copyright notice. For existing projects, preserve the canonical license file, including alternative filenames; add a missing root `LICENSE` only if the owner confirms the terms. Use the owner's chosen license and copyright details; preserve third-party license and copyright notices.

Start each in-scope, project-owned `.h` and `.c` file with the complete project license text and applicable copyright notice in a C-style comment. Protect headers with `#pragma once`, not macro include guards.

## Setup

For a new project without a root `.gitignore`, use the plugin's [default](../assets/.gitignore). Preserve existing ignore rules; review copied patterns to avoid hiding files that need tracking.

Put build artifacts under `build`; use development and release configurations where appropriate. See [Build and tools](build.md) for build-system guidance.
