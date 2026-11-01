# Parallel execution

Use multiple cores where independent work and workload size justify the scheduling and synchronization cost. Preserve a correct one-worker path and measure performance on the intended workload.

## Lane groups

For suitable data-parallel operations, a group of workers can execute the same routine with a lane index and lane count. Each lane handles its own portion of the data; a single lane can perform work that must happen once.

To partition `count` items across `lanes` workers, require `lanes > 0` and `0 <= lane < lanes`. Let `q = count / lanes` and `r = count % lanes`. The lane's half-open range starts at `lane * q + min(lane, r)` and contains `q + (lane < r)` items. This also works when there are fewer items than lanes.

- Keep independent writes in disjoint ranges or use appropriate synchronization. Join or synchronize before consuming results from other lanes.
- If one lane prepares shared data, synchronize before other lanes read it. Every participating lane must reach each group barrier in the same order; avoid early returns that strand peers.
- Keep temporary state per lane or per thread. Thread-local storage belongs to an operating-system thread, so reset task-specific state when threads are reused.
- Keep group state separate between concurrent invocations. Avoid shared static scratch state that makes a routine unexpectedly non-reentrant.
- Choose lane counts and task granularity based on the workload; account for uneven work and the cost of synchronization. A task system is useful when it addresses a concrete scheduling need.

For a reduction, either combine per-lane partial results after synchronization or use an appropriate atomic operation. Account for integer overflow and, for floating point, changes caused by summing in a different order. For a broadcast, let the producing lane write to group-local shared storage, synchronize, let the other lanes read it, then synchronize before reusing that storage. The synchronization primitive must also provide the memory visibility required by the shared data.

Source of the lane-group approach: Ryan Fleury, *Multi-Core By Default* (2025).
