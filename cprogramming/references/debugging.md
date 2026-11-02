# Debugging with GDB

For runtime debugging, use GDB when available and compatible with the target. If GDB cannot be used, report the limitation and use an available compatible debugger where appropriate.

## Prepare the session

- Identify the failing executable, input, arguments, working directory, environment, and reproduction conditions. Preserve the original build and failure evidence when a build change could hide the issue.
- Check `gdb --version` works and GDB supports the target architecture and executable and debug-information formats. Windows and macOS toolchains may require a different compatible debugger; report what was available and used.
- Load the executable, matching source, symbols, and shared libraries from the same build. If suitable symbols are missing and rebuilding is appropriate, use the project's debug configuration; with a compatible GNU-style compiler, `-g -O0` is one option. Optimized builds can move code or eliminate variables, but may be needed to reproduce timing- or optimization-sensitive failures.

## Run and inspect

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

## Other entry points

- **Core dump:** Where supported, open an existing dump with `gdb -q ./build/program path/to/core`. Use its matching executable, libraries, and symbols. Inspect the stopped state; `run` starts a new execution and does not reproduce the dump.
- **Running process:** For a process in scope, use `gdb -q ./build/program -p PID` if target and permissions allow. Attaching stops it and can affect timing; `detach` releases it to resume.
- **Batch crash capture:** For a reproducible run stopping on failure, use `gdb -q -batch -ex run -ex "thread apply all bt full" --args ./build/program arg1`. Inspect the reported stop and output: GDB's batch exit status alone does not establish whether the program passed. If the program exits, there may be no live stack to inspect.

## In-process stack traces

When a program needs its own stack trace, capture calling-thread addresses and resolve module and symbol names where possible. On Windows, use `CaptureStackBackTrace` and DbgHelp when supported; on Linux and macOS, use `backtrace` and `dladdr` when available. Check the actual target's APIs and library linkage; report unsupported targets.

- Bound frame storage and validate capacity and frame-skip arithmetic. Return the number of frames captured and retain addresses when symbol names are unavailable.
- Coordinate DbgHelp initialization and cleanup with other users of the symbol handler, and serialize DbgHelp calls across threads.
- Treat symbol names as best-effort; optimized code may omit frames or names. Do not assume capture and symbolization are safe in a fatal-signal handler. Verify supported targets and actual output when implementing them.

## Validate the diagnosis

Connect the observed stop, frames, and values to a concrete cause. After a fix, rerun the original reproduction and relevant checks, including outside GDB when timing or debugger behavior matters. Report evidence, debugger and target limitations, and what remains unverified.

For command details, see the [GNU GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb/).
