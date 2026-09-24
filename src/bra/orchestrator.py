from pathlib import Path

import yaml

from .executors import DefaultExecutor
from .models import Run, RunRequest, Status


class Orchestrator:
    def __init__(self, pipelines_path: Path, executor: DefaultExecutor):
        self.pipelines = yaml.safe_load(pipelines_path.read_text(encoding="utf-8"))["pipelines"]
        self.executor = executor

    def run(self, request: RunRequest) -> Run:
        if request.pipeline not in self.pipelines:
            raise KeyError(f"Unknown pipeline: {request.pipeline}")
        run = Run(pipeline=request.pipeline, initiative=request.initiative)
        context = {}
        for skill in self.pipelines[request.pipeline]:
            step = self.executor.execute(skill, request, context)
            run.steps.append(step)
            context[skill] = step.model_dump(mode="json")
        actionable = any(s.status in {Status.NEEDS_INPUT, Status.FAILED} for s in run.steps)
        run.status = Status.NEEDS_INPUT if actionable else Status.NEEDS_APPROVAL
        return run

