from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.backend_coder import BackendCoderAgent
from app.agents.designer import DesignerAgent
from app.agents.frontend_coder import FrontendCoderAgent
from app.agents.planner import PlannerAgent
from app.agents.tester import TestingAgent
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


def tester_node(state: ProjectState) -> ProjectState:
    tester = TestingAgent(state["workspace_path"])
    test_results = tester.run_tests(state["files_changed"])
    state["test_results"] = test_results
    state["current_agent"] = "tester"
    if test_results["failed"] > 0:
        state["project_status"] = "tests_failed"
        state["errors"] = test_results["errors"]
    else:
        state["project_status"] = "tests_passed"
    return state


def should_debug(state: ProjectState) -> str:
    if state["test_results"].get("failed", 0) > 0 and state.get("debug_attempts", 0) < 3:
        return "debugger"
    return "reviewer"


def debugger_node(state: ProjectState) -> ProjectState:
    state["current_agent"] = "debugger"
    state["errors"] = []
    state["project_status"] = "debugged"
    state["debug_attempts"] = state.get("debug_attempts", 0) + 1
    return state


def reviewer_node(state: ProjectState) -> ProjectState:
    state["current_agent"] = "reviewer"
    state["review_result"] = {"status": "PASS", "issues": []}
    state["project_status"] = "reviewed"
    return state


def docs_agent_node(state: ProjectState) -> ProjectState:
    state["current_agent"] = "documentation"
    state["documentation"] = "Project generated successfully by DevAI"
    state["project_status"] = "documented"
    return state


def git_node(state: ProjectState) -> ProjectState:
    from app.mcp.git import GitTools
    git = GitTools(state["workspace_path"])
    git._run_git(["init"])
    git._run_git(["add", "."])
    git._run_git(["commit", "-m", "Initial commit by DevAI"])
    state["current_agent"] = "git"
    state["project_status"] = "git_initialized"
    return state


def build_graph() -> StateGraph:
    workflow = StateGraph(ProjectState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("designer", designer_node)
    workflow.add_node("frontend_coder", frontend_coder_node)
    workflow.add_node("backend_coder", backend_coder_node)
    workflow.add_node("tester", tester_node)
    workflow.add_node("debugger", debugger_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("docs_agent", docs_agent_node)
    workflow.add_node("git", git_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "designer")
    workflow.add_edge("designer", "frontend_coder")
    workflow.add_edge("frontend_coder", "backend_coder")
    workflow.add_edge("backend_coder", "tester")
    workflow.add_conditional_edges("tester", should_debug)
    workflow.add_edge("debugger", "tester")
    workflow.add_edge("reviewer", "docs_agent")
    workflow.add_edge("docs_agent", "git")
    workflow.add_edge("git", END)

    return workflow.compile()
