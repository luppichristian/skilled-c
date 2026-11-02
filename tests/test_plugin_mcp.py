"""Exercise the plugin's configured MCP servers through their stdio protocol."""

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


class Client:
    def __init__(self, name, workspace, env, *, config=None):
        if config is None:
            manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
            config = json.loads((ROOT / manifest["mcpServers"]).read_text(encoding="utf-8"))["mcpServers"][name]
        command = [config["command"], *config.get("args", [])]
        executable = shutil.which(command[0])
        if executable is None:
            raise unittest.SkipTest(f"{command[0]} is not installed")
        command[0] = executable
        self.proc = subprocess.Popen(
            command,
            cwd=ROOT / config.get("cwd", workspace),
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        self.lines = queue.Queue()
        self.errors = []
        threading.Thread(target=self._read_stdout, daemon=True).start()
        threading.Thread(target=self._read, args=(self.proc.stderr, self.errors.append), daemon=True).start()
        self.next_id = 0

    @staticmethod
    def _read(stream, consume):
        for line in stream:
            consume(line)

    def _read_stdout(self):
        self._read(self.proc.stdout, self.lines.put)
        self.lines.put(None)

    def send(self, message):
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()

    def request(self, method, params=None):
        self.next_id += 1
        request_id = self.next_id
        self.send({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}})
        while True:
            try:
                line = self.lines.get(timeout=120)
            except queue.Empty as exc:
                raise AssertionError(f"MCP response timed out; stderr: {''.join(self.errors)}") from exc
            if line is None:
                self.proc.wait(timeout=10)
                raise AssertionError(f"MCP server exited ({self.proc.returncode}); stderr: {''.join(self.errors)}")
            message = json.loads(line)
            if message.get("id") == request_id:
                if "error" in message:
                    raise AssertionError(f"MCP error: {message['error']}")
                return message["result"]

    def initialize(self):
        result = self.request("initialize", {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "skilled-c-smoke-test", "version": "1.0"},
        })
        self.send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return result

    def call(self, name, arguments):
        result = self.request("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError"):
            raise AssertionError(f"{name} failed: {result}")
        return result

    def close(self):
        self.proc.stdin.close()
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=10)
        self.proc.stdout.close()
        self.proc.stderr.close()


class PluginMcpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skilled-c-test-")
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.env = os.environ.copy()
        # RenderDoc installs its extension on startup. Keep that write isolated.
        self.env["APPDATA"] = str(self.workspace / "appdata")

    def connect(self, name):
        client = Client(name, self.workspace, self.env)
        self.addCleanup(client.close)
        client.initialize()
        return client

    def test_gdb_server_lists_tools(self):
        client = self.connect("gdb-mcp")
        tools = client.request("tools/list")["tools"]
        self.assertIn("gdb_start_session", {tool["name"] for tool in tools})

    def test_gdb_can_start_and_stop_a_session(self):
        gdb = self.env.get("GDB_PATH") or shutil.which("gdb")
        if not gdb:
            self.skipTest("GDB is not installed or GDB_PATH is not set")
        client = self.connect("gdb-mcp")
        result = client.call("gdb_start_session", {"gdb_path": gdb})
        session = json.loads(result["content"][0]["text"])
        self.assertNotEqual(session.get("status"), "error", session)
        self.assertIn("session_id", session)
        stopped = client.call("gdb_stop_session", {"session_id": session["session_id"]})
        self.assertNotEqual(json.loads(stopped["content"][0]["text"]).get("status"), "error")

    @unittest.skipUnless(os.name == "nt", "renderdoc-mcp supports Windows")
    def test_renderdoc_server_reports_status(self):
        client = self.connect("renderdoc-mcp")
        result = client.call("renderdoc_get_server_status", {})
        self.assertTrue(result.get("content") or result.get("structuredContent"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
