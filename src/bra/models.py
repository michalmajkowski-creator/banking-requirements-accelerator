from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Status(StrEnum):
    DRAFT = "draft"
    COMPLETED = "completed"
    NEEDS_INPUT = "needs_input"
    STUBBED = "stubbed"
    NEEDS_APPROVAL = "needs_approval"
    FAILED = "failed"


class Initiative(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    problem: str
    desired_outcome: str
    sources: list[str] = Field(default_factory=list)
    stakeholders: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class Requirement(BaseModel):
    id: str
    type: str = "business"
    statement: str
    rationale: str | None = None
    owner: str | None = None
    source_refs: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    status: Status = Status.DRAFT
    version: int = 1


class Finding(BaseModel):
    rule_id: str
    severity: str
    message: str
    artifact_id: str | None = None


class StepResult(BaseModel):
    skill: str
    status: Status
    outputs: dict[str, Any] = Field(default_factory=dict)
    findings: list[Finding] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    approval_gate: str | None = None


class Run(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    pipeline: str
    initiative: Initiative
    status: Status = Status.DRAFT
    steps: list[StepResult] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RunRequest(BaseModel):
    pipeline: str = "mvp"
    initiative: Initiative
    requirements: list[Requirement] = Field(default_factory=list)

