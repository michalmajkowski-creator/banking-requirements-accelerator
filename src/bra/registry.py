from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class SkillSpec:
    name: str
    version: str
    strategy: str
    runtime: str
    approval_gate: str | None = None
    source: str | None = None


class SkillRegistry:
    def __init__(self, path: Path):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))["skills"]
        self._skills = {name: SkillSpec(name=name, **data) for name, data in raw.items()}

    def get(self, name: str) -> SkillSpec:
        if name not in self._skills:
            raise KeyError(f"Unknown skill: {name}")
        return self._skills[name]

