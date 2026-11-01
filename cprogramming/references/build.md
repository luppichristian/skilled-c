# Build and tools

## Tools

- Debugger: `gdb`.
- Compiler: `clang`.
- Formatter: `clang-format`.
- Analyzer: `clang-tidy`.
- Web compiler: `emcc`.

## Compilation

- Use the `gnu23` language version.
- Enable `-Wall -Wextra -Wpedantic -Wshadow -Wformat=2 -Wconversion`.
- Define `-D_CRT_SECURE_NO_WARNINGS`.
- Use a static C runtime on all target platforms where supported. On the MSVC ABI, use the debug static CRT (`/MTd`) for debug builds and the release static CRT (`/MT`) for release builds; also generate debug information for the project in debug builds. If the platform requires system libraries to be dynamic, use them and report the exception. Static runtime linkage and debug symbols are separate choices; a static runtime does not imply every runtime dependency is statically linked.
- For development builds, use `-g -fsanitize=address -fno-omit-frame-pointer`. Apply the sanitizer option during compilation and final linking, and use the compiler driver for the link. When AddressSanitizer is unavailable on a requested target, build without it and report the limitation. On Windows, an AddressSanitizer runtime DLL may still be required with a static CRT.
- Clang's AddressSanitizer does not support fully static executables. When the chosen static-runtime setup and sanitizer cannot coexist, retain the supported runtime configuration, omit AddressSanitizer for that build, and report the limitation.
- If a Windows sanitizer build exits with `0xC0000135` before starting, inspect its imported DLLs and locate the matching sanitizer runtime from the selected compiler. Make that runtime discoverable for the test process and rerun; successful linking alone does not prove the executable can start.
- When optimizing, prioritize speed over binary size.
- Use unity builds to merge translation units and improve compilation speed. If combining translation units causes collisions or cannot support the project, fall back to separate compilation and report why.

Unity builds are a compilation technique; they are unrelated to the Unity unit-testing library.

## Clang frontends

The options above use the GNU-style `clang` driver. When using the MSVC-style `clang-cl` frontend, forward the C dialect and warning options with `/clang:`, for example `/clang:-std=gnu23` and `/clang:-Wformat=2`. Use `/Z7` or `/Zi` for debug information and `/clang:-fno-omit-frame-pointer` for frame pointers. Use the frontend's sanitizer option at both compilation and linking, and verify the complete configuration rather than assuming a GNU-style option was accepted.

Probe the requested CRT and sanitizer combination with the actual compiler and linker. For example, Clang 20's `clang-cl` rejects AddressSanitizer with `/MTd`; the GNU-style driver may instead link with a CRT-conflict warning. Treat such a rejection or runtime-library conflict as an unsupported combination, keep the requested debug CRT, and report that the sanitizer was omitted.

## Build systems

Choose Bash (`build.sh`) for simple builds, Make (`Makefile`) for multiple configurations without third-party libraries, and CMake (`CMakeLists.txt`) when the project needs third-party libraries. Put build artifacts in a folder named `build`.

- **Bash:** Call tools directly, support command-line configuration if necessary, and assume tools are present.
- **Make:** Choose it for managing multiple platforms, architectures, or configurations. Do not use third-party libraries unless they are header-only.
- **CMake:** Use the most recent available version and `FetchContent` for third-party libraries. Prefer portable options over compiler-specific arguments.

For CMake, request C23 with extensions and require the selected standard using `CMAKE_C_STANDARD`, `CMAKE_C_EXTENSIONS`, and `CMAKE_C_STANDARD_REQUIRED` when the selected CMake and compiler frontend support that mapping. If CMake cannot generate a C23 flag for `clang-cl`, avoid initializing the affected target with the unsupported C23 standard property, add `/clang:-std=gnu23` to its compile options, and compile-probe the selected dialect. Do not silently fall back to an older C version. Enable unity builds for the project's targets where they work; disable them for a target that cannot be combined safely.

For an MSVC-ABI toolchain, set policy `CMP0091` to `NEW` before the first `project()` or `enable_language()` call. Set `CMAKE_MSVC_RUNTIME_LIBRARY` before creating targets to `MultiThreaded$<$<CONFIG:Debug>:Debug>`. CMake then selects the appropriate static runtime flag for the compiler frontend. Do not pass `clang-cl`-style `/MT` options blindly to a GNU-style `clang` command line.

On Linux, use a toolchain and installed runtime that support the requested static C runtime; a fully static link is appropriate only if the project's other dependencies also support it. On macOS, use the platform-required dynamic system libraries and report that exception. Verify the resulting linkage with available platform tools rather than assuming a compiler flag produced the intended binary.
