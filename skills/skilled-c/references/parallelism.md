# Parallel execution

Use parallel execution when independent work and workload size justify scheduling and synchronization costs. Preserve a correct one-worker CPU path; measure performance on the intended workload.

## GPU compute

Consider a compute shader for sufficiently large, parallel workloads, especially when inputs or subsequent consumers already reside on the GPU. Small or irregular jobs, and results needed immediately by the CPU, may favor a sequential, SIMD, or multithreaded CPU implementation. Keep a CPU path for unsupported targets and workloads where offloading loses; preserve required result semantics, including determinism requirements and numerical tolerances, across paths.

Use the compute interface available in the project's graphics or compute stack, such as SDL_GPU compute passes, Vulkan compute, Direct3D 12, or Metal. Other APIs may offer compute where their version, device, and backend support it; a graphics wrapper such as raylib does not guarantee a compute interface on every target. Check required shader formats, buffer and texture features, and device limits. If using a separate compute API, account for resource sharing, synchronization, and any copies between APIs rather than assuming interoperability.

Compare CPU and GPU paths on representative targets and input sizes. Include CPU command recording and submission, shader or pipeline setup, uploads, dispatch and GPU execution, GPU contention with rendering, readback, and waits in end-to-end latency and frame-time or throughput measurements. Measure cold and steady-state behavior where relevant; GPU execution time alone is not the cost of offloading. Batch suitable work, reuse pipelines and buffers, and keep intermediate data on the GPU when profitable. Choose any CPU/GPU crossover from measurements, not a universal item-count threshold.

Partition work into invocations and workgroups within the API's limits, guard out-of-range accesses for partial groups, and use appropriate atomics or disjoint writes. A workgroup barrier does not synchronize all workgroups: use separate dispatches and the API's required dependencies for global phases. Ensure every participating invocation reaches required workgroup barriers, including in partial groups. Match host and shader data layouts and account for overflow and changes to floating-point reduction order.

### CPU and GPU coordination

- For CPU-to-GPU data, finish host writes before GPU consumption, flush mapped memory when required, and use the API's upload, access-transition, and ordering rules. Keep staging data and other resources valid until the GPU is finished with them.
- For GPU-to-GPU dependencies, order dependent compute, copy, and render operations with the API's required barriers, resource transitions, and queue synchronization. For SDL_GPU, end the compute pass and begin another before a dispatch consumes a previous dispatch's output or requires ordered overlapping writes.
- For GPU-to-CPU results, copy to host-readable storage when needed and consume it only after the relevant CPU-visible fence, event, or completion callback signals. Map and invalidate memory as required by the API. For example, SDL_GPU can copy into a download transfer buffer in a copy pass, submit with a fence, and map and read after it signals; release the fence when finished. A completion signal does not replace GPU memory dependencies or host visibility operations.
- Avoid an immediate CPU wait when the algorithm permits: poll or use a completion callback, do independent CPU work, and consume a completed result later. Double- or triple-buffer staging and results, tracking completion per slot before reuse; accepting an older result must satisfy the application's latency and correctness requirements. If a current result is required, account for the wait or use the CPU path.

For resource lifetime, mapping, shader interfaces, and graphics debugging, also read [Graphics and GPU work](graphics.md).

## Lane groups

For suitable data-parallel operations, workers can execute the same routine with a lane index and count. Each lane handles its data portion; one lane can perform work that must happen once.

- Keep independent writes in disjoint ranges or synchronize appropriately. Join or synchronize before consuming other lanes' results.
- If one lane prepares shared data, synchronize before other lanes read it. Every participating lane must reach each group barrier in the same order; avoid early returns that strand peers.
- Keep temporary state per lane or per thread. Thread-local storage belongs to an operating-system thread, so reset task-specific state when threads are reused.
- Keep group state separate between concurrent invocations. Avoid shared static scratch state that makes a routine unexpectedly non-reentrant.
- Choose lane counts and task granularity for the workload; account for uneven work and synchronization cost. A task system is useful when it addresses a concrete scheduling need.
- If per-item work varies, consider dynamically assigning bounded chunks to workers; for a few disproportionately large tasks, look for safe ways to subdivide them. Ensure every item is handled as required, counter arithmetic cannot wrap, and the assignment and result order meet the algorithm's contract. Measure contention and load balance.
- Coordinate failures and cancellation across the group so every required barrier is reached or the group has a defined way to abort; one lane must not strand the others.

For a reduction, combine per-lane partial results after synchronization or use an appropriate atomic operation. Account for integer overflow and floating-point changes from summing in a different order. For a broadcast, the producing lane writes to group-local shared storage; synchronize, let other lanes read it, and synchronize before reuse. The primitive must provide the memory visibility the shared data requires.
