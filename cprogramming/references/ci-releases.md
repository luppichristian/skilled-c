# CI and releases

- Use `MAJOR.MINOR.PATCH-DD.MM.YYYY` as the artifact version format.
- For new projects, set up GitHub workflows: run `ci.yml` on pushes and pull requests, and `cd.yml` when a new tag is pushed. The tag workflow builds artifacts and attaches them to a GitHub Release.
- Recommended runners are `ubuntu-latest` for Linux/Unix, `macos-latest` for macOS, and `windows-latest` for Windows.
- Cross-compile for different architectures on these systems when needed.

## Continuous integration

- Use a runner matrix for supported desktop platforms. On each runner, check out the source, select Clang, configure the project's actual build system, and build the requested configurations.
- Run configured project tests, including CTest for CMake projects, and configured formatting or static-analysis checks.
- Respect platform runtime and sanitizer limitations in [Build and tools](build.md). A successful cross-compile does not establish successful execution on the target architecture.

## Tag-triggered release

- Build release artifacts for supported platform and architecture combinations, package files users need, and include the required version format in each artifact name.
- Derive `MAJOR.MINOR.PATCH` from the pushed version tag, e.g. `v1.2.3`, and `DD.MM.YYYY` from the tagged commit's committer date. Validate the tag and use the same commit date on reruns so artifact names stay stable.
- Create or update the GitHub Release for the pushed tag and attach artifacts. Give the release job needed repository permissions and make reruns handle an existing release deliberately.
- Keep unsupported targets or unavailable checks visible in the workflow output instead of claiming they passed.
