# Debugging

## GDB

For runtime debugging, use GDB when available and compatible with the target; otherwise use an available compatible debugger.

When available, `gdb-mcp` can control a GDB session and return structured debugger results. See [MCP integration](mcp.md#gdb-debugging-with-gdb-mcp) for prerequisites and fallback.

### Prepare the session

- Identify the failing executable, input, arguments, working directory, environment, and reproduction conditions. Preserve the original build and failure evidence when a build change could hide the issue.
- Check `gdb --version` works and GDB supports the target architecture and executable and debug-information formats. Windows and macOS toolchains may require a different compatible debugger.
- Load the executable, matching source, symbols, and shared libraries from the same build. If suitable symbols are missing and rebuilding is appropriate, use the project's debug configuration; with a compatible GNU-style compiler, `-g -O0` is one option. Optimized builds can move code or eliminate variables, but may be needed to reproduce timing- or optimization-sensitive failures.

### Run and inspect

Start GDB with the actual program and arguments; adapt paths for the host:

```sh
gdb -q --args ./build/program arg1
```

At the GDB prompt, replace `suspect_function` with a program function and inspect the stop:

```text
(gdb) set pagination off
(gdb) break suspect_function
(gdb) run
(gdb) bt
(gdb) frame 0
(gdb) info args
(gdb) info locals
(gdb) list
```

- Use `break file.c:42` for a source location and `break file.c:42 if condition` for a conditional breakpoint. Use `continue` to resume, `next` to step over a call, `step` to step into it, and `finish` to return from the current frame.
- Use `print expression` to inspect a value and `watch expression` to stop when it changes. Watchpoints depend on the target and may be slow or limited; expressions calling functions or assigning values can change program state.
- At a crash or other stop, use `bt full` for a stack with locals, then select a relevant frame with `frame N`. For concurrent problems, inspect other threads with `info threads`, `thread N`, and `thread apply all bt`. A corrupted stack or optimized code can make frames and values incomplete.

### Other entry points

- **Core dump:** Where supported, open an existing dump with `gdb -q ./build/program path/to/core`. Use its matching executable, libraries, and symbols. Inspect the stopped state; `run` starts a new execution and does not reproduce the dump.
- **Running process:** For a process in scope, use `gdb -q ./build/program -p PID` if target and permissions allow. Attaching stops it and can affect timing; `detach` releases it to resume.
- **Batch crash capture:** For a reproducible run stopping on failure, use `gdb -q -batch -ex run -ex "thread apply all bt full" --args ./build/program arg1`. Inspect the reported stop and output: GDB's batch exit status alone does not establish whether the program passed. If the program exits, there may be no live stack to inspect.

## In-process stack traces

When a program needs its own stack trace, capture calling-thread addresses and resolve module and symbol names where possible. On Windows, use `CaptureStackBackTrace` and DbgHelp when supported; on Linux and macOS, use `backtrace` and `dladdr` when available. API availability and library linkage depend on the target.

- Bound frame storage and validate capacity and frame-skip arithmetic. Return the number of frames captured and retain addresses when symbol names are unavailable.
- Coordinate DbgHelp initialization and cleanup with other users of the symbol handler, and serialize DbgHelp calls across threads.
- Treat symbol names as best-effort; optimized code may omit frames or names. Do not assume capture and symbolization are safe in a fatal-signal handler. Verify supported targets and actual output when implementing them.

## Debugger effects

The debugger can affect timing and program behavior, so a reproduction outside GDB may behave differently.

For command details, see the [GNU GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb/).

## Graphics debugging with RenderDoc

Use RenderDoc when an applicable graphics issue needs frame capture and inspection. It complements a CPU debugger such as GDB. Check the installed version and the target API, platform, and features against [RenderDoc's API support](https://github.com/baldurk/renderdoc#api-support): Vulkan, OpenGL, OpenGL ES, D3D11, and D3D12 support depends on the platform and API version; Metal, D3D9, and D3D10 are not supported.

On Windows, an available `renderdoc-mcp` can inspect an existing capture; see [MCP integration](mcp.md#capture-analysis-with-renderdoc-mcp). Capture and inspection still depend on RenderDoc's support for the target.

1. Reproduce the problem with the actual build, inputs, arguments, working directory, and environment. In RenderDoc, use **File > Launch Application**, configure the executable and its settings, and launch it. If CPU call stacks are needed, enable **Collect Callstacks** before capture. With the RenderDoc overlay active, capture the next presented frame using the configured capture key (normally `F12` or `Print Screen`). Open and save the resulting `.rdc` capture, and confirm that it contains the faulty frame. See the [quick start](https://github.com/baldurk/renderdoc/blob/v1.x/docs/getting_started/quick_start.rst).
2. In the Event Browser, step through the frame to locate the draw or dispatch where the output first becomes incorrect; compare against a known-good capture when useful. Inspect render targets and textures, then the pipeline state, bound buffers and resources, shaders, viewport/scissor, culling, depth, and blend settings. For geometry issues, use the Mesh Viewer to compare vertex/index inputs and vertex shader output with the expected data; check counts, offsets, formats, and strides.
3. Where supported, use Pixel History to identify the events affecting a pixel and debug the relevant vertex, pixel, or compute shader invocation. Source-level shader debugging requires suitable shader debug information, separately from C debug symbols. Shader debugging is supported for D3D11, D3D12, and Vulkan, but not all shaders or features are supported; consult the [shader debugging guide](https://github.com/baldurk/renderdoc/blob/v1.x/docs/how/how_debug_shader.rst).
4. Correlate the suspect event with the C code. If call stacks were captured, use **Tools > Resolve Symbols** with matching symbols and inspect the API Inspector; see the [call stack guide](https://github.com/baldurk/renderdoc/blob/v1.x/docs/how/how_capture_callstack.rst). Use graphics API validation and a CPU debugger as needed, and verify the issue and any fix outside capture: instrumentation and replay can affect behavior.

Prefer launching through RenderDoc. Injection into an already running process is only appropriate before that process has initialized or used the graphics API; see [capture and injection](https://github.com/baldurk/renderdoc/blob/v1.x/docs/window/capture_attach.rst). For precisely timed or non-presenting work, the optional [in-application API](https://github.com/baldurk/renderdoc/blob/v1.x/docs/in_application_api.rst) can bracket work with `StartFrameCapture` and `EndFrameCapture` for the appropriate device/window, checking whether capture succeeded; a normal capture hotkey or `TriggerCapture` needs a presented frame. If RenderDoc or the required capture/replay support is unavailable, report that limitation and use an available compatible graphics debugger or API validation tools.
