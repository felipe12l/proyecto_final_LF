from fastapi import APIRouter, HTTPException
from controllers.analyzeController import analyzeJWT
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