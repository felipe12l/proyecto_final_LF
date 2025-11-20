import hmac
import hashlib
import base64

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

class JWTSigner:

    def __init__(self, algorithm: str, secret_key: str):
        self.alg = algorithm
        self.secret = secret_key.encode()

    def sign(self, token_unsigned: str) -> str:
        if self.alg == "HS256":
            signature = hmac.new(
                self.secret,
                msg=token_unsigned.encode(),
                digestmod=hashlib.sha256
            ).digest()
            return base64url_encode(signature)

        elif self.alg == "RS256":
            raise NotImplementedError("RS256 no implementado en este proyecto")

        elif self.alg == "ES256":
            raise NotImplementedError("ES256 no implementado en este proyecto")

        else:
            raise ValueError("Algoritmo no soportado")
