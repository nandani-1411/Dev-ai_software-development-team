import subprocess
from typing import Self


class GitTools:
    def __init__(self: Self, workspace_path: str) -> None:
        self.workspace_path = workspace_path

    def _run_git(self: Self, args: list[str]) -> dict:
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out after 30 seconds",
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
            }

    def git_status(self: Self) -> dict:
        return self._run_git(["status", "--porcelain"])

    def git_diff(self: Self) -> dict:
        return self._run_git(["diff"])

    def git_log(self: Self, max_count: int = 10) -> dict:
        return self._run_git(["log", f"-{max_count}", "--oneline"])

    def git_add(self: Self, files: list[str]) -> dict:
        return self._run_git(["add"] + files)

    def git_commit(self: Self, message: str) -> dict:
        return self._run_git(["commit", "-m", message])
