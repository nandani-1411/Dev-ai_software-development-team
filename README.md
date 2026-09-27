# DevAI — Autonomous Software Development Team

DevAI is a multi-agent autonomous software-development platform. It uses specialized AI agents coordinated by LangGraph to plan, design, code, test, debug, review, and document software projects, with human approval for sensitive operations.

## Features

- **Multi-Agent Workflow**: Planner, Designer, Frontend Coder, Backend Coder, Tester, Debugger, Reviewer, Documentation, Git
- **LangGraph Orchestration**: Manages agent execution order, shared state, and conditional routing
- **MCP Tools**: Filesystem, Terminal, Git tools for agents
- **RAG/Project Memory**: Simple in-memory document retrieval for agents
- **SSE Streaming**: Real-time agent activity updates in the dashboard
- **Human Approval**: Basic approval system for sensitive operations
- **Generated Projects**: Each project gets its own workspace directory

## Technology Stack

- **Backend:** Python, FastAPI, LangChain, LangGraph, Mistral AI
- **Frontend:** React, JavaScript, Vite
- **DevOps:** Git
- **Communication:** SSE for live progress

## Folder Structure

```
.
├── .env                 # Local secrets (not committed)
├── .env.example         # Secret template
├── .gitignore
├── README.md
├── docs/
│   └── architecture.md
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── run.py           # Entry point for dev server
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── state.py     # LangGraph shared state
│       ├── workflow.py  # LangGraph graph
│       ├── rag.py       # Simple RAG manager
│       ├── agents/      # All agent implementations
│       ├── mcp/         # MCP tools (filesystem, terminal, git)
│       └── api/v1/      # API endpoints
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── main.jsx
        └── App.css
```

## Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python run.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```
MISTRAL_API_KEY=your_mistral_api_key_here
DATABASE_URL=postgresql://devai_user:devai_pass@localhost:5432/devai_db
GITHUB_TOKEN=your_github_token_here
WORKSPACE_PATH=D:/DevAI/workspaces
```

## Usage

1. Start the backend (port 8000)
2. Start the frontend (port 5173)
3. Open the dashboard at http://localhost:5173
4. Enter a project requirement
5. Click "Generate Full Project"
6. Watch the agent activity stream
7. View the generated project in the workspace directory

## Project Workflow

```
User Request
    ↓
Planner Agent (with RAG context)
    ↓
Designer Agent
    ↓
Frontend Coder + Backend Coder
    ↓
Testing Agent
    ↓
Debugger (if tests fail) → Testing again
    ↓
Reviewer Agent
    ↓
Documentation Agent
    ↓
Git Initialization
    ↓
Completed Project
```

## Resume Description

Built a multi-agent autonomous software-development platform using LangGraph and MCP to coordinate planning, architecture, coding, testing, debugging, code review, and documentation, with RAG-based project memory and human-in-the-loop approval for sensitive operations.
