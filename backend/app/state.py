from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class ProjectState(TypedDict):
    project_id: str
    project_request: str
    requirements: str
    development_plan: str
    architecture: str
    tasks: list[str]
    files_changed: list[str]
    frontend_status: str
    backend_status: str
    test_results: dict
    errors: list[str]
    review_result: dict
    documentation: str
    approval_status: str
    current_agent: str
    project_status: str
    workspace_path: str
    messages: Annotated[list, add_messages]
