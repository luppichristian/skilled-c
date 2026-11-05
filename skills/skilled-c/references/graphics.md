# Graphics and GPU work

## Library selection

Respect an existing project stack and explicit user choices. For a new project, prefer the following according to its targets and performance needs:

- **SDL3 + SDL_GPU:** cross-platform applications needing high performance.
- **raylib:** cross-platform applications without extreme performance requirements.
- **Win32 + Direct3D 12:** high-performance Windows-specific applications.
- **Metal:** high-performance Apple-specific applications. In a C project, isolate any required Objective-C or C++ bridge behind a C interface. If using Metal-cpp, compile the bridge as C++17 or later and link the required Apple frameworks.
- **SDL + Vulkan:** applications with extreme performance requirements needing direct control and recent Vulkan features, accepting more limited portability. Use SDL for windowing and Vulkan directly for rendering.

When cases overlap, prioritize SDL + Vulkan for extreme performance if it exposes the required features on the targets and its portability tradeoff is acceptable. Otherwise, prefer a platform-specific high-performance route, then SDL GPU for cross-platform performance; use raylib for simpler cross-platform workloads. Match the choice to the project's required features and constraints.

These are selection preferences, not performance guarantees. Profile representative workloads and check target hardware, drivers, API versions, and required features. SDL GPU's Metal, Direct3D 12, and Vulkan backends do not themselves provide a browser renderer; for WebAssembly, verify the selected SDL version and use a supported browser rendering path. Android Vulkan support depends on device capabilities. Vulkan on Apple platforms needs a compatible implementation such as MoltenVK; check feature support rather than assuming every extension is available.

## Resource lifetime and synchronization

Recording or submitting GPU work does not generally mean it has finished. Keep resources, descriptors, upload storage, and their referenced contents valid for the period required by the chosen API. Before the CPU overwrites storage still in use, wait for the relevant completion signal or use another safe resource or region. GPU-side reuse can instead be ordered and synchronized according to the API. Track completion before recycling frame or staging storage and before destruction when the API requires it.

Follow the API's rules for access transitions, barriers, queue ownership, and visibility; a completion fence and a device memory barrier serve different purposes. Honor host mapping and flush/invalidate requirements. A resource-renaming or cycling feature may provide fresh backing storage; initialize every part the subsequent work needs instead of assuming old contents survived. Exact cycling rules depend on the API.

## Shader interfaces and images

Match host data to the shader's actual buffer layout, bindings, element types, and matrix conventions. Verify sizes and offsets against the target shader language and compiler rules, using reflection or explicit checks where available; a similar-looking C struct is not proof of a matching layout. Build or translate shaders for the formats the selected backend accepts, and diagnose compilation and binding failures. For SDL GPU, SDL_shadercross is an optional tool for translating HLSL or SPIR-V into backend shader formats.

Measure shader changes on representative hardware and workloads, and inspect compiled output when useful. A source-level conditional does not necessarily become a hardware branch, and rewriting it as arithmetic is not automatically faster or semantically equivalent.

State whether color data is linear or encoded and whether alpha is straight or premultiplied. Match texture interpretation, shader output, blend factors, and render-target behavior; blend color in the intended space and preserve alpha when the result needs it. Set filtering, addressing, and mip behavior intentionally, including atlas padding where filtered samples could reach neighboring images. Do not apply legacy API pixel-center offsets without checking the target API.

Test updates across multiple frames, partial writes, resizing, transparency, and supported backends. Use API validation and a compatible graphics debugger to inspect incorrect results. For supported targets, use the RenderDoc workflow in [Debugging](debugging.md#graphics-debugging-with-renderdoc); for Metal, use Xcode GPU frame capture where available.
