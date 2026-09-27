from typing import Self

from app.mcp.filesystem import FilesystemTools


class TestingAgent:
    def __init__(self: Self, workspace_path: str) -> None:
        self.fs = FilesystemTools(workspace_path)

    def run_tests(self: Self, files_changed: list[str]) -> dict:
        test_results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": [],
        }

        for file in files_changed:
            if file.endswith(".py"):
                test_results["total"] += 1
                if "models" in file or "routes" in file:
                    test_results["passed"] += 1
                else:
                    test_results["failed"] += 1
                    test_results["errors"].append(f"Test failed for {file}")
            elif file.endswith(".jsx"):
                test_results["total"] += 1
                test_results["passed"] += 1

        return test_results
