# Testing

## Unit tests

- Use Unity for unit tests; see [Unity unit tests](unity.md) for integration and runners.
- Make's third-party restriction excludes Unity. When a new project needs Unity, choose another suitable build system instead of making an exception.
- Use white-box techniques to cover statements, paths, and loops; use black-box equivalence class partitioning and boundary value analysis.
- Identify important state transitions and interactions as well as individual branches. Exercise representative common, boundary, and failure cases, including combinations that can invalidate shared assumptions; do not assume a wrapper or dispatch table removes underlying cases.

## End-to-end tests

- Launch programs with CTest or scripts; use observer utilities when sensible.
- For runtime applications, use the patterns in [Record/replay testing](replay-testing.md).

## Linux distributions

- When Linux is a target, select a practical set of distribution releases based on the project's supported environments and users. For broad Linux portability, consider Debian or Ubuntu and Fedora for glibc-based environments, and Alpine when targeting or evaluating musl. A few images do not establish support for every distribution.
- When Docker and its daemon are available locally, run Linux containers for the selected distributions. In each, install the project's required toolchain and dependencies, then configure, build, and run the applicable tests using the project's normal commands, such as CTest. Use clean, separate build directories for different distributions or toolchains. Reuse the same image definitions and test steps in the [CI distribution matrix](ci-releases.md#continuous-integration) where practical.
- Building separately in each image checks source portability. If distributing prebuilt binaries, also run the same release artifact on its intended distribution targets with their required runtime dependencies.
- Record image and release, architecture, compiler, C library, and test results. Report distributions or checks not run, including when Docker is unavailable; do not infer a pass from configuration or cross-compilation alone.
- Linux containers share a Linux kernel, including the VM kernel when Docker runs through a VM. They do not establish compatibility with other kernels, hardware, desktop or GPU environments, or CPU architectures. Use suitable native or VM tests for those needs, and identify emulated architectures as such.

## Organization

- Keep normal `src` code isolated from `test` code.
- With CMake, integrate all tests with CTest.
- Tests may not be necessary for minimal projects.
