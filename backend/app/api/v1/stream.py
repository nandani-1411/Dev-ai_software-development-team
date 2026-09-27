from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter(prefix="/api/v1", tags=["stream"])


async def event_generator():
    events = [
        "Planner started",
        "Planner completed",
        "Designer started",
        "Designer completed",
        "Frontend Coder started",
        "Frontend Coder completed",
        "Backend Coder started",
        "Backend Coder completed",
        "Testing started",
        "Testing completed",
        "Review completed",
        "Documentation completed",
        "Git initialized",
    ]
    for event in events:
        yield f"data: {event}\n\n"
        await asyncio.sleep(0.5)


@router.get("/stream")
async def stream_events():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
