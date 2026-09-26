import os
from pathlib import Path
from typing import Self


class FilesystemTools:
    def __init__(self: Self, workspace_path: str) -> None:
        self.workspace_path = Path(workspace_path).resolve()
        if not self.workspace_path.exists():
            self.workspace_path.mkdir(parents=True, exist_ok=True)

    def list_files(self: Self, path: str = "") -> list[str]:
        target_path = self.workspace_path / path if path else self.workspace_path
        if not target_path.exists():
            return []
        return sorted([f.name for f in target_path.iterdir()])

    def read_file(self: Self, path: str) -> str:
        target_path = self.workspace_path / path
        if not target_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return target_path.read_text(encoding="utf-8")

    def write_file(self: Self, path: str, content: str) -> None:
        target_path = self.workspace_path / path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")

    def create_directory(self: Self, path: str) -> None:
        target_path = self.workspace_path / path
        target_path.mkdir(parents=True, exist_ok=True)

    def search_files(self: Self, pattern: str) -> list[str]:
        matches = []
        for root, dirs, files in os.walk(self.workspace_path):
            for file in files:
                if pattern.lower() in file.lower():
                    rel_path = Path(root).relative_to(self.workspace_path) / file
                    matches.append(str(rel_path))
        return matches
