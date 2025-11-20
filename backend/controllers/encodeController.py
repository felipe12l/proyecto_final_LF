from utils.encode import JWTEncoder
from utils.signer import signer_hs256, signer_hs384

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
