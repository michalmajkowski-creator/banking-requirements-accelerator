from pathlib import Path

from bra.executors import DefaultExecutor
from bra.models import Initiative, Requirement, RunRequest, Status
from bra.orchestrator import Orchestrator
from bra.registry import SkillRegistry


root = Path(__file__).resolve().parents[1]
registry = SkillRegistry(root / "config" / "skills.yaml")
orchestrator = Orchestrator(root / "config" / "pipelines.yaml", DefaultExecutor(registry))
request = RunRequest(
    initiative=Initiative(title="Limity", problem="Brak samoobsługi", desired_outcome="Samoobsługa", sources=["warsztat"]),
    requirements=[Requirement(id="BR-1", statement="System ma szybko zmienić limit", owner="Payments")],
)
run = orchestrator.run(request)
lint = next(step for step in run.steps if step.skill == "requirement-linting")
assert run.status == Status.NEEDS_INPUT
assert any(step.status == Status.STUBBED for step in run.steps)
assert {"REQ-QUALITY-003", "REQ-QUALITY-005"} <= {finding.rule_id for finding in lint.findings}
print("Smoke test passed")
