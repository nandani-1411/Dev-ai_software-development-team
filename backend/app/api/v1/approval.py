from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class ApprovalRequest(BaseModel):
    project_id: str
    action: str
    approved: bool


router = APIRouter(prefix="/api/v1", tags=["approval"])


@router.post("/approve")
async def handle_approval(request: ApprovalRequest):
    return {
        "status": "success",
        "project_id": request.project_id,
        "action": request.action,
        "approved": request.approved,
        "message": f"{request.action} {'approved' if request.approved else 'rejected'}",
    }
