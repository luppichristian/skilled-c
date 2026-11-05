# Copyright (c) 2026 Christian Luppi. MIT license; see LICENSE.
cmake_minimum_required(VERSION 3.21)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
project(unity_example LANGUAGES C)

include(CTest)
if(BUILD_TESTING)
    include(FetchContent)
    FetchContent_Declare(unity
        GIT_REPOSITORY https://github.com/ThrowTheSwitch/Unity.git
        GIT_TAG 54f864cf6027a50f4cc5424616e9e01e1bb729da
        SOURCE_SUBDIR __fetch_only__
    )
    FetchContent_MakeAvailable(unity)

    # Avoid adding Unity's upstream CMake target and its warning options.
    add_library(unity_local STATIC "${unity_SOURCE_DIR}/src/unity.c")
    target_include_directories(unity_local PUBLIC "${unity_SOURCE_DIR}/src")
    set_target_properties(unity_local PROPERTIES
        C_STANDARD 11
        C_STANDARD_REQUIRED ON
        C_EXTENSIONS OFF
    )

    add_executable(project_tests project_tests.c)
    if(CMAKE_C_COMPILER_ID STREQUAL "Clang" AND
       CMAKE_C_COMPILER_FRONTEND_VARIANT STREQUAL "MSVC")
        # Remove any inherited C23 property before adding the manual flag.
        set_property(TARGET project_tests PROPERTY C_STANDARD)
        target_compile_options(project_tests PRIVATE /clang:-std=gnu23)
    else()
        set_target_properties(project_tests PROPERTIES
            C_STANDARD 23
            C_STANDARD_REQUIRED ON
            C_EXTENSIONS ON
        )
    endif()
    target_link_libraries(project_tests PRIVATE unity_local)
    # Replace the example test and also link the project code under test.
    add_test(NAME project_tests COMMAND project_tests)
endif()
