# C correctness

## Arithmetic and conversions

- Before computing an allocation size such as `count * sizeof(*items)`, check `count` does not exceed `SIZE_MAX / sizeof(*items)`. Check subsequent alignment and offset additions before performing them.
- Validate values before narrowing or converting between signed and unsigned types. Do not rely on signed overflow or out-of-range shifts to wrap predictably.
- Use sizes and counts in the type required by the operation; check externally supplied values before conversion to a size.

## Pointers and lifetimes

- Initialize objects before reading. Keep pointer arithmetic and dereferences within the referenced object's bounds and lifetime.
- Do not retain pointers to stack objects after their scope or into an arena after the relevant rewind, reset, or release.
- Avoid unaligned or incompatible typed dereferences of raw bytes. Copy with `memcpy` where appropriate, then explicitly decode the representation; use `memmove` when regions may overlap.
- A pointer-sized integer alias serves platform interfaces requiring it; raw pointer values are not a portable file or network representation.

## Strings and resources

- Track string lengths and buffer capacities explicitly. Reserve terminator space when passing a C string; check formatting or copying for errors and truncation.
- Check allocation, file, and other external operations for failure. Keep ownership clear and release resources on every path that does not transfer them to the caller.
- Validate external inputs through ordinary error handling. Assertions express internal invariants; they must not be the only protection against invalid input.
