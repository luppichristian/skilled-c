/* Copyright (c) 2026 Christian Luppi. MIT; see LICENSE. */
#pragma once

#include <limits.h>
#include <stddef.h>
#include <stdint.h>

#define SKILLED_C_INTEGER_TYPES(n)                                                                  \
  typedef int##n##_t s##n;                                                                          \
  typedef uint##n##_t u##n;                                                                         \
  typedef int_fast##n##_t s##n##x;                                                                  \
  typedef uint_fast##n##_t u##n##x;                                                                 \
  static_assert(sizeof(s##n) * CHAR_BIT == (n) && sizeof(u##n) * CHAR_BIT == (n), "integer width"); \
  static_assert(sizeof(s##n##x) * CHAR_BIT >= (n) && sizeof(u##n##x) * CHAR_BIT >= (n), "fast integer width")

SKILLED_C_INTEGER_TYPES(8);
SKILLED_C_INTEGER_TYPES(16);
SKILLED_C_INTEGER_TYPES(32);
SKILLED_C_INTEGER_TYPES(64);
#undef SKILLED_C_INTEGER_TYPES

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
#ifndef PROJECT_USE_BITINT128
#  define PROJECT_USE_BITINT128 0
#endif
#ifndef PROJECT_USE_FLOAT128
#  define PROJECT_USE_FLOAT128 0
#endif

#if (PROJECT_USE_FLOAT16 | PROJECT_USE_INT128 | PROJECT_USE_BITINT128 | PROJECT_USE_FLOAT128) & ~1
#  error "PROJECT_USE_* flags must be 0 or 1"
#endif

#define PROJECT_HAS_F16  PROJECT_USE_FLOAT16
#define PROJECT_HAS_F128 PROJECT_USE_FLOAT128

#if PROJECT_HAS_F16
typedef _Float16 f16;
static_assert(sizeof(f16) * CHAR_BIT == 16, "f16 width");
#endif

#if PROJECT_USE_INT128
__extension__ typedef __int128 s128;
__extension__ typedef unsigned __int128 u128;
#  define PROJECT_HAS_INT128 1
#elif PROJECT_USE_BITINT128
typedef _BitInt(128) s128;
typedef unsigned _BitInt(128) u128;
#  define PROJECT_HAS_INT128 1
#else
#  define PROJECT_HAS_INT128 0
#endif

#if PROJECT_HAS_INT128
static_assert(sizeof(s128) * CHAR_BIT == 128 && sizeof(u128) * CHAR_BIT == 128, "integer width");
#endif

#if PROJECT_HAS_F128
typedef __float128 f128;
static_assert(sizeof(f128) * CHAR_BIT == 128, "f128 width");
#endif
