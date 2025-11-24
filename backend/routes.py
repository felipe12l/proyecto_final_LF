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

    save_analysis(token, normalize({
        "status": result.get("status"),
        "phase": result.get("phase"),
        "message": result.get("message"),
        "header": result.get("header"),        
        "payload": result.get("payload"),     
        "signature": result.get("signature"),
    }))

    return result


@router.post("/api/encode")
def encode(data: dict):
    return encode_jwt(data)
@router.get("/api/get_tests")
def get_tests():
    return analyze_repository()