from .claude import ClaudeAdapter
from .codex import CodexAdapter

ADAPTERS = {"claude": ClaudeAdapter, "codex": CodexAdapter}
