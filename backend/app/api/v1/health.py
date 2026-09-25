from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["status"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "DevAI API",
        "version": "0.1.0",
    }
