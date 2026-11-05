# Arena allocation

Base dynamic allocation on arenas that group allocations by lifetime. Choose a lifetime first, such as a request, frame, loaded document, or application state; allocate related data from its arena. Reuse an existing implementation when appropriate. Build pools, free lists, or other specialized allocators atop arenas for individual reuse or different allocation behavior.

Collections, elements, and associated strings or diagnostics can share an arena when they have the same release boundary. An arena alone does not manage external resources or keep an object valid after its removal or the arena's rewind.

## Allocation and lifetime

- Document arena ownership, when it may be reset or released, and whether allocations are zero-initialized. Every pointer into a reset or released region becomes invalid.
- Provide the allocated type's required alignment. Check multiplication, alignment, and position arithmetic for overflow before advancing the cursor; handle insufficient capacity per project error policy.
- Save a position and rewind for nested temporary work. Before restoring it, finish using objects in the rewound region and release their non-memory resources. A checkpoint must restore all allocation state changed since it was taken, including earlier blocks used afterward and blocks added later; all later allocations become invalid. Respect ownership when retaining or releasing backing blocks. Release nested checkpoints in last-in, first-out order unless the arena explicitly supports another order.
- Allocate results that must outlive temporary work in a caller-provided or otherwise longer-lived arena. Do not return pointers into scratch storage that will be reset before use.
- Use independent scratch arenas for overlapping lifetimes. Exclude arenas holding results that must survive the rewind, including a caller-supplied output arena. Give each concurrent thread its own scratch arena, or hold exclusive access to a shared one for the entire mark-to-rewind interval; locking individual allocations alone does not protect their lifetimes.

## Common patterns

- Pass an output arena to functions returning allocated data so the caller controls its lifetime. Use a separate scratch arena for intermediate data; rewind it before returning.
- Reset a frame arena only after all consumers finish. If the next frame needs the preceding frame's data, use separate arenas; rotate only when their previous contents are no longer needed.
- When fixed-size objects need individual reuse before the parent arena resets, allocate backing storage from it and return released objects to a free list or pool. The parent arena still controls storage lifetime.

Choose a fixed buffer, growable blocks, or platform-backed reservation to suit the project. Growth must preserve live allocation addresses; separate blocks or committing a reserved address range can guarantee this. Do not assume a particular virtual-memory API exists on every target.

## Allocator interfaces

When interchangeable allocation strategies are useful, accept an allocator interface with callbacks and user-data context. Expose supported allocation, reallocation, and release operations; an arena need not support individual release. Make optional operations identifiable so callers can check support before invoking them. Document alignment, zero-size behavior, allocation and reallocation failure, ownership, matching release, callback-context lifetime, and thread safety. For reallocation, specify preserved contents, when old pointers become invalid, and any old size or alignment the caller must provide. Preserve the original allocation on reallocation failure when the interface requires it.
