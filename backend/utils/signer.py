import hmac
import hashlib
import base64


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _make_signer(digestmod, secret: str):

    secret_bytes = secret.encode("utf-8")

    def _sign(unsigned_token: str) -> str:
        signature = hmac.new(
            secret_bytes,
            msg=unsigned_token.encode("utf-8"),
            digestmod=digestmod
        ).digest()
        return base64url_encode(signature)

    return _sign


def signer_hs256(secret: str):
    return _make_signer(hashlib.sha256, secret)


def signer_hs384(secret: str):
    return _make_signer(hashlib.sha384, secret)
