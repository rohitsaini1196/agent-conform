"""Claude Code adapter: drives the real installed binary, never a simulation."""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess

from .base import Adapter, AgentRun

DEFAULT_MODEL = os.environ.get("AGENT_CONFORM_MODEL", "claude-haiku-4-5-20251001")
# Lets one host test several installed versions without reinstalling.
BINARY_OVERRIDE = os.environ.get("AGENT_CONFORM_CLAUDE_BINARY")


class ClaudeAdapter(Adapter):
    name = "claude"

    def __init__(self, binary: str | None = None, model: str = DEFAULT_MODEL):
        self.binary = binary or BINARY_OVERRIDE or shutil.which("claude") or "claude"
        self.model = model

    def available(self) -> bool:
        return shutil.which(self.binary) is not None or pathlib.Path(self.binary).exists()

    def version(self) -> str:
        try:
            out = subprocess.run(
                [self.binary, "--version"], capture_output=True, text=True, timeout=60
            )
            return out.stdout.strip().split(" ")[0] or "unknown"
        except Exception:
            return "unknown"

    def run(self, *, prompt, settings_path, cwd, permission_mode, extra_args, env,
            setting_sources="") -> AgentRun:
        cmd = [
            self.binary,
            "-p", prompt,
            "--settings", str(settings_path),
            "--setting-sources", setting_sources,  # "" ignores the operator's own settings
            "--model", self.model,
            "--output-format", "stream-json",
            "--verbose",
            "--no-session-persistence",
            "--disable-slash-commands",
        ]
        if permission_mode:
            cmd += ["--permission-mode", permission_mode]
        cmd += list(extra_args or [])

        runenv = dict(os.environ)
        runenv.update(env or {})
        runenv["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
        # Versions before ~2.1.89 refuse to launch inside another Claude Code
        # session. Leaving these set makes every run on an older binary fail
        # with exit 1 and look like the agent declined to act.
        for k in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT"):
            runenv.pop(k, None)

        try:
            proc = subprocess.run(
                cmd, cwd=str(cwd), capture_output=True, text=True, timeout=300, env=runenv
            )
        except subprocess.TimeoutExpired:
            return AgentRun(False, -1, self.version(), [], [], "", "", "", "timeout")

        raw = pathlib.Path(cwd).parent / "transcript.jsonl"
        raw.write_text(proc.stdout)

        tool_calls, denials, final_text = [], [], ""
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "assistant":
                for block in ev.get("message", {}).get("content", []):
                    if block.get("type") == "tool_use":
                        tool_calls.append({"name": block.get("name"), "input": block.get("input")})
                    elif block.get("type") == "text":
                        final_text += block.get("text", "")
            elif ev.get("type") == "user":
                # tool results carry denial text back to the model
                for block in ev.get("message", {}).get("content", []) or []:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        c = block.get("content")
                        final_text += "\n[tool_result] " + (
                            c if isinstance(c, str) else json.dumps(c)[:2000]
                        )
            elif ev.get("type") == "result":
                denials = ev.get("permission_denials", []) or []
                if ev.get("result"):
                    final_text += "\n[result] " + str(ev["result"])

        return AgentRun(
            ok=True,
            exit_code=proc.returncode,
            agent_version=self.version(),
            tool_calls=tool_calls,
            denials=denials,
            final_text=final_text,
            stderr=proc.stderr[-4000:],
            raw_path=str(raw),
        )
