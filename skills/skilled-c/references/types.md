# Primitive types

Reuse compatible project definitions; for a new project, use [primitive_types.h](../assets/examples/primitive_types.h) for inspiration when defining the required aliases and compile-time width checks. Tailor the header to the project instead of copying the example verbatim.

Integer aliases use no suffix for exact-width types, `x` for fast types, and `y` for least-width types. Fast, least, size, and pointer-related types have target-dependent sizes; do not guess fixed widths. Use exact-width types for a fixed binary format or ABI. Exact-width and pointer-sized integer types exist only when the implementation provides them. Verify required aliases per target; never silently substitute a different width. Use types required by the C language, system APIs, and external ABI signatures. Float storage width does not establish IEEE 754 representation.

## Optional types

`_Float16` and `_Float128` are optional, and `_BitInt(128)` requires a sufficient `BITINT_MAXWIDTH`. Probe the actual compiler, language mode, target, and flags; verify that needed operations and runtime support link successfully. Set the example's `PROJECT_USE_*` flags to `1` only after successful probes, consistently across translation units and header consumers. The default `0` means unprobed, not necessarily unsupported; `PROJECT_HAS_*` lets callers check availability. Use `_BitInt(128)` only where its ABI is suitable.
