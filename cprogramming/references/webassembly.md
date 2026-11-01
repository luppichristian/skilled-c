# WebAssembly

Use Emscripten's `emcc` when WebAssembly is requested. Identify the intended runtime and output format, preserve a native build where required, and validate the WebAssembly artifact in a suitable runtime before claiming it works.

## SIMD

- Emscripten enables WebAssembly SIMD with `-msimd128`; `__wasm_simd128__` indicates that the code is being compiled with that feature enabled. The macro describes the build, not the capabilities of every runtime that may load the result.
- If a target runtime may lack SIMD, provide a baseline build as well as the SIMD build and select a compatible artifact before loading it. Do not assume a scalar branch inside a SIMD-requiring module will run on an engine that rejects that module's features.

## Threads

- Enable Emscripten pthread support at both compile and link time with `-pthread` when the application needs it. Keep a non-threaded path where required by the target environment.
- Browser pthread builds depend on shared-memory support and the appropriate cross-origin isolation headers. Check deployment requirements and report when they cannot be verified locally.
