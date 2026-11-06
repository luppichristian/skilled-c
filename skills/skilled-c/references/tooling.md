# Clang tooling

Use available local Clang tools, such as `clangd` for diagnostics and symbol navigation, `clang-format` for formatting, and `clang-tidy` for analysis.

Use the project's `.clang-format` and `.clang-tidy` files. If a needed configuration is absent, use the plugin's [formatter](../assets/.clang-format) and [analyzer](../assets/.clang-tidy) for inspiration when writing project-specific configurations; do not copy them verbatim or replace an existing configuration.

- Format C sources and headers with `clang-format` using project configuration. Check the intended files without modifying them using `clang-format --dry-run --Werror`.
- Run `clang-tidy` with the project's compilation database when available, e.g. `-p build`. CMake's `CMAKE_EXPORT_COMPILE_COMMANDS=ON` produces one with supported generators such as Ninja and Makefiles.
- Use the project's compilation database and target configuration so language mode, includes, defines, and compiler options match the C build. Check header diagnostics in the correct C context; review changes against the project's build and checks.
- The example analyzer's header filter assumes an `include/` path with forward slashes, so may miss project headers. To check headers, use a suitable `--header-filter` override, such as `--header-filter='.*'`, or a narrower expression verified against project paths. System-header diagnostics remain suppressed unless explicitly enabled.
- Without a compilation database, pass the actual language version, include paths, target options, and relevant definitions after `--` so analysis matches the build.
- The example analyzer configuration includes identifier-naming rules and treats its warnings as errors. Follow the selected project configuration instead of adding a separate naming style.
