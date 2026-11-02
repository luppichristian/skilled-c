# Primitive types

Reuse compatible project definitions. For a new project, put these definitions in an appropriately named common header starting with the complete project license text and applicable copyright notice, followed by `#pragma once`. Include `<limits.h>`, `<stddef.h>`, and `<stdint.h>`.

- For each N in 8, 16, 32, and 64, define `sN` and `uN` as the corresponding `intN_t` and `uintN_t`; define `sNx` and `uNx` as `int_fastN_t` and `uint_fastN_t`. For example, `s16` uses `int16_t` and `u32x` uses `uint_fast32_t`.
- Define `f32` as `float`, `f64` as `double`, `sz` as `size_t`, `up` as `uintptr_t`, `sp` as `intptr_t`, and `pd` as `ptrdiff_t`.
- Use compile-time assertions on `sizeof(type) * CHAR_BIT`: each fixed-width integer and float, including enabled optional types, must have the exact named width; each fast integer must have at least its named width. A float's storage width does not establish IEEE 754 representation.
- Fast, size, and pointer-related types have target-dependent sizes; do not guess fixed widths for them. Use exact-width types for a fixed binary format or ABI. Exact-width and pointer-sized integer types exist only when the implementation provides them. Verify required aliases on each target; never silently substitute a different width. Use types required by the C language, system APIs, and external ABI signatures.

## Optional types

Probe with the actual compiler, language mode, target, and flags, and verify that needed operations and runtime support link successfully. Configure `PROJECT_USE_FLOAT16`, `PROJECT_USE_INT128`, `PROJECT_USE_BITINT128`, and `PROJECT_USE_FLOAT128` consistently as `0` or `1` for all translation units and header consumers. Default each to `0` if undefined; set it to `1` only after a successful probe. A zero default marks an unprobed feature unavailable, not necessarily unsupported by the target.

- When `PROJECT_USE_FLOAT16` is enabled, define `f16` as `_Float16` and check 16-bit storage. Define `PROJECT_HAS_F16` as `PROJECT_USE_FLOAT16`.
- When `PROJECT_USE_INT128` is enabled, define `s128` and `u128` using `__int128` and `unsigned __int128`, using `__extension__` for the typedefs. Otherwise, when `PROJECT_USE_BITINT128` is enabled, use C23 `_BitInt(128)` and `unsigned _BitInt(128)`, only where their ABI is suitable. Define `PROJECT_HAS_INT128` as `1` when either implementation is selected and `0` otherwise. Check both enabled aliases have 128-bit storage.
- When `PROJECT_USE_FLOAT128` is enabled, define `f128` as `__float128`, or adapt it to a supported 128-bit float such as `_Float128`; check 128-bit storage. Define `PROJECT_HAS_F128` as `PROJECT_USE_FLOAT128`.

Always expose `PROJECT_HAS_F16`, `PROJECT_HAS_INT128`, and `PROJECT_HAS_F128` as `0` or `1` so callers can avoid unavailable aliases. Define each optional alias only when its feature is enabled.
