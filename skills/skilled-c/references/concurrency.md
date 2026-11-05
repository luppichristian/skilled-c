# Concurrency

- Always consider thread safety.
- Prefer keeping state `thread_local`.
- Build and use a task system when it makes sense.
- Apply the [parallel execution patterns](parallelism.md) when the workload can benefit from multiple cores.

For each public interface accessing mutable state, document whether callers may use it concurrently and who synchronizes it. Keep scratch storage and other naturally per-thread state thread-local; do not silently duplicate state intended to be shared across threads.

Protect shared mutable state with a lock, atomics, or a clear ownership protocol. `volatile` alone does not provide inter-thread synchronization. Specify worker shutdown and work-item ownership; ensure all workers finish before releasing data they can access.

Map work ordering and communication before choosing a threading model. Distinguish accelerating independent parts of one operation from allowing separate tasks, such as input and I/O, to progress independently. Introduce queues or additional threads only when their scheduling and lifetime costs suit the problem.

Classify operations by actual reads and possible writes, including lazy initialization, cache misses, and allocations. Concurrent reads of immutable data are useful only after safe publication and while its lifetime is protected. Where it helps callers reason about concurrency, separate a read-only lookup from an operation that may insert or otherwise mutate.

When the workload permits, give workers disjoint output ranges or independent data structures; combine results after synchronization. Define merge ordering, duplicate handling, allocation failure, and ownership; storage contributing to a merged result must outlive all readers. Synchronize when mutation cannot be partitioned safely.
