# Arena allocation

Base dynamic allocation around arenas that group allocations with a common lifetime. Choose the lifetime first, such as one request, frame, loaded document, or application state, and allocate related data from the corresponding arena. Reuse an existing arena implementation when appropriate. Build pools, free lists, or other specialized allocators on top of arenas when individual reuse or different allocation behavior is needed.

## Allocation and lifetime

- Document who owns an arena, when it may be reset or released, and whether allocations are zero-initialized. Every pointer into a reset or released region becomes invalid.
- Provide the alignment required by the allocated type. Check multiplication, alignment, and position arithmetic for overflow before advancing the allocation cursor; handle insufficient capacity according to the project's error policy.
- Use a saved position and rewind for nested temporary work. Finish using all objects in the rewound region before restoring the position, and release any non-memory resources those objects own.
- For a result that must outlive temporary work, allocate it in a caller-provided or otherwise longer-lived arena. Do not return pointers into scratch storage that will be reset before the caller uses them.
- Use independent scratch arenas for overlapping lifetimes. When acquiring scratch storage, exclude any arena holding results that must survive the scratch rewind, including a caller-supplied output arena. Give each concurrently executing thread its own scratch arena, or hold exclusive access to a shared scratch arena for the entire mark-to-rewind interval; locking individual allocations alone does not protect their lifetimes.

## Common patterns

- Pass an output arena to a function that returns allocated data; the caller then controls the result's lifetime. Use a separate scratch arena for intermediate data and rewind it before returning.
- For frame-local data, reset a frame arena only after all consumers are done. If the next frame needs the preceding frame's data, use separate arenas and rotate them only when their previous contents are no longer needed.
- When individual fixed-size objects need reuse before the parent arena is reset, allocate backing storage from the arena and return released objects to a free list or pool. The parent arena still controls the storage's overall lifetime.

Choose a fixed buffer, growable blocks, or platform-backed reservation to suit the project. Growth must preserve the addresses of live allocations; adding separate blocks or committing a reserved address range can provide that guarantee. Do not assume a particular virtual-memory API exists on every target.