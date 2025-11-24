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

        encoder = JWTEncoder(header, payload)
        unsigned = encoder.encode()

        if alg == "HS256":
            sign = signer_hs256(secret)
            verify = verify_hs256(secret)
        else:
            sign = signer_hs384(secret)
            verify = verify_hs384(secret)

        signature = sign(unsigned)
        jwt_final = f"{unsigned}.{signature}"

        if not verify(unsigned, signature):
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
    results = []
    try:
        for t in test_cases:
            result = test_encode_jwt(
                t.get("header", {}),
                t.get("payload", {}),
                t.get("secret", "")
            )
            results.append(result)

    except Exception as e:
        results.append({
            "status": "error",
            "phase": "test_encode_list",
            "message": str(e)
        })

    return results

def test_encode_repository():
    try:
        encoded_tokens = DatabaseConnector.find_encoded_tokens(limit=1000)

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

        test_cases = []
        for token_doc in encoded_tokens:
            test_cases.append({
                "header": token_doc.get("header", {}),
                "payload": token_doc.get("payload", {}),
                "secret": token_doc.get("secret", ""),
                "original_jwt": token_doc.get("jwt", "")
            })

        results = []
        passed = 0
        failed = 0

        for case in test_cases:
            result = test_encode_jwt(
                case["header"],
                case["payload"],
                case["secret"]
            )
            result["original_jwt"] = case["original_jwt"]

            if result["status"] == "ok":
                if result["jwt"] == case["original_jwt"]:
                    result["match"] = True
                    result["message"] = "Token regenerado coincide con el original"
                else:
                    result["match"] = False
                    result["message"] = "Token regenerado NO coincide con el original"
                passed += 1
            else:
                failed += 1

            results.append(result)

        return {
            "status": "ok",
            "summary": {
                "total": len(results),
                "passed": passed,
                "failed": failed
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
    try:
        tokens = DatabaseConnector.find_analyses(limit=1000)

        if not tokens:
            return {
                "status": "ok",
                "message": "No hay tokens encriptados en el repositorio",
                "results": []
            }

        results = []
        for t in tokens:
            results.append({
                "header": t.get("header"),
                "payload": t.get("payload"),
                "jwt": t.get("jwt"),
                "created_at": t.get("created_at")
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
