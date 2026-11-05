# Skilled C

[![GitHub stars](https://img.shields.io/github/stars/luppichristian/skilled-c?style=flat)](https://github.com/luppichristian/skilled-c)
[![GitHub issues](https://img.shields.io/github/issues/luppichristian/skilled-c?style=flat)](https://github.com/luppichristian/skilled-c/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/luppichristian/skilled-c?style=flat)](https://github.com/luppichristian/skilled-c)
[![License: MIT](https://img.shields.io/github/license/luppichristian/skilled-c?style=flat)](LICENSE)

Skilled C is a local plugin for C projects in Codex or Claude Code. It provides coding conventions, project guidance, and MCP tools for GDB and optional RenderDoc capture analysis.

The [skill](skills/skilled-c/SKILL.md) guides project setup, builds, code conventions, testing, debugging, and performance. It respects existing project conventions and user instructions and can use local tools when a server is unavailable.

| Server | What it does |
| --- | --- |
| [gdb-mcp](https://github.com/Ipiano/gdb-mcp) | Manages GDB sessions, breakpoints, backtraces, and inspection. |
| [renderdoc-mcp](https://github.com/scarletfantasy/renderdoc-mcp) | Inspects existing RenderDoc `.rdc` captures. Optional, disabled by default, and supported on Windows by the upstream server. |

## Requirements

- Codex CLI or desktop with local plugin support, or Claude Code, and Git.
- [uv](https://docs.astral.sh/uv/) (`uvx` on `PATH`) and Python 3.10 or newer for the Python servers. `uv` can install a compatible Python. The first launch downloads server dependencies unless cached.
- External tools for the capabilities you use: `clangd`, `clang-format`, and `clang-tidy` for local Clang tooling; a compatible GDB for debugger sessions; and RenderDoc for capture replay. The plugin does not install these programs.

## Install

Clone this repository with its submodules:

```sh
git clone --recurse-submodules https://github.com/luppichristian/skilled-c.git skilled-c
cd skilled-c
```

For an existing checkout, initialize the pinned servers:

```sh
git submodule update --init --recursive
```

### Codex

From the repository root, register the local marketplace and install the plugin:

```sh
codex plugin marketplace add .
codex plugin add skilled-c@skilled-c
```

Alternatively, open this repository in a supported Codex desktop client, restart the app, select the Skilled C repository marketplace in Plugins Directory, and install Skilled C there. See the [OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins) for local marketplaces.

Start a new Codex chat after installation. The local plugin needs no separate MCP configuration in `config.toml`.

Codex installs a cached plugin copy. Initialize submodules before installation; GitHub source ZIPs and clones without `--recurse-submodules` omit their contents. After changing the checkout or updating submodules, run `codex plugin add skilled-c@skilled-c` again to refresh the installed copy, then start a new chat.

### Claude Code

From the repository root, register the local marketplace and install the plugin:

```sh
claude plugin marketplace add .
claude plugin install skilled-c@skilled-c
```

Start a new Claude Code session and use `/mcp` to check the GDB server. The local marketplace reads the plugin from this checkout, so keep the checkout and its submodules in place. After changing the plugin, use `/reload-plugins` in a session or start a new one. See the [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins) for details.

If the first server launch times out while `uv` downloads dependencies, set `MCP_TIMEOUT=120000` before starting Claude Code and retry.

## Use Skilled C

Open a C project in Codex or Claude Code and request the work. For example:

> Use the Skilled C skill to review this project's coding conventions and build setup.

The skill applies relevant references and can use available configured MCP tools. See the [skill and reference list](skills/skilled-c/SKILL.md) for the topics it covers and the [MCP integration guide](skills/skilled-c/references/mcp.md) for server-specific guidance and fallbacks.

In Claude Code, you can also explicitly invoke the skill with `/skilled-c:skilled-c`.

## Configure the servers

GDB lookup defaults to `PATH`. Set `GDB_PATH` for a different executable or pass the debugger path to `gdb_start_session`. Set environment variables in the client startup environment; open a new session after changing them.

### Enable RenderDoc on Windows

In Codex, add this to your user configuration (`~/.codex/config.toml`), then start a new chat:

```toml
[plugins."skilled-c@skilled-c".mcp_servers.renderdoc-mcp]
enabled = true
```

In Claude Code, register the optional server separately. From the repository root in PowerShell, run:

```powershell
$renderdocSource = (Resolve-Path .\mcp\renderdoc-mcp).Path
claude mcp add --scope user --transport stdio renderdoc-mcp -- uvx --from $renderdocSource renderdoc-mcp
```

Registration uses the checkout's absolute path; update it if you move the checkout. Start a new session and check `/mcp` for the server. Claude Code starts plugin-provided servers automatically, so register RenderDoc separately to keep it optional.

On startup, the upstream server's default `qrenderdoc` backend installs its bundled extension into `%APPDATA%\qrenderdoc\extensions\renderdoc_mcp_bridge` and, by default, adds it to `AlwaysLoad_Extensions` in `UI.config`. Set `RENDERDOC_INSTALL_ALWAYS_LOAD=0` before starting your client to avoid that configuration change; RenderDoc still needs the extension. Set `RENDERDOC_QRENDERDOC_PATH` if `qrenderdoc.exe` is not in the upstream default location. See the [upstream RenderDoc documentation](https://github.com/scarletfantasy/renderdoc-mcp) for version support, backend options, and capture limitations.

## Updating the bundled servers

Server revisions are pinned as Git submodules. To update a server, check out the desired upstream revision in its `mcp/` directory and record the new submodule commit. Server dependencies are resolved by `uvx`; `gdb-mcp` is constrained to MCP versions below 2 for compatibility with its current upstream API.

## License

The plugin is [MIT licensed](LICENSE). The upstream servers have their own licenses in their submodules.
