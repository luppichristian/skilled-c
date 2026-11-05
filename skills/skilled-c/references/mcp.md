# MCP integration

The Skilled C plugin bundles server sources and configures MCP servers for C development. Use command-line tools and the RenderDoc interface when a server or its external prerequisites are unavailable.

## Availability and setup

Check available MCP tools in the current session; use those relevant to the task. A configured server may still need its runtime, a first-run dependency download, or an external tool. The servers require `uvx`, and GDB sessions require a compatible GDB. The Windows-only RenderDoc server is disabled by default and can be enabled for graphics work as described in the repository README.

Do not assume an executable or configured server is available in the current session. If a server or capability is unavailable, use a suitable local tool directly; for needed configuration changes, follow the user's preferences and plugin installation instructions.

## GDB debugging with gdb-mcp

Use [gdb-mcp](https://github.com/Ipiano/gdb-mcp) when available to manage a GDB session, set breakpoints, step through execution, and inspect frames, threads, and variables. It requires a compatible GDB installation; configure `GDB_PATH` or the session's debugger path when needed. Follow the preparation and target-compatibility checks in [Debugging](debugging.md#gdb). If the server is unavailable or unsuitable, use a compatible debugger directly.

## Capture analysis with renderdoc-mcp

On Windows, use [renderdoc-mcp](https://github.com/scarletfantasy/renderdoc-mcp) when available to inspect an existing `.rdc` capture, including events, resources, pipeline state, and supported pixel or shader debugging. Its default backend uses `qrenderdoc` and installs a RenderDoc extension; check server version requirements and replay capabilities. Capture the frame using the RenderDoc workflow in [Debugging](debugging.md#graphics-debugging-with-renderdoc). If the server or a replay feature is unavailable, inspect the capture in RenderDoc or use another compatible graphics debugger.
