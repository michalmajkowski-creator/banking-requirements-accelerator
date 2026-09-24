import re
from typing import Any

from .models import Finding, RunRequest, Status, StepResult
from .registry import SkillRegistry


SUBJECTIVE = re.compile(r"\b(szybko|łatwo|przyjazn\w*|odpowiedni\w*|niezwłocznie|fast|easy|user-friendly|appropriate|as soon as possible)\b", re.I)


class DefaultExecutor:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry

    def execute(self, skill: str, request: RunRequest, context: dict[str, Any]) -> StepResult:
        spec = self.registry.get(skill)
        if spec.runtime == "stub":
            return StepResult(skill=skill, status=Status.STUBBED, approval_gate=spec.approval_gate,
                              questions=[f"Skill '{skill}' wymaga implementacji lub podłączenia zatwierdzonego adaptera."])
        handler = getattr(self, f"_{skill.replace('-', '_')}")
        result = handler(request, context)
        result.approval_gate = spec.approval_gate
        return result

    def _idea_refinement(self, request: RunRequest, _: dict[str, Any]) -> StepResult:
        brief = request.initiative.model_dump(mode="json")
        questions = []
        if not request.initiative.stakeholders:
            questions.append("Kto jest właścicielem biznesowym i które grupy interesariuszy odczuje zmianę?")
        if not request.initiative.constraints:
            questions.append("Jakie ograniczenia regulacyjne, operacyjne, danych i architektury obowiązują?")
        return StepResult(skill="idea-refinement", status=Status.NEEDS_INPUT if questions else Status.COMPLETED,
                          outputs={"business_brief": brief}, questions=questions)

    def _requirements_elicitation(self, request: RunRequest, _: dict[str, Any]) -> StepResult:
        questions = []
        if not request.initiative.sources:
            questions.append("Jakie źródła potwierdzają potrzebę i zakres zmiany?")
        if not request.requirements:
            questions.append("Brak zatwierdzonych wymagań wejściowych; należy je zebrać lub wygenerować jako draft.")
        return StepResult(skill="requirements-elicitation", status=Status.NEEDS_INPUT if questions else Status.COMPLETED,
                          questions=questions)

    def _requirement_linting(self, request: RunRequest, _: dict[str, Any]) -> StepResult:
        findings: list[Finding] = []
        for req in request.requirements:
            if SUBJECTIVE.search(req.statement):
                findings.append(Finding(rule_id="REQ-QUALITY-003", severity="error", artifact_id=req.id,
                                        message="Wymaganie zawiera subiektywne lub niemierzalne określenie."))
            if not req.source_refs:
                findings.append(Finding(rule_id="REQ-QUALITY-005", severity="error", artifact_id=req.id,
                                        message="Wymaganie nie ma źródła."))
            if not req.owner:
                findings.append(Finding(rule_id="REQ-QUALITY-008", severity="warning", artifact_id=req.id,
                                        message="Wymaganie nie ma właściciela."))
            if len(re.findall(r"\b(?:oraz|i|and)\b", req.statement, re.I)) > 2:
                findings.append(Finding(rule_id="REQ-QUALITY-001", severity="warning", artifact_id=req.id,
                                        message="Wymaganie może nie być atomowe."))
        return StepResult(skill="requirement-linting", status=Status.NEEDS_INPUT if findings else Status.COMPLETED,
                          findings=findings, outputs={"checked": len(request.requirements)})

