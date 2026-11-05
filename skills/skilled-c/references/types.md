# Primitive types

Reuse compatible project definitions; for a new project, adapt [primitive_types.h](../assets/examples/primitive_types.h) as a common header. Preserve the example's [MIT license](../assets/examples/LICENSE) and add the destination project's license and copyright. The example defines the required aliases and compile-time width checks.

Fast, size, and pointer-related types have target-dependent sizes; do not guess fixed widths. Use exact-width types for a fixed binary format or ABI. Exact-width and pointer-sized integer types exist only when the implementation provides them. Verify required aliases per target; never silently substitute a different width. Use types required by the C language, system APIs, and external ABI signatures. Float storage width does not establish IEEE 754 representation.

## Optional types

Probe with the actual compiler, language mode, target, and flags; verify needed operations and runtime support link successfully. Configure the example's `PROJECT_USE_*` flags consistently as `0` or `1` for all translation units and header consumers. Set a flag to `1` only after a successful probe; its zero default marks an unprobed feature unavailable, not necessarily unsupported. Use `_BitInt(128)` only where its ABI is suitable, and adapt `__float128` to another supported 128-bit float such as `_Float128` when appropriate. Always expose the `PROJECT_HAS_*` flags so callers can avoid unavailable aliases.
