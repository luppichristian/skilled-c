# Testing

## Unit tests

- When unit tests are requested, integrate Unity into the project's build. For integration and test runners, read [Unity unit tests](unity.md).
- Make's third-party restriction excludes Unity. When a new project needs Unity, choose another suitable build system rather than making an exception to that restriction.
- Use white-box techniques to cover statements, paths, and loops; use black-box equivalence class partitioning and boundary value analysis.

## End-to-end tests

- Launch programs with CTest or scripts. Use observer utilities when they make sense.
- For runtime applications, use the patterns in [Record/replay testing](replay-testing.md).

## Organization

- Keep normal `src` code isolated from `test` code.
- When using CMake, integrate all tests with CTest.
- Tests may not be necessary for minimal projects.
