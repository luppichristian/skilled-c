# Clang tooling

Use the project's `.clang-format` and `.clang-tidy` files. If either file is absent from the project, copy only the missing file from the skill's [formatter configuration](../assets/.clang-format) or [analyzer configuration](../assets/.clang-tidy); do not replace an existing configuration.

- Format C source and header files with `clang-format` using the project configuration. To check formatting without modifying files, use `clang-format --dry-run --Werror` on the intended files.
- Run `clang-tidy` with the project's compilation database when available, for example with `-p build`. CMake's `CMAKE_EXPORT_COMPILE_COMMANDS=ON` produces a compilation database with supported generators such as Ninja and Makefiles.
- The copied default's header filter may not match project headers because it assumes an `include/` path with forward slashes. When checking headers, use an appropriate `--header-filter` override, such as `--header-filter='.*'`, or a narrower expression verified against the project's actual paths. System-header diagnostics remain suppressed unless explicitly enabled.
- When there is no compilation database, pass the actual language version, include paths, target options, and relevant definitions after `--` so that analysis matches the build. Report unavailable tooling or checks rather than claiming they passed.
- The default analyzer configuration includes identifier-naming rules and treats its warnings as errors. Follow the selected project configuration instead of introducing an independent naming style.
