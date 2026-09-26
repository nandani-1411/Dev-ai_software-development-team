from typing import Self

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings
from app.mcp.filesystem import FilesystemTools


class FrontendCoderAgent:
    def __init__(self: Self, workspace_path: str) -> None:
        self.llm = ChatMistralAI(
            model="open-mistral-7b",
            api_key=settings.MISTRAL_API_KEY,
            temperature=0.3,
        )
        self.fs = FilesystemTools(workspace_path)

    def generate_frontend_code(self: Self, architecture: str) -> str:
        system_prompt = """You are a React frontend developer. Generate React component code based on the architecture.

Your output should be:
- Create the frontend folder structure
- Generate React components with proper imports
- Create pages and routing if needed
- Add basic styling
- Follow the architecture exactly

Return a summary of what files were created and their contents in a structured format."""

        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=architecture),
            ]
        )
        return response.content

    def write_frontend_files(self: Self, code_summary: str) -> list[str]:
        files_changed = []
        self.fs.create_directory("frontend/src")
        self.fs.create_directory("frontend/src/components")
        self.fs.create_directory("frontend/src/pages")

        base_component = """import React from 'react'

export default function TaskList() {
  return (
    <div>
      <h1>Task List</h1>
      <p>Tasks will be displayed here</p>
    </div>
  )
}
"""
        self.fs.write_file("frontend/src/components/TaskList.jsx", base_component)
        files_changed.append("frontend/src/components/TaskList.jsx")

        app_component = """import React from 'react'
import TaskList from './components/TaskList'

function App() {
  return (
    <div className="app">
      <h1>Task Management App</h1>
      <TaskList />
    </div>
  )
}

export default App
"""
        self.fs.write_file("frontend/src/App.jsx", app_component)
        files_changed.append("frontend/src/App.jsx")

        index_html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Task Management App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
        self.fs.write_file("frontend/index.html", index_html)
        files_changed.append("frontend/index.html")

        main_jsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
        self.fs.write_file("frontend/src/main.jsx", main_jsx)
        files_changed.append("frontend/src/main.jsx")

        package_json = """{
  "name": "task-management-app",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "18.3.1",
    "react-dom": "18.3.1"
  },
  "devDependencies": {
    "@types/react": "18.3.3",
    "@types/react-dom": "18.3.0",
    "@vitejs/plugin-react": "4.3.1",
    "vite": "5.4.1"
  }
}
"""
        self.fs.write_file("frontend/package.json", package_json)
        files_changed.append("frontend/package.json")

        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,
  },
})
"""
        self.fs.write_file("frontend/vite.config.js", vite_config)
        files_changed.append("frontend/vite.config.js")

        return files_changed
