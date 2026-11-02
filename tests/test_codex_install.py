"""Install a clean plugin copy and exercise it through Codex's app server."""

import json
import os
import queue
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("codex") and shutil.which("uvx"),
                     "codex and uvx are required")
class CodexInstallTests(unittest.TestCase):
    def test_installed_plugin_exposes_and_runs_its_servers(self):
        with tempfile.TemporaryDirectory(prefix="skilled-c-install-", ignore_cleanup_errors=True) as temp:
            base = Path(temp)
            source = base / "source"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(
                ".git", "node_modules", "__pycache__", ".venv", ".pytest_tmp"
            ))
            state = base / "codex-state"
            state.mkdir()
            workspace = base / "workspace"
            workspace.mkdir()
            env = os.environ.copy()
            env["CODEX_HOME"] = str(state)
            env["APPDATA"] = str(base / "appdata")
            env["RUST_LOG"] = "info"
            options = [
                "-c", 'marketplaces.skilled-c-local.source_type="local"',
                "-c", "marketplaces.skilled-c-local.source=" + json.dumps(source.as_posix()),
            ]
            codex = shutil.which("codex")
            install = subprocess.run(
                [codex, *options, "plugin", "add", "skilled-c@skilled-c-local", "--json"],
                cwd=workspace, env=env, capture_output=True, text=True, timeout=60, check=True,
            )
            cached = Path(json.loads(install.stdout)["installedPath"])
            if os.name == "nt":
                with (state / "config.toml").open("a", encoding="utf-8") as config:
                    config.write('\n[plugins."skilled-c@skilled-c-local".mcp_servers.renderdoc-mcp]\nenabled = true\n')
            entrypoint = cached / "skills/skilled-c/SKILL.md"
            self.assertTrue(entrypoint.is_file())
            self.assertIn("\nname: skilled-c\n", entrypoint.read_text(encoding="utf-8"))
            self.assertFalse((cached / "skills/c-programming").exists())
            self.assertTrue((cached / "mcp/gdb-mcp/pyproject.toml").is_file())
            self.assertTrue((cached / "mcp/renderdoc-mcp/pyproject.toml").is_file())

            app = subprocess.Popen(
                [codex, *options, "app-server"], cwd=workspace, env=env,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8",
            )
            lines = queue.Queue()
            errors = []

            def read(stream, consume):
                for line in stream:
                    consume(line)

            stdout_reader = threading.Thread(target=read, args=(app.stdout, lines.put), daemon=True)
            stdout_reader.start()
            stderr_reader = threading.Thread(target=read, args=(app.stderr, errors.append), daemon=True)
            stderr_reader.start()

            def request(request_id, method, params):
                app.stdin.write(json.dumps({"id": request_id, "method": method, "params": params}) + "\n")
                app.stdin.flush()
                while True:
                    try:
                        response = json.loads(lines.get(timeout=120))
                    except queue.Empty as exc:
                        raise AssertionError(f"Codex response timed out: {''.join(errors)}") from exc
                    if response.get("id") == request_id:
                        self.assertNotIn("error", response, response)
                        return response["result"]

            try:
                request(1, "initialize", {"clientInfo": {"name": "skilled-c-test", "version": "1.0"}})
                skill_list = request(2, "skills/list", {"cwds": [str(workspace)], "forceReload": True})
                bundled = [skill for entry in skill_list["data"] for skill in entry["skills"]
                           if skill.get("pluginId") == "skilled-c@skilled-c-local"]
                self.assertEqual(len(bundled), 1, bundled)
                self.assertIn(bundled[0]["name"], {"skilled-c", "skilled-c:skilled-c"})
                self.assertTrue(bundled[0]["enabled"])

                servers = {item["name"]: item for item in request(3, "mcpServerStatus/list", {})["data"]}
                names = ["gdb-mcp"]
                if os.name == "nt":
                    names.append("renderdoc-mcp")
                for name in names:
                    self.assertTrue(servers[name]["tools"], f"{name}: {servers[name]['toolsError']}; {''.join(errors)[-4000:]}")

                thread = request(4, "thread/start", {
                    "cwd": str(workspace), "ephemeral": True, "approvalPolicy": "never",
                })["thread"]["id"]
                result = request(5, "mcpServer/tool/call", {
                    "threadId": thread, "server": "gdb-mcp", "tool": "gdb_get_status",
                    "arguments": {"session_id": 0},
                })
                self.assertIn("Invalid session_id: 0", json.dumps(result))
            finally:
                app.stdin.close()
                try:
                    app.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    app.terminate()
                    app.wait(timeout=10)
                stdout_reader.join(timeout=2)
                stderr_reader.join(timeout=2)
                app.stdout.close()
                app.stderr.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
