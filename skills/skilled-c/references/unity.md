# Unity unit tests

Unity's core is `unity.c`, `unity.h`, and `unity_internals.h`; it is not header-only or bundled with this plugin.

- Compile and link `unity.c`, test source, and code under test into a test executable. Add Unity and project header directories to its include path.
- For the default hand-written runner, define `setUp` and `tearDown`, even if empty. Start the suite with `UNITY_BEGIN()`, register each case with `RUN_TEST`, and return `UNITY_END()` from `main`. A generated runner or different Unity configuration may supply those functions instead.
- Exercise observable behavior, representative branches, boundary values, and relevant error cases. Keep test code separate from production code.
- With CMake, register the executable with CTest and propagate its exit status. For script or Make builds, run it in the test command and propagate failures.

## CMake integration

Include CTest; place dependency acquisition, the Unity library, test executable, and test registration inside `if(BUILD_TESTING)`. Use `FetchContent_Declare` with the name `unity` to fetch `https://github.com/ThrowTheSwitch/Unity.git` at an immutable revision, for example `54f864cf6027a50f4cc5424616e9e01e1bb729da`. The address is a build dependency, not documentation the model must retrieve. Respect project network constraints.

To avoid Unity's upstream CMake target and its warning options that can fail with `clang-cl`, set `SOURCE_SUBDIR` to the nonexistent `__fetch_only__`, call `FetchContent_MakeAvailable(unity)`, and build `${unity_SOURCE_DIR}/src/unity.c` as a local static library with `${unity_SOURCE_DIR}/src` as a public include directory. For example, build this library as required C11 with extensions off.

Create the test executable from the test source, link the local Unity library and project target or sources under test, and register it with `add_test`. For the requested GNU C23 mode, configure the test target for required C23 with extensions; for MSVC-style `clang-cl`, use `/clang:-std=gnu23` instead. Probe the mode with the selected compiler as in [Build and tools](build.md).

Support `-DFETCHCONTENT_SOURCE_DIR_UNITY=<local-unity-source>` to use a local checkout without downloading. This override bypasses `GIT_TAG`; inspect the local revision when available because it may differ from the pin.
