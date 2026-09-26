import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.config import settings
from app.workflow import build_graph
from pydantic import BaseModel


class PlanRequest(BaseModel):
    project_request: str


router = APIRouter(prefix="/api/v1", tags=["project"])


@router.post("/plan")
async def create_plan(request: PlanRequest):
    try:
        project_id = str(uuid.uuid4())[:8]
        project_workspace = Path(settings.WORKSPACE_PATH) / f"project-{project_id}"
        project_workspace.mkdir(parents=True, exist_ok=True)

        graph = build_graph()
        initial_state = {
            "project_id": project_id,
            "project_request": request.project_request,
            "requirements": "",
            "development_plan": "",
            "architecture": "",
            "tasks": [],
            "files_changed": [],
            "frontend_status": "",
            "backend_status": "",
            "test_results": {},
            "errors": [],
            "review_result": {},
            "documentation": "",
            "approval_status": "",
            "current_agent": "",
            "project_status": "",
            "workspace_path": str(project_workspace),
            "messages": [],
        }
        result = graph.invoke(initial_state)
        return {
            "status": "success",
            "project_id": project_id,
            "development_plan": result["development_plan"],
            "architecture": result["architecture"],
            "files_changed": result["files_changed"],
            "frontend_status": result["frontend_status"],
            "backend_status": result["backend_status"],
            "project_status": result["project_status"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
