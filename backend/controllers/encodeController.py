from utils.encode import JWTEncoder
from utils.signer import signer_hs256, signer_hs384
from utils.verify import verify_hs256, verify_hs384
from database.db import DatabaseConnector

def encode_jwt(data):
    header = data["header"]
    payload = data["payload"]
    secret = data["secret"]

    alg = header.get("alg")
    encoder = JWTEncoder(header, payload)

    unsigned = encoder.encode()

    if alg == "HS256":
        sign = signer_hs256(secret)
    elif alg == "HS384":
        sign = signer_hs384(secret)
    else:
        raise ValueError("Algoritmo no soportado")

    signature = sign(unsigned)

    jwt_final = f"{unsigned}.{signature}"

    return {"jwt": jwt_final}

def test_encode_jwt(header, payload, secret):
    """
    Versión de prueba que valida el encoding y verifica la firma.
    Retorna status, message y el token generado.
    """
    try:
        alg = header.get("alg")
        if not alg:
            return {
                "status": "error",
                "phase": "validation",
                "message": "Header no contiene algoritmo (alg)",
                "header": header,
                "payload": payload
            }
        
        if alg not in ["HS256", "HS384"]:
            return {
                "status": "error",
                "phase": "validation",
                "message": f"Algoritmo no soportado: {alg}",
                "header": header,
                "payload": payload
            }
        
        # Generar el token
        encoder = JWTEncoder(header, payload)
        unsigned = encoder.encode()
        
        if alg == "HS256":
            sign = signer_hs256(secret)
            verify = verify_hs256(secret)
        elif alg == "HS384":
            sign = signer_hs384(secret)
            verify = verify_hs384(secret)
        
        signature = sign(unsigned)
        jwt_final = f"{unsigned}.{signature}"
        
        # Verificar la firma generada
        is_valid = verify(unsigned, signature)
        
        if not is_valid:
            return {
                "status": "error",
                "phase": "verification",
                "message": "La firma generada no es válida",
                "jwt": jwt_final,
                "header": header,
                "payload": payload
            }
        
        return {
            "status": "ok",
            "message": "Token generado y verificado correctamente",
            "jwt": jwt_final,
            "header": header,
            "payload": payload,
            "algorithm": alg
        }
        
    except Exception as e:
        return {
            "status": "error",
            "phase": "encoding",
            "message": str(e),
            "header": header,
            "payload": payload
        }

def test_encode_list(test_cases):
    """
    Ejecuta pruebas de encoding para múltiples casos.
    test_cases: lista de dicts con {header, payload, secret}
    """
    results = []
    try:
        for test_case in test_cases:
            header = test_case.get("header", {})
            payload = test_case.get("payload", {})
            secret = test_case.get("secret", "")
            
            result = test_encode_jwt(header, payload, secret)
            results.append(result)
            
    except Exception as e:
        results.append({
            "status": "error",
            "phase": "test_encode_list",
            "message": str(e)
        })
    
    return results

def test_encode_repository():
    """
    Recupera todos los tokens del repositorio y ejecuta pruebas de encoding.
    Valida que cada token guardado se pueda regenerar correctamente.
    """
    try:
        db = DatabaseConnector()
        encoded_tokens = db.find_encoded_tokens(limit=1000)
        
        if not encoded_tokens:
            return {
                "status": "ok",
                "message": "No hay tokens en el repositorio para probar",
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 0
                },
                "results": []
            }
        
        # Preparar casos de prueba
        test_cases = []
        for token_doc in encoded_tokens:
            test_cases.append({
                "header": token_doc.get("header", {}),
                "payload": token_doc.get("payload", {}),
                "secret": token_doc.get("secret", ""),
                "original_jwt": token_doc.get("jwt", "")
            })
        
        # Ejecutar pruebas
        results = []
        passed_count = 0
        failed_count = 0
        
        for test_case in test_cases:
            result = test_encode_jwt(
                test_case["header"],
                test_case["payload"],
                test_case["secret"]
            )
            
            # Agregar el JWT original al resultado
            result["original_jwt"] = test_case["original_jwt"]
            
            # Comparar con el token original si existe
            if result["status"] == "ok" and test_case["original_jwt"]:
                if result["jwt"] == test_case["original_jwt"]:
                    result["match"] = True
                    result["message"] = "Token regenerado coincide con el original"
                else:
                    result["match"] = False
                    result["message"] = "Token regenerado NO coincide con el original"
            
            results.append(result)
            
            if result["status"] == "ok":
                passed_count += 1
            else:
                failed_count += 1
        
        return {
            "status": "ok",
            "summary": {
                "total": len(test_cases),
                "passed": passed_count,
                "failed": failed_count
            },
            "results": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "phase": "test_encode_repository",
            "message": str(e)
        }

def get_encoded_tokens():
    """Recupera todos los tokens encriptados del repositorio."""
    try:
        db = DatabaseConnector()
        tokens = db.find_encoded_tokens(limit=1000)
        
        if not tokens:
            return {
                "status": "ok",
                "message": "No hay tokens encriptados en el repositorio",
                "results": []
            }
        
        # Formatear los resultados
        results = []
        for token_doc in tokens:
            results.append({
                "header": token_doc.get("header"),
                "payload": token_doc.get("payload"),
                "jwt": token_doc.get("jwt"),
                "created_at": token_doc.get("created_at")
            })
        
        return {
            "status": "ok",
            "total": len(results),
            "results": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
