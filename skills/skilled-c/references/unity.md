# Unity unit tests

Unity's core is `unity.c`, `unity.h`, and `unity_internals.h`; it is not header-only or bundled with this plugin. Compile it with the tests and code under test, and propagate the test runner's exit status. Keep tests separate from production code; exercise observable behavior, boundaries, and relevant errors. For a hand-written runner, adapt [project_tests.c](../assets/examples/project_tests.c); generated runners or custom Unity configurations may supply the setup functions.

## CMake integration

Adapt the [CMake/FetchContent project](../assets/examples/CMakeLists.txt). Replace the illustrative test, link the project code under test, and respect project network constraints. The example pins Unity, acquires it only when testing is enabled, builds its core locally to avoid upstream `clang-cl` warning issues, and registers the runner with CTest. Probe GNU C23 with the selected compiler as in [Build and tools](build.md).

Support `-DFETCHCONTENT_SOURCE_DIR_UNITY=<local-unity-source>` to use a local checkout without downloading. This bypasses the pin; inspect the local revision when available because it may differ. For other build systems, run the test executable from the test command.
