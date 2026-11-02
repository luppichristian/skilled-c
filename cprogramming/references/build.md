# Build and tools

Check that the selected compiler, target, and tools support requested options; explain limitations rather than claiming unverified support.

## Tools

- Debugger: `gdb`.
- Compiler: `clang`.
- Formatter: `clang-format`.
- Analyzer: `clang-tidy`.
- Web compiler: `emcc`.

## Compilation

- Use `gnu23`.
- Enable `-Wall -Wextra -Wpedantic -Wshadow -Wformat=2 -Wconversion`.
- Define `-D_CRT_SECURE_NO_WARNINGS`.
- Use a static C runtime on all targets where supported. On the MSVC ABI, use the debug static CRT (`/MTd`) for debug builds and release static CRT (`/MT`) for release builds; also generate project debug information in debug builds. Use required dynamic system libraries and report the exception. Static runtime linkage and debug symbols are separate choices; a static runtime does not imply every runtime dependency is statically linked.
- For development builds, use `-g -fsanitize=address -fno-omit-frame-pointer`. Apply the sanitizer option during compilation and final linking, using the compiler driver to link. If AddressSanitizer is unavailable on a requested target, build without it and report the limitation. On Windows, a sanitizer runtime DLL may still be required with a static CRT.
- Clang's AddressSanitizer does not support fully static executables. If the chosen static-runtime setup and sanitizer cannot coexist, retain the supported runtime configuration, omit AddressSanitizer for that build, and report the limitation.
- If a Windows sanitizer build exits with `0xC0000135` before starting, inspect imported DLLs and locate the selected compiler's matching sanitizer runtime. Make it discoverable to the test process and rerun; successful linking alone does not prove the executable can start.
- When optimizing, prioritize speed over binary size.
- Use unity builds to merge translation units and improve compilation speed. If combining them causes collisions or cannot support the project, fall back to separate compilation and report why.

Unity builds are a compilation technique; they are unrelated to the Unity unit-testing library.

## Clang frontends

The options above use the GNU-style `clang` driver. With MSVC-style `clang-cl`, forward C dialect and warning options with `/clang:`, e.g. `/clang:-std=gnu23` and `/clang:-Wformat=2`. Use `/Z7` or `/Zi` for debug information and `/clang:-fno-omit-frame-pointer` for frame pointers. Use the frontend's sanitizer option at compilation and linking; verify the complete configuration rather than assuming a GNU-style option was accepted.

Probe the requested CRT/sanitizer combination with the actual compiler and linker. For example, Clang 20's `clang-cl` rejects AddressSanitizer with `/MTd`; the GNU-style driver may instead link with a CRT-conflict warning. Treat either rejection or runtime-library conflict as unsupported, keep the requested debug CRT, and report that the sanitizer was omitted.

## Build systems

Choose Bash (`build.sh`) for simple builds, Make (`Makefile`) for multiple configurations without third-party libraries, and CMake (`CMakeLists.txt`) when third-party libraries are needed. Put artifacts in `build`.

- **Bash:** Call tools directly, support command-line configuration if necessary, and assume tools are present.
- **Make:** Use for multiple platforms, architectures, or configurations. Do not use third-party libraries unless they are header-only.
- **CMake:** Use the most recent available version and `FetchContent` for third-party libraries. Prefer portable options over compiler-specific arguments.

For CMake, request C23 with extensions and require the standard using `CMAKE_C_STANDARD`, `CMAKE_C_EXTENSIONS`, and `CMAKE_C_STANDARD_REQUIRED` when the selected CMake and frontend support that mapping. If CMake cannot generate a C23 flag for `clang-cl`, do not initialize the affected target with the unsupported C23 standard property; add `/clang:-std=gnu23` to its compile options and compile-probe the dialect. Do not silently fall back to older C. Enable unity builds for project targets where they work; disable them for targets that cannot be combined safely.

For an MSVC-ABI toolchain, set policy `CMP0091` to `NEW` before the first `project()` or `enable_language()` call. Before creating targets, set `CMAKE_MSVC_RUNTIME_LIBRARY` to `MultiThreaded$<$<CONFIG:Debug>:Debug>`; CMake selects the appropriate static runtime flag for the frontend. Do not pass `clang-cl`-style `/MT` options blindly to GNU-style `clang`.

On Linux, use a toolchain and installed runtime supporting the requested static C runtime; fully static linking is appropriate only if other project dependencies also support it. On macOS, use platform-required dynamic system libraries and report the exception. Verify linkage with available platform tools rather than assuming a compiler flag produced the intended binary.
