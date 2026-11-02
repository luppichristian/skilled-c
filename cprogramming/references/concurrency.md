# Concurrency

- Always consider thread safety.
- Prefer keeping state `thread_local`.
- Build and use a task system when it makes sense.
- Apply the [parallel execution patterns](parallelism.md) when the workload can benefit from multiple cores.

For each public interface accessing mutable state, document whether callers may use it concurrently and who synchronizes it. Keep scratch storage and other naturally per-thread state thread-local; do not silently duplicate state intended to be shared across threads.

Protect genuinely shared mutable state with a lock, atomics, or a clear ownership protocol. `volatile` alone does not provide inter-thread synchronization. Make worker shutdown and work-item ownership explicit; ensure all workers have finished before releasing data they can access.
