from pathlib import Path

from bra.executors import DefaultExecutor
from bra.models import Initiative, Requirement, RunRequest, Status
from bra.orchestrator import Orchestrator
from bra.registry import SkillRegistry

ROOT = Path(__file__).resolve().parents[1]


def build_orchestrator() -> Orchestrator:
    registry = SkillRegistry(ROOT / "config" / "skills.yaml")
    return Orchestrator(ROOT / "config" / "pipelines.yaml", DefaultExecutor(registry))


def test_pipeline_exposes_stubs_and_never_fakes_completion():
    req = RunRequest(initiative=Initiative(title="Limity", problem="Brak samoobsługi", desired_outcome="Samoobsługa"))
    run = build_orchestrator().run(req)
    assert run.status == Status.NEEDS_INPUT
    assert any(step.status == Status.STUBBED for step in run.steps)


def test_linter_flags_subjective_requirement_and_missing_source():
    req = RunRequest(
        initiative=Initiative(title="Limity", problem="Brak", desired_outcome="Zmiana", sources=["warsztat"]),
        requirements=[Requirement(id="BR-1", statement="System ma szybko zmienić limit", owner="Payments")],
    )
    run = build_orchestrator().run(req)
    lint = next(step for step in run.steps if step.skill == "requirement-linting")
    assert {f.rule_id for f in lint.findings} >= {"REQ-QUALITY-003", "REQ-QUALITY-005"}

