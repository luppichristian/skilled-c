# Portability

- Isolate platform-specific code as much as possible.
- A module may have different platform or architecture implementations, such as `project_module.h` and `project_module_platform.c`.
- Select the appropriate implementation in the build and keep platform headers and handles behind the interface when practical.
- Define the byte order and integer widths of serialized data. Encode and decode fields explicitly; do not rely on the in-memory layout, padding, or endianness of a C struct. Validate lengths before reading or writing.
- Detect SIMD capabilities and provide a fallback when the host does not support them. Keep the baseline path free of instructions that require the optional feature, and compare the optimized and fallback results on supported targets. Check operating-system support as well as CPU support where the instruction set requires it.

For a WebAssembly target, read [WebAssembly](webassembly.md).
