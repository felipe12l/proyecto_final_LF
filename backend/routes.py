from fastapi import APIRouter, HTTPException
from controllers.analyzeController import analyzeJWT, analyze_repository, analyze_repository_summary
from controllers.encodeController import encode_jwt
router = APIRouter()

@router.post("/api/analyze")
def analyze(data: dict):
    token = data.get("token")
    if not token:
        raise HTTPException(400, "token requerido")
    return analyzeJWT(token)


@router.post("/api/encode")
def encode(data: dict):
    return encode_jwt(data)
@router.get("/api/get_tests")
def get_tests():
    return analyze_repository()

@router.get("/api/analyze_all")
def analyze_all():
    return analyze_repository_summary()