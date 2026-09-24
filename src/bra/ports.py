from typing import Any, Protocol

from .models import RunRequest, StepResult


class SkillExecutor(Protocol):
    def execute(self, skill: str, request: RunRequest, context: dict[str, Any]) -> StepResult: ...


class LLMGateway(Protocol):
    def generate(self, task: str, payload: dict[str, Any]) -> dict[str, Any]: ...


class KnowledgeGateway(Protocol):
    def retrieve(self, query: str, scopes: list[str]) -> list[dict[str, Any]]: ...


class GraphStore(Protocol):
    def upsert_edges(self, edges: list[dict[str, Any]]) -> None: ...
    def impact(self, artifact_id: str) -> list[dict[str, Any]]: ...

