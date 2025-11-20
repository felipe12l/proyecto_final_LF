from fastapi import APIRouter, HTTPException
from controllers.analyze import analyzeJWT

router = APIRouter()

@router.post("/api/analyze")
def analyze(data: dict):
    token = data.get("token")
    if not token:
        raise HTTPException(400, "token requerido")
    return analyzeJWT(token)