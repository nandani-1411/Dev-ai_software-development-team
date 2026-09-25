# DevAI — Autonomous Software Development Team

DevAI is a multi-agent autonomous software-development platform. It uses specialized AI agents coordinated by LangGraph to plan, design, code, test, debug, review, and document software projects, with human approval for sensitive operations.

## Current Phase

**Phase 0 — Project Setup**

This phase sets up the project structure, a minimal FastAPI backend, a minimal React frontend, Git, and environment configuration. No agents are implemented yet.

## Technology Stack

- **Backend:** Python, FastAPI, LangChain, LangGraph, Mistral AI, ChromaDB, PostgreSQL
- **Frontend:** React, JavaScript, Vite
- **DevOps:** Git, GitHub
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
│       └── api/v1/
│           └── health.py
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── main.jsx
        └── ...
```

## Setup

### Backend

```bash
cd backend
python -m venv .venv
. .venv/bin/activate  # On Windows: .venv\Scripts\activate
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

Copy `.env.example` to `.env` and fill in the values. The `.env` file is never committed to Git.

## Next Steps

Phase 1 will add the **Planner Agent** and the first LangGraph workflow: React → FastAPI → LangGraph → Planner → Plan → React.
