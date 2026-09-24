from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .executors import DefaultExecutor
from .models import Run, RunRequest
from .orchestrator import Orchestrator
from .registry import SkillRegistry

ROOT = Path(__file__).resolve().parents[2]
registry = SkillRegistry(ROOT / "config" / "skills.yaml")
orchestrator = Orchestrator(ROOT / "config" / "pipelines.yaml", DefaultExecutor(registry))
runs: dict[UUID, Run] = {}
app = FastAPI(title="Banking Requirements Accelerator", version="0.2.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


@app.get("/", include_in_schema=False)
def workbench() -> FileResponse:
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/runs", response_model=Run)
def create_run(request: RunRequest) -> Run:
    try:
        run = orchestrator.run(request)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    runs[run.id] = run
    return run


@app.get("/v1/runs/{run_id}", response_model=Run)
def get_run(run_id: UUID) -> Run:
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run not found")
    return runs[run_id]
