# Parallel execution

Use multiple cores when independent work and workload size justify scheduling and synchronization costs. Preserve a correct one-worker path and measure performance on the intended workload.

## Lane groups

For suitable data-parallel operations, workers can execute the same routine with a lane index and count. Each lane handles its own portion of the data; one lane can perform work that must happen once.

To partition `count` items across `lanes` workers, require `lanes > 0` and `0 <= lane < lanes`. Let `q = count / lanes` and `r = count % lanes`. The lane's half-open range starts at `lane * q + min(lane, r)` and contains `q + (lane < r)` items, even when items are fewer than lanes.

- Keep independent writes in disjoint ranges or synchronize appropriately. Join or synchronize before consuming other lanes' results.
- If one lane prepares shared data, synchronize before other lanes read it. Every participating lane must reach each group barrier in the same order; avoid early returns that strand peers.
- Keep temporary state per lane or per thread. Thread-local storage belongs to an operating-system thread, so reset task-specific state when threads are reused.
- Keep group state separate between concurrent invocations. Avoid shared static scratch state that makes a routine unexpectedly non-reentrant.
- Choose lane counts and task granularity for the workload; account for uneven work and synchronization cost. A task system is useful when it addresses a concrete scheduling need.
- If per-item work varies, consider dynamically assigning bounded chunks to workers; for a few disproportionately large tasks, look for safe ways to subdivide them. Ensure every item is handled as required, counter arithmetic cannot wrap, and the assignment and result order meet the algorithm's contract. Measure contention and load balance.
- Coordinate failures and cancellation across the group so every required barrier is reached or the group has a defined way to abort; one lane must not strand the others.

For a reduction, combine per-lane partial results after synchronization or use an appropriate atomic operation. Account for integer overflow and floating-point changes from summing in a different order. For a broadcast, the producing lane writes to group-local shared storage; synchronize, let other lanes read it, and synchronize before reuse. The primitive must provide the memory visibility required by the shared data.

Source of the lane-group approach: Ryan Fleury, [Multi-Core By Default](https://www.dgtlgrove.com/p/multi-core-by-default) (2025).
