from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health, project


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Phase 0: minimal startup/shutdown.
    # In later phases this will initialize ChromaDB, PostgreSQL, etc.
    yield


app = FastAPI(
    title="DevAI API",
    description="Autonomous software development team API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(project.router)


@app.get("/", tags=["status"])
def root():
    return {"message": "DevAI API is running", "version": "0.1.0"}
