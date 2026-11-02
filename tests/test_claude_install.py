"""Exercise the Claude plugin from a cached copy outside the project."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_plugin_mcp import Client


ROOT = Path(__file__).resolve().parents[1]


class ClaudeInstallTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("claude"), "Claude Code CLI is required")
    def test_marketplace_install_exposes_skill_and_gdb(self):
        with tempfile.TemporaryDirectory(prefix="skilled-c-claude-cli-", ignore_cleanup_errors=True) as temp:
            base = Path(temp)
            workspace = base / "project"
            workspace.mkdir()
            env = os.environ.copy()
            env["CLAUDE_CONFIG_DIR"] = str(base / "claude-state")
            env["DISABLE_AUTOUPDATER"] = "1"
            env["APPDATA"] = str(base / "appdata")
            env["RENDERDOC_INSTALL_ALWAYS_LOAD"] = "0"

            def claude(*args):
                return subprocess.run([shutil.which("claude"), *args], cwd=workspace, env=env,
                                      capture_output=True, text=True, encoding="utf-8",
                                      timeout=120, check=True).stdout

            claude("plugin", "marketplace", "add", str(ROOT))
            claude("plugin", "install", "skilled-c@skilled-c-local")
            details = claude("plugin", "details", "skilled-c")
            self.assertIn("Skills (1)  skilled-c", details)
            self.assertIn("gdb-mcp", details)
            servers = claude("mcp", "list")
            self.assertIn("plugin:skilled-c:gdb-mcp", servers)
            self.assertIn("Connected", servers)
            self.assertNotIn("renderdoc-mcp", servers)

            if os.name == "nt":
                claude("mcp", "add", "--scope", "user", "--transport", "stdio", "renderdoc-mcp",
                       "--", "uvx", "--from", str(ROOT / "mcp" / "renderdoc-mcp"), "renderdoc-mcp")
                servers = claude("mcp", "list")
                renderdoc = next((line for line in servers.splitlines()
                                  if line.startswith("renderdoc-mcp:")), "")
                self.assertIn("Connected", renderdoc)

    def test_cached_plugin_exposes_skill_and_gdb_from_another_workspace(self):
        manifest_path = ROOT / ".claude-plugin" / "plugin.json"
        self.assertTrue(manifest_path.is_file(), "Claude plugin manifest is missing")

        with tempfile.TemporaryDirectory(prefix="skilled-c-claude-") as temp:
            base = Path(temp)
            cached = base / "cached plugin with spaces"
            cached.mkdir()
            shutil.copytree(ROOT / "skills", cached / "skills")
            shutil.copytree(ROOT / "mcp" / "gdb-mcp", cached / "mcp" / "gdb-mcp",
                            ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertTrue((cached / "skills" / "skilled-c" / "SKILL.md").is_file())

            config = manifest["mcpServers"]["gdb-mcp"].copy()
            config["args"] = [arg.replace("${CLAUDE_PLUGIN_ROOT}", str(cached))
                              for arg in config.get("args", [])]
            workspace = base / "other project"
            workspace.mkdir()
            client = Client("gdb-mcp", workspace, os.environ.copy(), config=config)
            try:
                client.initialize()
                tools = client.request("tools/list")["tools"]
                self.assertIn("gdb_start_session", {tool["name"] for tool in tools})
            finally:
                client.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
