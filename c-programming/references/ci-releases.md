# CI and releases

- Use `MAJOR.MINOR.PATCH-DD.MM.YYYY` as the artifact version format.
- For new projects, set up GitHub workflows: run `ci.yml` on pushes and pull requests and run `cd.yml` when a new tag is pushed. The tag workflow builds artifacts and attaches them to a GitHub Release.
- Recommended runners are `ubuntu-latest` for Linux/Unix, `macos-latest` for macOS, and `windows-latest` for Windows.
- Cross-compile for different architectures on these systems when needed.

## Continuous integration

- Use a runner matrix for the project's supported desktop platforms. Check out the source, select Clang, configure the project's actual build system, and build the requested configurations on each runner.
- Run the project's tests when they are configured, including CTest for CMake projects. Run formatting or static-analysis checks when those checks are configured for the project.
- Respect the platform's runtime and sanitizer limitations described in [Build and tools](build.md). A successful cross-compile does not establish that a binary was executed successfully on its target architecture.

## Tag-triggered release

- Build release artifacts for the supported platform and architecture combinations, package the files users need, and include the required version format in each artifact name.
- Derive `MAJOR.MINOR.PATCH` from the pushed version tag, such as `v1.2.3`, and derive `DD.MM.YYYY` from the tagged commit's committer date. Validate the version tag and use the same commit date on reruns so artifact names stay stable.
- Create or update the GitHub Release for the pushed tag and attach the built artifacts. Give the release job the repository permissions it needs, and make reruns handle an existing release deliberately.
- Keep unsupported targets or unavailable checks visible in the workflow output instead of claiming they passed.
