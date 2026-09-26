"""Codex adapter — stub. v0 is Claude Code only.

Kept so the shape of a second adapter is explicit: the runner is agent-agnostic,
only command construction and transcript parsing live here.
"""
from __future__ import annotations

import shutil

from .base import Adapter, AgentRun


class CodexAdapter(Adapter):
    name = "codex"

    def available(self) -> bool:
        return shutil.which("codex") is not None

    def version(self) -> str:
        return "not-implemented"

    def run(self, **kw) -> AgentRun:
        return AgentRun(False, -1, "not-implemented", [], [], "", "", "", "codex adapter not implemented")
