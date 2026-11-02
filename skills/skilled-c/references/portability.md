# Portability

- Isolate platform-specific code as much as possible.
- A module may have different platform or architecture implementations, such as `project_module.h` and `project_module_platform.c`.
- Select the appropriate implementation in the build; keep platform headers and handles behind the interface when practical.
- Define serialized data's byte order and integer widths. Encode and decode fields explicitly; do not rely on a C struct's in-memory layout, padding, or endianness. Validate lengths before reading or writing.
- Detect SIMD capabilities and provide a fallback when the host lacks them. Keep the baseline path free of instructions requiring the optional feature; compare optimized and fallback results on supported targets. Check operating-system as well as CPU support where required by the instruction set.

For a WebAssembly target, read [WebAssembly](webassembly.md).
