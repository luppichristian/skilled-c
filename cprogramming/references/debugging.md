# Debugging with GDB

## Prepare the session

- Identify the failing executable, input, arguments, working directory, environment, and conditions needed to reproduce the problem. Preserve the original build and failure evidence when changing the build could hide the issue.
- Check that `gdb --version` works and that this GDB supports the target architecture and executable and debug-information formats. Windows and macOS toolchains may require a different compatible debugger; report what was actually available and used.
- Load the executable, matching source, symbols, and shared libraries from the same build. If suitable symbols are missing and rebuilding is appropriate, use the project's debug configuration; with a compatible GNU-style compiler, `-g -O0` is one option. Optimized builds can move code or eliminate variables, but may be necessary to reproduce timing- or optimization-sensitive failures.

## Run and inspect

Start GDB with the actual program and arguments, adapting paths for the host:

```sh
gdb -q --args ./build/program arg1
```

At the GDB prompt, replace `suspect_function` with a function in the program and inspect the stop:

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
- Use `print expression` to inspect a value and `watch expression` to stop when its value changes. Watchpoints depend on the target and may be slow or limited; expressions that call functions or assign values can change program state.
- At a crash or other stop, use `bt full` for a stack with locals, then select a relevant frame with `frame N`. For concurrent problems, use `info threads`, `thread N`, and `thread apply all bt` to inspect the other threads. A corrupted stack or optimized code can make frames and values incomplete.

## Other entry points

- **Core dump:** When the target supports it, open an existing dump with `gdb -q ./build/program path/to/core`. Use the executable, libraries, and symbols matching the dump. Inspect the stopped state; `run` starts a new execution and does not reproduce the dump itself.
- **Running process:** For a process in scope, use `gdb -q ./build/program -p PID` if the target and permissions allow it. Attaching stops the process and can affect timing; use `detach` to release it and let it resume.
- **Batch crash capture:** For a reproducible run that stops on the failure, use `gdb -q -batch -ex run -ex "thread apply all bt full" --args ./build/program arg1`. Inspect the reported stop and output: GDB's batch exit status alone does not establish whether the program passed. If the program exits, there may be no live stack to inspect.

## In-process stack traces

When a program needs to capture its own stack trace, capture addresses for the calling thread and resolve module and symbol names where possible. On Windows, use `CaptureStackBackTrace` and DbgHelp when supported; on Linux and macOS, use `backtrace` and `dladdr` when available. Check the actual target's APIs and library linkage, and report unsupported targets.

- Bound frame storage and validate capacity and frame-skip arithmetic. Return the number of frames captured and retain addresses when symbol names are unavailable.
- Coordinate DbgHelp initialization and cleanup with other users of the symbol handler, and serialize DbgHelp calls across threads.
- Treat symbol names as best-effort; optimized code may omit frames or names. Do not assume capture and symbolization are safe in a fatal-signal handler. Verify the supported targets and actual output when implementing them.

## Validate the diagnosis

Connect the observed stop, frames, and values to a concrete cause. After a fix, rerun the original reproduction and relevant checks, including outside GDB when timing or debugger behavior matters. Report the evidence, debugger and target limitations, and anything that remains unverified.

For command details, see the [GNU GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb/).
