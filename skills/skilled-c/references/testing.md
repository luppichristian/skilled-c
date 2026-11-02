# Testing

## Unit tests

- Use Unity for unit tests; see [Unity unit tests](unity.md) for integration and runners.
- Make's third-party restriction excludes Unity. When a new project needs Unity, choose another suitable build system rather than making an exception to that restriction.
- Use white-box techniques to cover statements, paths, and loops; use black-box equivalence class partitioning and boundary value analysis.

## End-to-end tests

- Launch programs with CTest or scripts; use observer utilities when sensible.
- For runtime applications, use the patterns in [Record/replay testing](replay-testing.md).

## Organization

- Keep normal `src` code isolated from `test` code.
- When using CMake, integrate all tests with CTest.
- Tests may not be necessary for minimal projects.
