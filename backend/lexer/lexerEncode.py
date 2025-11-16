import re
from .tokens import TokenType

class EncodedLexer:

    BASE64URL_REGEX = r'^[A-Za-z0-9\-_]+$' 

    def __init__(self, token_str: str):
        self.token_str = token_str.strip()
        self.tokens = []
    
    def tokenize(self):

        parts = self.token_str.split('.')

        if len(parts) != 3:
            raise ValueError("El JWT codificado debe tener exactamente 3 secciones separadas por '.'")

        header, payload, signature = parts

        self._validate_segment(header, TokenType.HEADER_TOKEN)
        self._validate_segment(payload, TokenType.PAYLOAD_TOKEN)
        self._validate_segment(signature, TokenType.SIGNATURE_TOKEN)

        return self.tokens

    def _validate_segment(self, segment: str, token_type):

        if not re.match(self.BASE64URL_REGEX, segment):
            raise ValueError(f"Segmento inválido según Σ₁: {segment}")

        self.tokens.append((token_type, segment))
