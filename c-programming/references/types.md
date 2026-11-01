# Primitive types

Use the project's existing compatible definitions when present. For a new project, put the following definitions in an appropriately named common header. Replace the illustrative first comment with the project's complete license text and applicable copyright notice before using the header. The optional-type configuration macros shown here must be set consistently for the target by the project configuration.

```c
/* Project license text and applicable copyright notice. */
#pragma once

#include <limits.h>
#include <stddef.h>
#include <stdint.h>

typedef int8_t s8;
typedef int16_t s16;
typedef int32_t s32;
typedef int64_t s64;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

typedef int_fast8_t s8x;
typedef int_fast16_t s16x;
typedef int_fast32_t s32x;
typedef int_fast64_t s64x;
typedef uint_fast8_t u8x;
typedef uint_fast16_t u16x;
typedef uint_fast32_t u32x;
typedef uint_fast64_t u64x;

typedef float f32;
typedef double f64;
typedef size_t sz;
typedef uintptr_t up;
typedef intptr_t sp;
typedef ptrdiff_t pd;

#define ASSERT_TYPE_BITS(type, bits) \
    static_assert(sizeof(type) * CHAR_BIT == (bits), #type " has the wrong size")
#define ASSERT_MIN_TYPE_BITS(type, bits) \
    static_assert(sizeof(type) * CHAR_BIT >= (bits), #type " is too small")

ASSERT_TYPE_BITS(s8, 8);
ASSERT_TYPE_BITS(s16, 16);
ASSERT_TYPE_BITS(s32, 32);
ASSERT_TYPE_BITS(s64, 64);
ASSERT_TYPE_BITS(u8, 8);
ASSERT_TYPE_BITS(u16, 16);
ASSERT_TYPE_BITS(u32, 32);
ASSERT_TYPE_BITS(u64, 64);
ASSERT_TYPE_BITS(f32, 32);
ASSERT_TYPE_BITS(f64, 64);

ASSERT_MIN_TYPE_BITS(s8x, 8);
ASSERT_MIN_TYPE_BITS(s16x, 16);
ASSERT_MIN_TYPE_BITS(s32x, 32);
ASSERT_MIN_TYPE_BITS(s64x, 64);
ASSERT_MIN_TYPE_BITS(u8x, 8);
ASSERT_MIN_TYPE_BITS(u16x, 16);
ASSERT_MIN_TYPE_BITS(u32x, 32);
ASSERT_MIN_TYPE_BITS(u64x, 64);

/* Set these to 1 only after probing the selected compiler and target. */
#ifndef PROJECT_USE_FLOAT16
#define PROJECT_USE_FLOAT16 0
#endif
#ifndef PROJECT_USE_INT128
#define PROJECT_USE_INT128 0
#endif
#ifndef PROJECT_USE_BITINT128
#define PROJECT_USE_BITINT128 0
#endif
#ifndef PROJECT_USE_FLOAT128
#define PROJECT_USE_FLOAT128 0
#endif

#define PROJECT_HAS_F16 PROJECT_USE_FLOAT16
#define PROJECT_HAS_F128 PROJECT_USE_FLOAT128

#if PROJECT_HAS_F16
typedef _Float16 f16;
ASSERT_TYPE_BITS(f16, 16);
#endif

#if PROJECT_USE_INT128
__extension__ typedef __int128 s128;
__extension__ typedef unsigned __int128 u128;
#define PROJECT_HAS_INT128 1
#elif PROJECT_USE_BITINT128
typedef _BitInt(128) s128;
typedef unsigned _BitInt(128) u128;
#define PROJECT_HAS_INT128 1
#else
#define PROJECT_HAS_INT128 0
#endif

#if PROJECT_HAS_INT128
ASSERT_TYPE_BITS(s128, 128);
ASSERT_TYPE_BITS(u128, 128);
#endif

#if PROJECT_HAS_F128
typedef __float128 f128;
ASSERT_TYPE_BITS(f128, 128);
#endif

#undef ASSERT_MIN_TYPE_BITS
#undef ASSERT_TYPE_BITS
```

The integer types without `x` and the floating-point aliases have the exact widths stated in their names; the compile-time assertions check their storage sizes in bits. The `x` integer types are fast types with at least the indicated width; their actual width can vary by target. `sz`, `up`, `sp`, and `pd` likewise use their underlying standard types and have target-dependent sizes, available as `sizeof(type) * CHAR_BIT`. Do not impose a guessed fixed width on them. Use exact-width types for a fixed binary format or ABI. The floating-point checks establish storage width, not IEEE 754 representation.

Probe optional types using the actual compiler, language mode, target, and flags, then configure the corresponding `PROJECT_USE_*` values as `0` or `1` in a configuration shared by all translation units and consumers of the header. For `f16`, probe `_Float16`. For `s128` and `u128`, probe the illustrated `__int128` extension or C23 `_BitInt(128)` implementation; use the latter only where its ABI is suitable. For `f128`, probe `__float128`, or adapt the typedef to a supported 128-bit floating type such as `_Float128`. Check that needed operations and runtime support link successfully. Expose the resulting `PROJECT_HAS_F16`, `PROJECT_HAS_INT128`, and `PROJECT_HAS_F128` flags so callers can avoid unavailable aliases. The example's zero defaults mean an unprobed feature is unavailable; they do not mean the target cannot support it.

Exact-width integer types and pointer-sized integer types are only available when the implementation provides them. Verify that required aliases exist on each target; do not silently replace them with a type of a different width. Use types required by the C language, system APIs, and external ABIs where their signatures require them.
