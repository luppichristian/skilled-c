# Unity unit tests

When the user wants unit tests, integrate Unity into the project's build. Its core consists of `unity.c`, `unity.h`, and `unity_internals.h`; it is not header-only. This skill does not bundle Unity.

- Compile and link `unity.c`, the test source, and the code under test into a test executable. Add the Unity and project header directories to that executable's include path.
- For the default hand-written runner, define both `setUp` and `tearDown` functions, even if they are empty. Start the suite with `UNITY_BEGIN()`, register each case with `RUN_TEST`, and return `UNITY_END()` from `main`. A generated runner or a different Unity configuration may supply those functions instead.
- Exercise observable behavior, representative branches, boundary values, and relevant error cases. Keep test code separate from production code.
- With CMake, register the executable with CTest and propagate its exit status. For script or Make builds, run it as part of the test command and propagate failures.

For CMake, declare Unity with `FetchContent` and pin it to an immutable revision. Support the `FETCHCONTENT_SOURCE_DIR_UNITY` override so an existing local source tree can be used without downloading it. If obtaining the dependency requires network access, respect the project's constraints and report when it is unavailable.

For example, when the project has `tests/project_tests.c`:

```cmake
include(CTest)
if(BUILD_TESTING)
    include(FetchContent)
    FetchContent_Declare(unity
        GIT_REPOSITORY https://github.com/ThrowTheSwitch/Unity.git
        GIT_TAG 54f864cf6027a50f4cc5424616e9e01e1bb729da
        SOURCE_SUBDIR __fetch_only__
    )
    FetchContent_MakeAvailable(unity)

    add_library(unity_local STATIC "${unity_SOURCE_DIR}/src/unity.c")
    target_include_directories(unity_local PUBLIC "${unity_SOURCE_DIR}/src")
    set_target_properties(unity_local PROPERTIES
        C_STANDARD 11
        C_STANDARD_REQUIRED ON
        C_EXTENSIONS OFF
    )
    add_executable(project_tests tests/project_tests.c)
    if(CMAKE_C_COMPILER_ID STREQUAL "Clang" AND
       CMAKE_C_COMPILER_FRONTEND_VARIANT STREQUAL "MSVC")
        target_compile_options(project_tests PRIVATE /clang:-std=gnu23)
    else()
        set_target_properties(project_tests PROPERTIES
            C_STANDARD 23
            C_STANDARD_REQUIRED ON
            C_EXTENSIONS ON
        )
    endif()
    target_link_libraries(project_tests PRIVATE unity_local)
    # Also link the project target or sources under test.
    add_test(NAME project_tests COMMAND project_tests)
endif()
```

The non-existent `SOURCE_SUBDIR` makes the source available without adding Unity's upstream CMake target; the local target builds its core directly and avoids inheriting upstream warning options that can fail with `clang-cl`. The test target uses the requested GNU C23 mode; probe that mode with the selected compiler as described in [Build and tools](build.md). Configure with `-DFETCHCONTENT_SOURCE_DIR_UNITY=<local-unity-source>` to use an existing checkout. This override bypasses `GIT_TAG`; inspect the local source revision when available and report a mismatch or an unverified version rather than claiming the pin was enforced. The repository address above is a build dependency, not documentation the model must retrieve.
