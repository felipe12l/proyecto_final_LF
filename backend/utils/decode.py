import base64
import json

class JWTDecoder:

    def __init__(self, token: str):
        self.token = token.strip()
        self.header_b64 = ""
        self.payload_b64 = ""
        self.signature_b64 = ""
        self.header_json = ""
        self.payload_json = ""
        self.header_obj = {}
        self.payload_obj = {}

    def split(self):
        parts = self.token.split(".")
        if len(parts) != 3:
            raise ValueError("El JWT debe tener exactamente 3 partes: header.payload.signature")
        self.header_b64, self.payload_b64, self.signature_b64 = parts

    def decode_segment(self, segment: str) -> str:
        try:
            padded = segment + "=" * (-len(segment) % 4)
            return base64.urlsafe_b64decode(padded).decode("utf-8")
        except Exception:
            raise ValueError(f"No se pudo decodificar el segmento Base64URL: {segment}")

    def decode(self):
        self.split()

        self.header_json = self.decode_segment(self.header_b64)
        self.payload_json = self.decode_segment(self.payload_b64)

        return {
            "header_json": self.header_json,
            "payload_json": self.payload_json,
            "signature_b64": self.signature_b64
        }

    def parse_json(self):
        try:
            self.header_obj = json.loads(self.header_json)
        except Exception:
            raise ValueError("El header JSON NO es válido.")

        try:
            self.payload_obj = json.loads(self.payload_json)
        except Exception:
            raise ValueError("El payload JSON NO es válido.")

        return {
            "header": self.header_obj,
            "payload": self.payload_obj
        }
