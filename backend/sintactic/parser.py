from lexer.tokens import TokenType

class SyntaxErrorException(Exception):
    pass


class SyntaxAnalyzer:
    
    def __init__(self, encoded_tokens, header_tokens, payload_tokens):
        self.encoded = encoded_tokens
        self.header = header_tokens
        self.payload = payload_tokens

    def checkEncoded(self):
        if len(self.encoded) != 3:
            raise SyntaxErrorException("El JWT codificado debe tener exactamente 3 secciones (G1).")

        h, p, s = self.encoded

        for token_type, segment in self.encoded:
            if not segment.isalnum() and "-" not in segment and "_" not in segment:
                raise SyntaxErrorException(f"Segmento no válido para γ* en G1: {segment}")


    def parseObject(self, tokens, name):

        i = 0
        length = len(tokens)

        if tokens[i][0] != TokenType.L_BRACE:
            raise SyntaxErrorException(f"JSON {name} debe iniciar con '{{' (G2).")
        i += 1

        if i < length and tokens[i][0] == TokenType.R_BRACE:
            return True

        expecting_key = True

        while i < length:
            tok_type, tok_val = tokens[i]

            if expecting_key:
                if tok_type != TokenType.STRING:
                    raise SyntaxErrorException(f"Se esperaba STRING como clave en {name} (G2).")
                i += 1

                if tokens[i][0] != TokenType.COLON:
                    raise SyntaxErrorException(f"Falta ':' después de clave en {name} (G2).")
                i += 1

                expecting_key = False
                continue

            tok_type, tok_val = tokens[i]

            if tok_type in (TokenType.STRING, TokenType.BOOLEAN):
                i += 1

            elif tok_val.isdigit():
                i += 1

            elif tok_type == TokenType.L_BRACE:
                brace_stack = 1
                j = i + 1
                while j < length and brace_stack > 0:
                    if tokens[j][0] == TokenType.L_BRACE:
                        brace_stack += 1
                    if tokens[j][0] == TokenType.R_BRACE:
                        brace_stack -= 1
                    j += 1
                i = j

            else:
                raise SyntaxErrorException(f"Valor no válido en {name}: {tok_val} (G2).")

            if i >= length:
                break

            if tokens[i][0] == TokenType.COMMA:
                i += 1
                expecting_key = True
                continue
            
            if tokens[i][0] == TokenType.R_BRACE:
                return True

            raise SyntaxErrorException(f"Error de estructura en JSON {name} (G2).")

        return True



    def analyze(self):
        self.checkEncoded()

        self.parseObject(self.header, "header")

        self.parseObject(self.payload, "payload")

        return True
