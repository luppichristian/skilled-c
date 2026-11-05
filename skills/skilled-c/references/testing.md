# Testing

## Unit tests

- Use Unity for unit tests; see [Unity unit tests](unity.md) for integration and runners.
- Make's third-party restriction excludes Unity. When a new project needs Unity, choose another suitable build system instead of making an exception.
- Use white-box techniques to cover statements, paths, and loops; use black-box equivalence class partitioning and boundary value analysis.
- Identify important state transitions and interactions as well as individual branches. Exercise representative common, boundary, and failure cases, including combinations that can invalidate shared assumptions; do not assume a wrapper or dispatch table removes underlying cases.

## End-to-end tests

- Launch programs with CTest or scripts; use observer utilities when sensible.
- For runtime applications, use the patterns in [Record/replay testing](replay-testing.md).

## Organization

- Keep normal `src` code isolated from `test` code.
- With CMake, integrate all tests with CTest.
- Tests may not be necessary for minimal projects.
