import time

class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    
    REQUIRED_HEADER = {"alg", "typ"}

    VALID_ALG = {"HS256", "RS256", "ES256"}

    RESERVED_CLAIMS = {
        "iss", "sub", "aud", "exp", "nbf", "iat", "jti"
    }


    def __init__(self, header: dict, payload: dict, signature: str):
        self.header = header
        self.payload = payload
        self.signature = signature
        self.symbol_table = {}

    def analyze(self):
        self.checkHeaderRequiredFields()
        self.checkHeaderTyp()
        self.checkHeaderAlg()
        self.checkSignatureRequired()

        self.checkClaimTypes()
        self.checkTimeConsistency()
        self.checkMissingOrDuplicateClaims()

        return True

    def checkHeaderRequiredFields(self):
        if not self.REQUIRED_HEADER.issubset(self.header.keys()):
            raise SemanticError("E1: El header no contiene los campos obligatorios: alg y typ")


    def checkHeaderTyp(self):
        if self.header.get("typ") != "JWT":
            raise SemanticError("E2: El campo 'typ' debe ser 'JWT'")


    def checkHeaderAlg(self):
        alg = self.header.get("alg")
        if alg not in self.VALID_ALG:
            raise SemanticError(
                f"E3: Algoritmo no reconocido '{alg}'. Debe ser uno de {self.VALID_ALG}"
            )


    def checkSignatureRequired(self):
        if self.signature is None or self.signature.strip() == "":
            raise SemanticError("E7: El token no contiene firma aun cuando 'alg' lo exige")


    def checkClaimTypes(self):

        for key, value in self.payload.items():

            if key in {"iss", "sub", "aud", "jti"}:
                if not isinstance(value, str):
                    raise SemanticError(f"E4/E5: Claim '{key}' debe ser string")

            if key in {"exp", "nbf", "iat"}:
                if not isinstance(value, int):
                    raise SemanticError(f"E4/E5: Claim '{key}' debe ser entero")

            if value is None or value == "":
                raise SemanticError(f"E6: Claim '{key}' no puede ser vacío")


    def checkTimeConsistency(self):

        exp = self.payload.get("exp")
        nbf = self.payload.get("nbf")
        iat = self.payload.get("iat")

        if exp is None or nbf is None or iat is None:
            return

        if not (nbf <= iat <= exp):
            raise SemanticError("E6: El orden temporal debe cumplir: nbf ≤ iat ≤ exp")

        now = int(time.time())

        if exp < now:
            raise SemanticError("E4: El token está expirado")

        if nbf > now:
            raise SemanticError("E5: El token aún no es válido")


    def checkMissingOrDuplicateClaims(self):

        symbol_table = {}

        for key, value in self.payload.items():

            if key not in symbol_table:
                symbol_table[key] = type(value)
                continue

            if type(value) != symbol_table[key]:
                raise SemanticError(
                    f"E6: Claim '{key}' tiene tipos inconsistentes dentro del payload"
                )

        self.symbol_table = symbol_table
