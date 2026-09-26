from typing import Self

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings
from app.mcp.filesystem import FilesystemTools


class BackendCoderAgent:
    def __init__(self: Self, workspace_path: str) -> None:
        self.llm = ChatMistralAI(
            model="open-mistral-7b",
            api_key=settings.MISTRAL_API_KEY,
            temperature=0.3,
        )
        self.fs = FilesystemTools(workspace_path)

    def generate_backend_code(self: Self, architecture: str) -> str:
        system_prompt = """You are a FastAPI backend developer. Generate FastAPI routes and models based on the architecture.

Your output should be:
- Create the backend folder structure
- Generate FastAPI routes with proper imports
- Create Pydantic models for request/response
- Add basic API endpoints
- Follow the architecture exactly

Return a summary of what files were created and their contents in a structured format."""

        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=architecture),
            ]
        )
        return response.content

    def write_backend_files(self: Self, code_summary: str) -> list[str]:
        files_changed = []
        self.fs.create_directory("backend/app/models")
        self.fs.create_directory("backend/app/routes")

        models_init = ""
        self.fs.write_file("backend/app/models/__init__.py", models_init)
        files_changed.append("backend/app/models/__init__.py")

        task_model = """from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
"""
        self.fs.write_file("backend/app/models/task.py", task_model)
        files_changed.append("backend/app/models/task.py")

        routes_init = ""
        self.fs.write_file("backend/app/routes/__init__.py", routes_init)
        files_changed.append("backend/app/routes/__init__.py")

        task_routes = """from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.task import Task, TaskCreate


router = APIRouter(prefix="/api/tasks", tags=["tasks"])

tasks_db = []
task_id_counter = 1


@router.get("/", response_model=List[Task])
def get_tasks():
    return tasks_db


@router.post("/", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=datetime.now(),
    )
    tasks_db.append(new_task)
    task_id_counter += 1
    return new_task


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}")
def delete_task(task_id: int):
    global tasks_db
    tasks_db = [t for t in tasks_db if t.id != task_id]
    return {"message": "Task deleted"}
"""
        self.fs.write_file("backend/app/routes/tasks.py", task_routes)
        files_changed.append("backend/app/routes/tasks.py")

        main_py = """from fastapi import FastAPI
from routes.tasks import router as tasks_router

app = FastAPI(title="Task Management API")
app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Task Management API is running"}
"""
        self.fs.write_file("backend/app/main.py", main_py)
        files_changed.append("backend/app/main.py")

        app_init = ""
        self.fs.write_file("backend/app/__init__.py", app_init)
        files_changed.append("backend/app/__init__.py")

        requirements_txt = """fastapi==0.115.0
uvicorn==0.30.6
pydantic==2.9.2
"""
        self.fs.write_file("backend/requirements.txt", requirements_txt)
        files_changed.append("backend/requirements.txt")

        return files_changed
