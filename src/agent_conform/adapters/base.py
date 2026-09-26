from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class AgentRun:
    """Normalized result of executing one prompt against a real agent binary."""

    ok: bool
    exit_code: int
    agent_version: str
    tool_calls: list[dict]          # every tool_use the agent emitted
    denials: list[dict]             # tool calls the harness refused
    final_text: str
    stderr: str
    raw_path: str                   # transcript on disk, for evidence
    error: str = ""

    @property
    def attempted(self) -> bool:
        return bool(self.tool_calls)


class Adapter:
    name = "base"

    def version(self) -> str:
        raise NotImplementedError

    def available(self) -> bool:
        raise NotImplementedError

    def run(self, *, prompt, settings_path, cwd, permission_mode, extra_args, env) -> AgentRun:
        raise NotImplementedError
