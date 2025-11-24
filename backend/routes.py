from fastapi import APIRouter, HTTPException
from controllers.analyzeController import analyzeJWT
from controllers.encodeController import encode_jwt
from controllers.analyzeController import analyze_repository
from controllers.analyzeController import analyze_repository_summary
from controllers.encodeController import get_encoded_tokens, test_encode_repository

from database.db import DatabaseConnector

router = APIRouter()

def _normalize(data: dict):
    """Normaliza el diccionario eliminando None y valores inútiles."""
    return {k: v for k, v in data.items() if v is not None}

@router.post("/api/analyze")
def analyze(data: dict):
    token = data.get("token")
    if not token:
        raise HTTPException(400, "token requerido")

    result = analyzeJWT(token)

    DatabaseConnector.save_analysis(
        token,
        _normalize({
            "status": result.get("status"),
            "phase": result.get("phase"),
            "message": result.get("message"),
            "header": result.get("header"),        
            "payload": result.get("payload"),     
            "signature": result.get("signature"),
        })
    )

    return result


@router.post("/api/encode")
def encode(data: dict):
    return encode_jwt(data)

@router.get("/api/get_tests")
def get_tests():
    return analyze_repository()

@router.get("/api/analyze_all")
def analyze_all():
    return analyze_repository_summary()

@router.get("/api/get_encoded_tests")
def get_encoded_tests():
    return get_encoded_tokens()

@router.get("/api/test_encode_all")
def test_encode_all():
    """Ejecuta pruebas de encoding para todos los tokens guardados."""
    return test_encode_repository()