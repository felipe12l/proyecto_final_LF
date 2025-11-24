from .tokens import TokenType

class LexerDecoded:

    ALPHABET = set(
        list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        + ['{', '}', ':', ',', '"', ' ','-', '_' ]
    )

    def __init__(self, json_text: str):
        self.json = json_text
        self.tokens = []
        self.i = 0

    def verify_alphabet(self):
        for ch in self.json:
            if ch not in self.ALPHABET:
                raise ValueError(f"Error léxico (decodificado): carácter '{ch}' fuera de Σ₂")

    def tokenize(self):
        text = self.json
        length = len(text)

        while self.i < length:
            ch = text[self.i]

            if ch.isspace():
                self.i += 1
                continue

            if ch == '{':
                self.tokens.append((TokenType.L_BRACE, ch))
                self.i += 1
                continue

            if ch == '}':
                self.tokens.append((TokenType.R_BRACE, ch))
                self.i += 1
                continue

            if ch == ',':
                self.tokens.append((TokenType.COMMA, ch))
                self.i += 1
                continue

            if ch == ':':
                self.tokens.append((TokenType.COLON, ch))
                self.i += 1
                continue

            if ch == '"':
                self.i += 1
                start = self.i

                while self.i < length and text[self.i] != '"':
                    if not (text[self.i].isalnum() or text[self.i] == " "):
                        raise ValueError(
                            "STRING inválido: solo letras, números y espacios permitidos según el AFD"
                        )
                    self.i += 1

                value = text[start:self.i]
                self.tokens.append((TokenType.STRING, value))
                self.i += 1
                continue

            if text.startswith("true", self.i):
                self.tokens.append((TokenType.BOOLEAN, "true"))
                self.i += 4
                continue

            if text.startswith("false", self.i):
                self.tokens.append((TokenType.BOOLEAN, "false"))
                self.i += 5
                continue

            if ch.isalnum():
                start = self.i
                while self.i < length and text[self.i].isalnum():
                    self.i += 1
                value = text[start:self.i]
                self.tokens.append((TokenType.STRING, value))
                continue

            raise ValueError(
                f"Caracter inesperado: '{ch}' en posición {self.i}"
            )

        return self.tokens

    def analyze(self):
        self.verify_alphabet()
        return self.tokenize()
