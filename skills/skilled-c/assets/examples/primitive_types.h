#pragma once

#include <limits.h>
#include <stddef.h>
#include <stdint.h>

typedef int8_t s8;
typedef uint8_t u8;
typedef int_fast8_t s8x;
typedef uint_fast8_t u8x;
typedef int_least8_t s8y;
typedef uint_least8_t u8y;

typedef int16_t s16;
typedef uint16_t u16;
typedef int_fast16_t s16x;
typedef uint_fast16_t u16x;
typedef int_least16_t s16y;
typedef uint_least16_t u16y;

typedef int32_t s32;
typedef uint32_t u32;
typedef int_fast32_t s32x;
typedef uint_fast32_t u32x;
typedef int_least32_t s32y;
typedef uint_least32_t u32y;

typedef int64_t s64;
typedef uint64_t u64;
typedef int_fast64_t s64x;
typedef uint_fast64_t u64x;
typedef int_least64_t s64y;
typedef uint_least64_t u64y;

static_assert(sizeof(s8) * CHAR_BIT == 8 && sizeof(u8) * CHAR_BIT == 8, "integer width");
static_assert(sizeof(s8x) * CHAR_BIT >= 8 && sizeof(u8x) * CHAR_BIT >= 8, "fast integer width");
static_assert(sizeof(s8y) * CHAR_BIT >= 8 && sizeof(u8y) * CHAR_BIT >= 8, "least integer width");
static_assert(sizeof(s16) * CHAR_BIT == 16 && sizeof(u16) * CHAR_BIT == 16, "integer width");
static_assert(sizeof(s16x) * CHAR_BIT >= 16 && sizeof(u16x) * CHAR_BIT >= 16, "fast integer width");
static_assert(sizeof(s16y) * CHAR_BIT >= 16 && sizeof(u16y) * CHAR_BIT >= 16, "least integer width");
static_assert(sizeof(s32) * CHAR_BIT == 32 && sizeof(u32) * CHAR_BIT == 32, "integer width");
static_assert(sizeof(s32x) * CHAR_BIT >= 32 && sizeof(u32x) * CHAR_BIT >= 32, "fast integer width");
static_assert(sizeof(s32y) * CHAR_BIT >= 32 && sizeof(u32y) * CHAR_BIT >= 32, "least integer width");
static_assert(sizeof(s64) * CHAR_BIT == 64 && sizeof(u64) * CHAR_BIT == 64, "integer width");
static_assert(sizeof(s64x) * CHAR_BIT >= 64 && sizeof(u64x) * CHAR_BIT >= 64, "fast integer width");
static_assert(sizeof(s64y) * CHAR_BIT >= 64 && sizeof(u64y) * CHAR_BIT >= 64, "least integer width");

typedef float f32;
typedef double f64;
typedef size_t sz;
typedef uintptr_t up;
typedef intptr_t sp;
typedef ptrdiff_t pd;

static_assert(sizeof(f32) * CHAR_BIT == 32 && sizeof(f64) * CHAR_BIT == 64, "float width");

/* Set each flag consistently to 1 only after probing the compiler and target. */
#ifndef PROJECT_USE_FLOAT16
#  define PROJECT_USE_FLOAT16 0
#endif
#ifndef PROJECT_USE_INT128
#  define PROJECT_USE_INT128 0
#endif
#ifndef PROJECT_USE_FLOAT128
#  define PROJECT_USE_FLOAT128 0
#endif

#if (PROJECT_USE_FLOAT16 | PROJECT_USE_INT128 | PROJECT_USE_FLOAT128) & ~1
#  error "PROJECT_USE_* flags must be 0 or 1"
#endif

#define PROJECT_HAS_F16    PROJECT_USE_FLOAT16
#define PROJECT_HAS_INT128 PROJECT_USE_INT128
#define PROJECT_HAS_F128   PROJECT_USE_FLOAT128

#if PROJECT_HAS_F16
typedef _Float16 f16;
static_assert(sizeof(f16) * CHAR_BIT == 16, "f16 width");
#endif

#if PROJECT_HAS_INT128
typedef _BitInt(128) s128;
typedef unsigned _BitInt(128) u128;
static_assert(sizeof(s128) * CHAR_BIT == 128 && sizeof(u128) * CHAR_BIT == 128, "integer width");
#endif

#if PROJECT_HAS_F128
typedef _Float128 f128;
static_assert(sizeof(f128) * CHAR_BIT == 128, "f128 width");
#endif
