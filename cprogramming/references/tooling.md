# Clang tooling

Use the project's `.clang-format` and `.clang-tidy` files. If either is absent, copy only the missing file from the skill's [formatter](../assets/.clang-format) or [analyzer](../assets/.clang-tidy) configuration; do not replace an existing one.

- Format C sources and headers with `clang-format` using project configuration. Check without modifying files using `clang-format --dry-run --Werror` on the intended files.
- Run `clang-tidy` with the project's compilation database when available, e.g. `-p build`. CMake's `CMAKE_EXPORT_COMPILE_COMMANDS=ON` produces one with supported generators such as Ninja and Makefiles.
- The copied default's header filter may not match project headers because it assumes an `include/` path with forward slashes. To check headers, use a suitable `--header-filter` override, such as `--header-filter='.*'`, or a narrower expression verified against actual project paths. System-header diagnostics remain suppressed unless explicitly enabled.
- Without a compilation database, pass the actual language version, include paths, target options, and relevant definitions after `--` so analysis matches the build. Report unavailable tooling or checks rather than claiming they passed.
- The default analyzer configuration includes identifier-naming rules and treats its warnings as errors. Follow the selected project configuration instead of introducing a separate naming style.
