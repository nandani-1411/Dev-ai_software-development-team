# DevAI Architecture

## Overview

DevAI is a multi-agent software development system. A user submits a software requirement through the React dashboard. The FastAPI backend passes the request to a LangGraph orchestrator, which routes work to specialized agents. Each agent reads from and writes to a shared `ProjectState`.

```text
Browser
  ↓
React Dashboard
  ↓
FastAPI Backend
  ↓
LangGraph Orchestrator
  ↓
Specialized Agents (Planner, Designer, Frontend, Backend, Tester, Debugger, Reviewer, Documentation)
  ↓
MCP Tools (filesystem, terminal, git, GitHub)
  ↓
Project Workspace

RAG / ChromaDB = project knowledge
PostgreSQL = project metadata and execution logs
```

## Shared State

LangGraph manages a typed `ProjectState` that holds the user request, plan, architecture, tasks, code status, test results, and approvals.

## Human-in-the-Loop

Sensitive operations (file modifications, terminal commands, Git push, GitHub repo creation) require user approval through the React dashboard.

## RAG / Memory

Project documents are chunked, embedded using Mistral, and stored in ChromaDB. Agents query this memory to avoid rediscovering the whole project every step.

## Phase 0 Status

In Phase 0, only the project skeleton, FastAPI backend, and React frontend are set up. No agents or LangGraph workflow is implemented yet.
