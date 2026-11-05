# Performance

- Profile and measure nontrivial optimizations. Use SIMD where it benefits the workload, and verify correctness and performance on representative targets.
- Use inline assembly or intrinsics for suitable performance-critical functions, with a supported fallback.
- Track cache misses when investigating relevant bottlenecks.
- Reorder struct members and set alignment and padding appropriately.

For logging and profiling scope contracts, see [Code conventions](code.md#diagnostics).

Compare optimized and baseline implementations using the same build configuration and representative inputs. Record workload, target, and measurements; investigate cache behavior when relevant. Account for API or ABI contracts before changing externally visible struct layouts.

Choose measurements that reflect the actual goal: for example, end-to-end latency and responsiveness, throughput, memory use, or frame-time distribution rather than just an average. Include repeated developer workflows such as build, test, and startup time when they are the bottleneck. Record enough conditions to compare like with like, including relevant input sizes and cold or warm state.

For inline assembly, constrain inputs and outputs correctly, declare relevant clobbers, preserve the platform calling convention, and document supported compiler and architecture. Keep and verify a suitable non-assembly implementation for other targets.

For SIMD, also read [Portability](portability.md) for capability detection and fallbacks.
