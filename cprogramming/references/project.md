# Project conventions

## Targets

For new projects, target Windows, Linux, and macOS by default; add WebAssembly on request. Distinguish intended support from platforms actually built or tested.

## Licensing and source files

For new projects, add a root `LICENSE` with the complete chosen license text and applicable copyright notice. For existing projects, preserve the canonical license file, including alternative filenames; if missing, add a root `LICENSE` when the owner confirms the terms. Ask for missing or unclear license and required copyright details. Do not choose or change terms yourself; preserve third-party license and copyright notices.

Start each in-scope, project-owned `.h` and `.c` file with the complete project license text and applicable copyright notice in a C-style comment. Protect headers with `#pragma once`, not macro include guards.

## Setup

If a project being created or modified has no root `.gitignore`, copy the skill's [default](../assets/.gitignore) there; preserve any existing one. Review the copied patterns and adjust those that would hide files needing tracking.

For a new project, select a build system and define development and release configurations. Put artifacts under `build`; add optional dependencies and test infrastructure when needed for the requested work. See [Build and tools](build.md) for build-system guidance.

## Project stage

| Stage | Priority |
| --- | --- |
| Early Development | Keep it simple and reach a first working build. |
| Deep Development | Prioritize quality and performance. |
| Closed Release | Start versioning; large changes are still allowed. |
| Public Release | Use strict versioning and be careful with large changes. |

Before Public Release, do not preserve backward compatibility by default; preserve it when explicitly required. If the stage is unknown and knowing it would change the work, do not assume one.
