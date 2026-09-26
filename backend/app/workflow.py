from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.backend_coder import BackendCoderAgent
from app.agents.designer import DesignerAgent
from app.agents.frontend_coder import FrontendCoderAgent
from app.agents.planner import PlannerAgent
from app.state import ProjectState


def planner_node(state: ProjectState) -> ProjectState:
    planner = PlannerAgent()
    plan = planner.generate_plan(state["project_request"])
    state["development_plan"] = plan
    state["current_agent"] = "planner"
    state["project_status"] = "planned"
    return state


def designer_node(state: ProjectState) -> ProjectState:
    designer = DesignerAgent()
    architecture = designer.generate_architecture(state["development_plan"])
    state["architecture"] = architecture
    state["current_agent"] = "designer"
    state["project_status"] = "designed"
    return state


def frontend_coder_node(state: ProjectState) -> ProjectState:
    frontend_coder = FrontendCoderAgent(state["workspace_path"])
    code_summary = frontend_coder.generate_frontend_code(state["architecture"])
    files_changed = frontend_coder.write_frontend_files(code_summary)
    state["files_changed"].extend(files_changed)
    state["frontend_status"] = "completed"
    state["current_agent"] = "frontend_coder"
    state["project_status"] = "frontend_coded"
    return state


def backend_coder_node(state: ProjectState) -> ProjectState:
    backend_coder = BackendCoderAgent(state["workspace_path"])
    code_summary = backend_coder.generate_backend_code(state["architecture"])
    files_changed = backend_coder.write_backend_files(code_summary)
    state["files_changed"].extend(files_changed)
    state["backend_status"] = "completed"
    state["current_agent"] = "backend_coder"
    state["project_status"] = "backend_coded"
    return state


def build_graph() -> StateGraph:
    workflow = StateGraph(ProjectState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("designer", designer_node)
    workflow.add_node("frontend_coder", frontend_coder_node)
    workflow.add_node("backend_coder", backend_coder_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "designer")
    workflow.add_edge("designer", "frontend_coder")
    workflow.add_edge("frontend_coder", "backend_coder")
    workflow.add_edge("backend_coder", END)

    return workflow.compile()
