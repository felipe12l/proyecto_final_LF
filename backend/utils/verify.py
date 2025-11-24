import hmac
import hashlib
import base64

def verify_hs256(secret: str):
    """
    Retorna una función que verifica firmas HMAC-SHA256.
    """
    def verify(unsigned_token: str, signature_b64: str) -> bool:
        try:
            # Calcular la firma esperada
            h = hmac.new(
                secret.encode('utf-8'),
                unsigned_token.encode('utf-8'),
                hashlib.sha256
            )
            expected_signature = base64.urlsafe_b64encode(h.digest()).decode('utf-8').rstrip('=')
            
            # Comparar con la firma proporcionada
            return hmac.compare_digest(expected_signature, signature_b64)
        except Exception:
            return False
    
    return verify

def verify_hs384(secret: str):
    """
    Retorna una función que verifica firmas HMAC-SHA384.
    """
    def verify(unsigned_token: str, signature_b64: str) -> bool:
        try:
            # Calcular la firma esperada
            h = hmac.new(
                secret.encode('utf-8'),
                unsigned_token.encode('utf-8'),
                hashlib.sha384
            )
            expected_signature = base64.urlsafe_b64encode(h.digest()).decode('utf-8').rstrip('=')
            
            # Comparar con la firma proporcionada
            return hmac.compare_digest(expected_signature, signature_b64)
        except Exception:
            return False
    
    return verify
