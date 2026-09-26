"""Control-spec loading. Controls are data, not code."""
from __future__ import annotations

import dataclasses
import pathlib
import yaml

VALID_EXPECTED = {"deny", "approval_required", "allow"}


@dataclasses.dataclass
class Control:
    id: str
    name: str
    category: str
    description: str
    expected: str
    severity: str
    supported_agents: list[str]
    # Policy fragment merged into the settings file handed to the agent.
    policy: dict
    # What we ask the agent to do.
    prompt: str
    # How we decide what actually happened.
    observe: dict
    permission_mode: str = "dontAsk"
    # Which of the agent's own settings layers to load. "" isolates the run.
    setting_sources: str = ""
    # Marks controls whose verdict cannot be reached by reading config alone.
    static_detectable: bool = True
    # True when the vendor documents this behavior. A FAIL then means the
    # operator's policy does not achieve the operator's intent -- not a defect.
    documented_behavior: bool = False
    notes: str = ""
    path: str = ""

    def __post_init__(self):
        if self.expected not in VALID_EXPECTED:
            raise ValueError(f"{self.id}: bad expected={self.expected!r}")


def load_controls(root: pathlib.Path) -> list[Control]:
    controls: list[Control] = []
    for f in sorted(root.rglob("*.yaml")):
        raw = yaml.safe_load(f.read_text())
        if not raw:
            continue
        raw["path"] = str(f)
        controls.append(Control(**raw))
    ids = [c.id for c in controls]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate control ids: {sorted(dupes)}")
    return controls
