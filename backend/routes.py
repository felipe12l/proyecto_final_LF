from fastapi import APIRouter, HTTPException
from controllers.analyzeController import analyzeJWT
from controllers.encodeController import encode_jwt
from controllers.analyzeController import analyze_repository
from database.db import save_analysis
router = APIRouter()

@router.post("/api/analyze")
def analyze(data: dict):
    token = data.get("token")
    if not token:
        raise HTTPException(400, "token requerido")

    result = analyzeJWT(token)

    if result.get("status") == "ok":
        save_analysis(token, result)
    return result


@router.post("/api/encode")
def encode(data: dict):
    return encode_jwt(data)
@router.get("/api/get_tests")
def get_tests():
    return analyze_repository()