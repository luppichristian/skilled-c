# CI and releases

- Use `MAJOR.MINOR.PATCH-DD.MM.YYYY` as the artifact version format.
- For GitHub Actions, use `ci.yml` on pushes and pull requests, and `cd.yml` when a new tag is pushed. The tag workflow builds artifacts and attaches them to a GitHub Release.
- Recommended runners: `ubuntu-latest` for Linux/Unix, `macos-latest` for macOS, and `windows-latest` for Windows.
- Cross-compile for different architectures on these systems when needed.

## Continuous integration

- Use a runner matrix for supported desktop platforms. On each runner, check out source, select Clang, configure the project's actual build system, and build requested configurations.
- Run configured project tests, including CTest for CMake projects, and configured formatting or static-analysis checks.
- For relevant Linux targets, add a Docker-based matrix on `ubuntu-latest` for the selected distribution releases in [Linux distribution testing](testing.md#linux-distributions), alongside any Windows and macOS jobs. Use the same container definitions and build/test steps locally where practical; check out the source on the runner and run the builds and tests inside each container.
- Select explicit image releases or digests and update them deliberately. Install distribution-specific dependencies with the appropriate package manager, use a Clang version that supports the project's required C dialect, and account for different shells, C libraries, runtimes, and sanitizer availability. Propagate build and test failures for every matrix entry.
- Respect platform runtime and sanitizer limits in [Build and tools](build.md). A successful cross-compile does not establish successful execution on the target architecture.

## Tag-triggered release

- Build release artifacts for supported platform and architecture combinations, package files users need, and include the required version format in each artifact name.
- Derive `MAJOR.MINOR.PATCH` from the pushed version tag, e.g. `v1.2.3`, and `DD.MM.YYYY` from the tagged commit's committer date. Validate the tag and use the same commit date on reruns so artifact names stay stable.
- Create or update the GitHub Release for the pushed tag and attach artifacts. Give the release job required repository permissions; handle an existing release deliberately on reruns.
- Keep unsupported targets or unavailable checks visible in the workflow output instead of claiming they passed.
