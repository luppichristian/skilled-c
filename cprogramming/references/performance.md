# Performance

- Profile and measure nontrivial optimizations. Apply an obvious SIMD improvement promptly when its benefit is clear, and verify correctness and performance on representative targets.
- Use inline assembly or intrinsics for suitable performance-critical functions, with a supported fallback.
- Track cache misses when investigating relevant bottlenecks.
- Reorder struct members and set alignment and padding appropriately.
- Use intrinsics where possible and SIMD where it makes sense.

Compare optimized and baseline implementations using the same build configuration and representative inputs. Record the workload, target, and measurements; investigate cache behavior when it is relevant. Do not change externally visible struct layouts without accounting for the API or ABI contract.

For inline assembly, constrain inputs and outputs correctly, declare relevant clobbers, preserve the platform calling convention, and document the supported compiler and architecture. Keep and verify a suitable non-assembly implementation for other targets.

For SIMD, also read [Portability](portability.md) for capability detection and fallbacks.
