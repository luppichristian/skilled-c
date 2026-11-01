# C correctness

## Arithmetic and conversions

- Before computing an allocation size such as `count * sizeof(*items)`, check that `count` does not exceed `SIZE_MAX / sizeof(*items)`. Check subsequent alignment and offset additions before performing them.
- Validate values before converting to a narrower type or between signed and unsigned types. Do not rely on signed integer overflow or an out-of-range shift to wrap predictably.
- Use sizes and counts in the type required by the operation, and check externally supplied values before converting them into a size.

## Pointers and lifetimes

- Initialize objects before reading them. Keep pointer arithmetic and dereferences within the bounds and lifetime of the referenced object.
- Do not retain pointers to stack objects after their scope ends or pointers into an arena after the relevant rewind, reset, or release.
- Avoid unaligned or incompatible typed dereferences when working with raw bytes. Copy bytes with `memcpy` where appropriate, then decode the representation explicitly; use `memmove` when regions may overlap.
- A pointer-sized integer alias is for platform interfaces that require it; it does not make raw pointer values a portable file or network representation.

## Strings and resources

- Track string lengths and buffer capacities explicitly. Reserve room for a terminator when passing a C string, and check formatting or copying results for errors and truncation.
- Check failures from allocation, file, and other external operations. Keep ownership clear and release resources on every path that does not transfer them to the caller.
- Validate external inputs through ordinary error handling. Assertions express internal invariants and must not be the only mechanism protecting an operation from invalid input.
