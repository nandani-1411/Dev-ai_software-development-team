from typing import Self

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings
from app.rag import RAGManager


class PlannerAgent:
    def __init__(self: Self) -> None:
        self.llm = ChatMistralAI(
            model="open-mistral-7b",
            api_key=settings.MISTRAL_API_KEY,
            temperature=0.3,
        )
        self.rag = RAGManager()
        self.rag.add_document("architecture", "Use React for frontend, FastAPI for backend, SQLite for database")

    def generate_plan(self: Self, project_request: str) -> str:
        context = self.rag.search(project_request)
        context_str = "\n".join(context) if context else ""

        system_prompt = f"""You are a software development planner. Convert the user's project requirement into a structured development plan.

Relevant context from project memory:
{context_str}

Your output should be a numbered list of steps covering:
1. Requirements definition
2. User and feature definition
3. Frontend requirements
4. Backend requirements
5. Database requirements
6. API endpoints
7. Testing requirements

Keep the plan clear, specific, and actionable. Return only the plan text, no explanations outside the plan."""

        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=project_request),
            ]
        )
        return response.content
