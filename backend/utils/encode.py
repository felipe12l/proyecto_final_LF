import json
import base64

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

class JWTEncoder:

    def __init__(self, header_dict: dict, payload_dict: dict):
        self.header = header_dict
        self.payload = payload_dict

    def encode(self):
        header_json = json.dumps(self.header, separators=(",", ":")).encode()
        payload_json = json.dumps(self.payload, separators=(",", ":")).encode()

        header_b64 = base64url_encode(header_json)
        payload_b64 = base64url_encode(payload_json)

        return f"{header_b64}.{payload_b64}"
