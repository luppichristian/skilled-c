# WebAssembly

Use Emscripten's `emcc` for WebAssembly. Select the appropriate runtime and output format; preserve a native build where required. A successful build alone does not establish behavior in the intended runtime.

## SIMD

- Emscripten enables WebAssembly SIMD with `-msimd128`; `__wasm_simd128__` indicates the feature is enabled for compilation. The macro describes the build, not the capabilities of every runtime that may load the result.
- If a target runtime may lack SIMD, provide baseline and SIMD builds and select a compatible artifact before loading. A scalar branch inside a SIMD-requiring module will not help an engine that rejects its features.

## Threads

- Enable Emscripten pthread support at compile and link time with `-pthread` when needed. Keep a non-threaded path where required by the target environment.
- Browser pthread builds depend on shared-memory support and appropriate cross-origin isolation headers in the deployment environment.
