from typing import Self

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings


class DesignerAgent:
    def __init__(self: Self) -> None:
        self.llm = ChatMistralAI(
            model="open-mistral-7b",
            api_key=settings.MISTRAL_API_KEY,
            temperature=0.3,
        )

    def generate_architecture(self: Self, development_plan: str) -> str:
        system_prompt = """You are a software architect. Convert the development plan into a system architecture design.

Your output should cover:
- System architecture (how components connect)
- Frontend structure (React components, pages, state management)
- Backend structure (FastAPI routes, models, services)
- Database schema (tables, relationships)
- API design (endpoints, request/response formats)
- Technology decisions (why these choices)

Keep the architecture clear, structured, and understandable for a student developer. Return only the architecture text, no explanations outside the architecture."""

        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=development_plan),
            ]
        )
        return response.content
