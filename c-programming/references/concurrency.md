# Concurrency

- Always consider thread safety when writing code.
- Prefer keeping state `thread_local`.
- Build and use a task system when it makes sense.
- Apply the [parallel execution patterns](parallelism.md) when the workload can benefit from multiple cores.

For each public interface that accesses mutable state, document whether callers may use it concurrently and who performs synchronization. Keep scratch storage and other naturally per-thread state thread-local; do not silently duplicate state that is intended to be shared across threads.

Protect genuinely shared mutable state with a lock, atomics, or a clearly defined ownership protocol. `volatile` does not by itself provide inter-thread synchronization. Make worker shutdown and ownership of work items explicit, and ensure all workers have finished before releasing data they can access.
