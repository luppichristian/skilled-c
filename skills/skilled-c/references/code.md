# Code conventions

## Modules

- A module has a header (`.h`) and implementation (`.c`), named `project_module.h` and `project_module.c`.
- Expose functionality in the header. Both header and implementation may include other modules.
- Prefer fewer modules grouping related functionality.

## Style

- Format, indent, and space code for readability. Follow project `clang-format` and `clang-tidy` configuration rather than invent a formatting or naming scheme. See [Clang tooling](tooling.md) for configuration and defaults.
- Keep code minimal and simple without compromising functionality. Use consistent case within each group: functions, types, variables, globals, constants, and macros.
- Use fixed-size types whenever possible and custom types instead of built-ins, including `u32`, `u16`, `s32`, `s8`, `f32`, `f64`, `u32x`, `s16x`, `sz`, `up`, `sp`, and `pd`.
- Define signed `s8`/`s16`/`s32`/`s64` and unsigned `u8`/`u16`/`u32`/`u64` with corresponding fixed-width `<stdint.h>` types. The `x` variants use corresponding `int_fastN_t` or `uint_fastN_t` types, such as `s16x` and `u32x`.
- Define `sz` as `size_t`, `up` as `uintptr_t`, `sp` as `intptr_t`, and `pd` as `ptrdiff_t`. Reuse existing definitions where appropriate; do not guess unresolved aliases.
- Define `f32` as `float` and `f64` as `double`. Specify and compile-time check fixed-size alias widths; document target-dependent sizes of fast, size, and pointer-related types. Width alone does not establish floating-point representation.
- Where supported by the selected compiler and target, also define `f16`, `s128`, `u128`, and `f128` with checked widths and feature indicators. Do not silently replace an unavailable type with one of a different width.
- Use [Primitive types](types.md) for the complete definitions and portability constraints.
- Allow global variables only in implementation files; prefer local persistent variables over globals.
- Define structs, enums, and unions with `typedef`, e.g. `typedef struct { } struct_name;`. Never add an `_f` suffix to type definitions.
- Use only C-style `/* ... */` comments, not `//` comments.
- Use `const` and `constexpr` as much as possible. Prefer complete words over obscure abbreviations for types and functions.
- In C23, `constexpr` declares objects, not functions; its initializer must satisfy constant-expression requirements. Use `const` for runtime-initialized values and verify compiler support for the selected dialect.
- Base dynamic memory management around arenas; build specialized allocators on top when needed. For allocation and lifetime decisions, read [Arena allocation](arenas.md).
- For pointer, arithmetic, string, and resource invariants, read [C correctness](correctness.md).

## Data flow and state

Trace a subsystem's inputs, outputs, ownership, mutations, and side effects. Describe observable operation across calls or frames, not just one helper's name. Where cases have the same intended effects, a common representation or operation can reduce callers' special cases. When simplifying an interface, check every underlying path's effects; hiding a branch does not remove its possible behavior.

Identify authoritative data and derive other views from it when practical. If retaining a cache or copy, define its update or invalidation, ownership, and how readers see changes. Choose recomputation or caching according to the workload. Before overwriting useful inputs or intermediate results, consider whether undo, diagnostics, another consumer, or recovery needs them; retain or reconstruct them with an appropriate lifetime and storage bound when needed.

For work benefiting from batching or deferred execution, a command buffer can separate recording a request from carrying it out. Define command order, referenced data ownership and lifetime, error reporting, and when execution is complete. Do not assume recording a command has already performed its effect.

## API results

Where practical, prefer returning an object or handle with checkable validity over a null pointer. An invalid object must be safe for its operations and cleanup: operations should do no harmful work and must report failure where success is checked. Document how callers check validity and results. Status codes and `errno` are also acceptable; respect required external APIs and platform interfaces.

For public APIs, state ownership of each returned resource, borrowed-data lifetime, and how and when resources are released. Validate external input through normal error paths, not assertions. On failure, leave outputs in a documented state; release acquired resources unless ownership is explicitly transferred to the caller.

When an empty value is meaningful, design and document a safe empty state and its operations. For suitable types, C initialization such as `T value = {0};` can produce that state. Do not assume `memset` to zero has the required representation for every pointer, floating-point type, or other object. An immutable sentinel can make absent read-only values safe to inspect, but it must never be treated as writable storage. Distinguish an empty result from failure whenever callers need to act on the difference.

An operation may return useful partial results alongside diagnostics when continuing is safe; state which results are valid and which failures prevent further work. A log or message list does not replace a required failure status. When practical, check prerequisites and acquire resources before changing important state; still handle later failures and preserve or report the resulting state.

## Object identity

If references can outlive a slot's occupant, use a stable identity or a generation-checked handle instead of assuming a reused address still names the same object. Validate the storage lifetime, index, occupancy, and generation before accessing the object. Define deletion, concurrent access, generation wraparound, and what happens to already borrowed pointers. If deletion can occur concurrently, hold a lock, pin, or equivalent lifetime guarantee across validation and use; checking a generation alone does not prevent a subsequent deletion.

## Contexts and callbacks

Group related state and dependencies that must be passed together in an explicit context object. Independent instances or threads can use separate contexts; document initialization, cleanup, ownership, lifetime, and whether the context or dependencies are shared. Separate contexts do not make shared dependencies thread-safe; use [Concurrency](concurrency.md) for synchronization.

When callers supply behavior, pair a typed callback function pointer with an opaque user-data pointer. Document the callback, user data, and argument lifetimes; when and on which thread it runs; and whether it may reenter the API. For registered callbacks, specify unregistration and when in-flight calls have finished so user data can be released safely. Respect existing project and external callback interfaces.

## Macros

Prefer functions or `static inline` functions when a macro is unnecessary. In function-like macros, parenthesize expression arguments in the expansion and the result of an expression macro. Evaluate each argument once where practical; document repeated evaluation so callers can avoid side effects. Wrap multi-statement macros in `do { ... } while (0)` when they must behave as one statement. There, `break` and `continue` target the wrapper, not an enclosing caller loop.

## Intrusive containers

When suitable, embed links in caller-owned objects so containers need no separate nodes. Specify who owns and releases objects, when to unlink them, which mutations invalidate iteration, and how concurrent access is synchronized. Use separate link fields for simultaneous membership in multiple containers.

Choose arrays, linked nodes, or another representation from the actual access and mutation pattern. Lists can support stable node addresses, insertion, and splicing; dependent pointer traversal and per-node overhead can be costly. A linked node can hold a batch of elements to reduce link and allocation overhead. Measure representative workloads, and do not confuse stable addresses with validity after removal or reuse.

## Diagnostics

When logging or profiling is needed, reuse project facilities where available. Use appropriate log levels and capture caller source location when useful. End every started profiling scope exactly once on all paths, including early returns. Disabled instrumentation must not skip required computations or state changes.

## Comments and API documentation

- Use the markers `$TODO`, `$HACK`, `$FIXME`, `$NOTE`, `$DEPRECATED`, `$INCOMPLETE`, and `$CLEANUP`.
- Document all functions and types in module headers with compact comments. For functions, describe behavior, each parameter and its accepted range, return values, and thread safety.
- For structs, enums, and unions, document only the members that need explanation for users.
- In implementations, comment only nontrivial details or reminders maintainers need.

## Assertions

- Use as many nonredundant assertions as possible for internal execution invariants, not parameter or input validation. Handle invalid inputs and expected failures through normal error paths that work with assertions disabled.
- Before memory access, assert required non-null pointers and that indices and accessed ranges fit within the live object. For indexing from an array's start, check signed indices are nonnegative before comparing with the element count, and every index is less than the count. Check range and size calculations without overflow.
- Before forming a pointer arithmetically, use overflow-safe integer offset checks to assert the result stays within the same live array object or its one-past position. Never dereference the one-past pointer; do not subtract or relationally compare unrelated pointers to check bounds. Pointer differences must fit in `ptrdiff_t`.
- Before arithmetic, assert internal preconditions such as nonzero divisors, representable signed results and sizes, valid shift counts and operands, and valid math-function domains (e.g. nonnegative inputs to `sqrt` and positive inputs to `log`). Account for `INT_MIN / -1` or `INT_MIN % -1`; check results are finite where required.
- Cover casts, statements, and code paths. Assert when an unimplemented or unfinished code path is reached.
- Keep assertion expressions free of side effects and undefined behavior. Do not put required computations or state changes in assertions, which may be disabled.
- Prefer compile-time assertions when equivalent to runtime assertions. Use them for required struct or union sizes, alignments, and other attributes.
