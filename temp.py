import requests

URL = "http://18.218.30.208:8000/api/analyze"

jwt_list = [
    # ====== 16 TOKENS VÁLIDOS (HS256 / HS384, secret = Furina) ======

    # HS256 válidos
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0IiwiaWF0IjoxNjAwMDAwMDAwfQ.r4QKrC5CJpVggQj2HxBx_QVzp2QrRb4iCuTNsabjQDQ",
    "eyJhbGciOiJIUzI1NiJ9.eyJhIjoxfQ.9S6AhbzpwA5-ovN9XExAEL0Y9J9a_8DlubzEPEq2PDE",
    "eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjQ3OTk5OTk5OTksIm5iZiI6MTYwMDAwMDAwMCwiaWF0IjoyfQ.GaObq1rgcLqa7lBlAQAtmcIuM1n2Fq5Ki2wLHBH0IWw",
    "eyJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6dHJ1ZX0._wHkqA0N2mVoD_vKvxrfiFGVuR6AFNB2pAvhODU1nEM",
    "eyJhbGciOiJIUzI1NiJ9.eyJtZXNzYWdlIjoiSGVsbG8ifQ.WnKbkZVgdItAAryrJycrhi0lzsmdcwQwjautaEefhAM",
    "eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjAwMDAwfQ.aNgJ2mVtK5-BpA3tGQQvCH3Ft46Tox8FNsUyLUleP7c",
    "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0In0.Ae4WSGr2Co5DdVASol20U2gVifAl6_7i2vkfovMhRp4",
    "eyJhbGciOiJIUzI1NiJ9.eyJodG1sIjoiYWNhYmFkb3JzIn0.XWT5OaUCDu5L2fHjuL2iJgqo-FFjndrfURm1EJAh8VE",

    # HS384 válidos
    "eyJhbGciOiJIUzM4NCJ9.eyJhIjoxfQ.0BaP_lmeZ_Fj0ArWgp0JH3nlOOAoE8keLJpLFt5fHt5Wt8VbZS3R3V7Rz6XjG1ne",
    "eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJqdyJ9.cR_tnzIBG7v8M1k_CnBLTYsQ5KuvRDz2H2zXy-sm7fOkhtGQKs0Ls6hV5eXl8v5t",
    "eyJhbGciOiJIUzM4NCJ9.eyJpYXQiOjE2MDAwMDAwMDB9.UQvQ530P2W-rlRZlvG0fTzH9d-1r0hfv1zBVjTt4K8I2pkQH6z7c9vZcH0t2EWkF",
    "eyJhbGciOiJIUzM4NCJ9.eyJlbnYiOiJwcm9kIn0.3W5P0YcKe86EgnNQVJShWcfaM8V3c0lK7EWpLtv69ZK3gKjSw4eqkE1uUgxLRqcX",
    "eyJhbGciOiJIUzM4NCJ9.eyJhZG1pbiI6dHJ1ZX0.PIFAZzk4h1xwQpVuN5VgyAgVFDa6dUiYr9S9gjdo0h1lvvkgqQ2Oub49l5qhZf1b",
    "eyJhbGciOiJIUzM4NCJ9.eyJub25jZSI6InRlc3QifQ.g8Bd309lm5cS4zJxjmwUa5dUwHWYm3uSHnv7lG0FNM8SxGixGcW8rNh0uxrIi9Pc",
    "eyJhbGciOiJIUzM4NCJ9.eyJuIjoxMjN9.MwguUtqGzMx0B1t4pWUV4cFUwYpJUiT5Iw85IhxQSLz1LFogGtEV3dSIHc0Fxsb0",
    "eyJhbGciOiJIUzM4NCJ9.eyJoZWxsbyI6IndvcmxkIn0.fTQ9z8cdy5Q1KEDmNQpU7N5wN_8ZD9l1ApW5MBjkeuF1vl0-k9QSN8pW8GjY0u8-",

    # ====== 16 TOKENS INVÁLIDOS ======

    # Algoritmo prohibido
    "eyJhbGciOiJub25lIn0.eyJpZCI6MX0.",  
    "eyJhbGciOiJSUzI1NiJ9.eyJpZCI6MX0.XYZXYZXYZ",

    # Firma incorrecta
    "eyJhbGciOiJIUzI1NiJ9.eyJ0ZXN0IjoiZmFpbGVkIn0.wrongWRONGwrongWRONG",
    "eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDAwMDAwMDB9.123",

    # Header inválido
    "e30.eyJpZCI6MX0.abc",
    "eyJhbGciIiOiJIUzI1NiJ9.eyJpZCI6MX0.signature",

    # Payload inválido
    "eyJhbGciOiJIUzI1NiJ9.e30=.signature",
    "eyJhbGciOiJIUzI1NiJ9.!!invalid!!.signature",

    # Token truncado
    "eyJhbGciOiJIUzI1NiJ9..signature",
    "abc.def",
    "abc",

    # Token con algoritmo correcto pero payload corrupto
    "eyJhbGciOiJIUzI1NiJ9.ZXJy.badsignature",
    "eyJhbGciOiJIUzI1NiJ9.e30.invalidinvalidinvalid",

    # Token expirado
    "eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjEwMH0.ZYco6ODr7yXjzfY1zVwL6nMaY3k0VJvSd-fdzHfbl8E",

    # Token con iat inválido
    "eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOiJub3QiOiBudW1iZXJ9.invalid",

    # Token con estructura rota
    ".....",
    "eyJhbGciOiJIUzI1NiJ9.e30",
    ".....broken.token.here....."
]


for i, token in enumerate(jwt_list, start=1):
    data = {"token": token}
    print(f"\n=== Enviando JWT #{i} ===")
    try:
        response = requests.post(URL, json=data)
        print("Status:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)
