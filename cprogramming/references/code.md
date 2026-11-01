# Code conventions

## Modules

- A module consists of a header (`.h`) and an implementation (`.c`), named `project_module.h` and `project_module.c`.
- Expose the module's functionality in its header. A module may include other modules from its header or implementation.
- Prefer fewer modules that group related functionality.

## Style

- Format, indent, and space code for human readability. Follow the project's `clang-format` and `clang-tidy` configuration rather than inventing a separate formatting or naming scheme. Use [Clang tooling](tooling.md) to install the skill's defaults when those project files are missing.
- Keep code minimal and simple without compromising functionality. Use consistent case conventions for each group: functions, types, variables, globals, constants, and macros.
- Use fixed-size types as much as possible. Use custom types instead of built-in ones, including `u32`, `u16`, `s32`, `s8`, `f32`, `f64`, `u32x`, `s16x`, `sz`, `up`, `sp`, and `pd`.
- Define the signed `s8`/`s16`/`s32`/`s64` and unsigned `u8`/`u16`/`u32`/`u64` families using the corresponding fixed-width types from `<stdint.h>`. The `x` variants use the corresponding `int_fastN_t` or `uint_fastN_t` types, such as `s16x` and `u32x`.
- Define `sz` as `size_t`, `up` as `uintptr_t`, `sp` as `intptr_t`, and `pd` as `ptrdiff_t`. Reuse existing definitions where appropriate; do not guess unresolved aliases.
- Define `f32` as `float` and `f64` as `double`. Specify and check the widths of fixed-size aliases at compile time; document the target-dependent sizes of fast, size, and pointer-related types. Width alone does not establish a particular floating-point representation.
- Where supported by the selected compiler and target, also define `f16`, `s128`, `u128`, and `f128` with checked widths and feature indicators. Do not silently replace an unavailable type with one of a different width.
- Use [Primitive types](types.md) for the complete definitions and portability constraints.
- Allow global variables only in implementation files; prefer local persistent variables over globals.
- Define structs, enums, and unions with `typedef`, for example `typedef struct { } struct_name;`. Never add an `_f` suffix to type definitions.
- Use only C-style `/* ... */` comments, not `//` comments.
- Use `const` and `constexpr` as much as possible. Prefer complete words for types and functions over obscure abbreviations.
- In C23, `constexpr` declares objects, not functions, and its initializer must satisfy the language's constant-expression requirements. Use `const` for values initialized at runtime and verify compiler support for the selected dialect.
- Base dynamic memory management around arenas; build more specialized allocators on top when necessary. For allocation and lifetime decisions, read [Arena allocation](arenas.md).
- For pointer, arithmetic, string, and resource invariants, read [C correctness](correctness.md).

## API results

Prefer returning an object or handle whose validity can be checked over returning a null pointer directly, where practical. An invalid object must be safe to pass to its operations and cleanup: operations should do no harmful work and must still report failure where success is checked. Document how callers check validity and operation results. Status codes and `errno` are also acceptable; respect required external APIs and platform interfaces.

For public APIs, state who owns each returned resource, how long borrowed data remains valid, and how and when resources are released. Validate external input through the normal error path rather than relying on assertions. On failure, leave outputs in a documented state and release acquired resources unless their ownership is explicitly transferred to the caller.

## Comments and API documentation

- Use the markers `$TODO`, `$HACK`, `$FIXME`, `$NOTE`, `$DEPRECATED`, `$INCOMPLETE`, and `$CLEANUP`.
- Document all functions and types in module headers with compact comments. Function documentation must describe behavior, each parameter and its accepted range, return values, and thread safety.
- For structs, enums, and unions, document only the members that need explanation for users.
- In implementations, comment only nontrivial details or things maintainers need to remember.

## Assertions

- Use as many nonredundant assertions as possible to check expected execution conditions, not to validate parameters or inputs.
- Cover casts, statements, and code paths. Assert when an unimplemented or unfinished code path is reached.
- Prefer compile-time assertions when they achieve the same result as runtime assertions. Use compile-time assertions for required struct or union sizes, alignments, and other attributes.
