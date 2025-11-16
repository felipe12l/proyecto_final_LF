from utils.decode import JWTDecoder
from lexer.lexerEncode import EncodedLexer
from lexer.lexerDecode import LexerDecoded

def test(token):
    print("encoded")
    try:
        lex =EncodedLexer(token)
        encodedToken = lex.tokenize()
        print("encoded ok 🐭")
    except Exception as e:
        print("error encoded")
        return
    
    print("decoded")
    
    try:
        decoded = JWTDecoder(token)
        decodedToken = decoded.decode()
        print("decoded ok 🐭")
    except:
        print("error decoded")
        return
    

    header_json = decodedToken["header_json"]
    payload_json = decodedToken["payload_json"]
    signature = decodedToken["signature_b64"]

    print("\n   HEADER JSON:")
    print("   ", header_json)
    print("\n   PAYLOAD JSON:")
    print("   ", payload_json)
    print("\n   SIGNATURE:")
    print("   ", signature)

    try:
        lex_h = LexerDecoded(header_json)
        header_tokens = lex_h.analyze()
        print("   ✔ Lexico header OK")
    except Exception as e:
        print(f"   ❌ Error léxico en el header JSON: {e}")
        return

    try:
        lex_p = LexerDecoded(payload_json)
        payload_tokens = lex_p.analyze()
        print("   ✔ Lexico payload OK")
    except Exception as e:
        print(f"   ❌ Error léxico en el payload JSON: {e}")
        return
    
    print("\n========== 🎉 PRUEBA COMPLETADA CON ÉXITO ==========")
    print("\nTokens generados:")
    print("Header tokens:", header_tokens)
    print("Payload tokens:", payload_tokens)
    print("Codificado tokens:", encodedToken)

if __name__ == "__main__":
    # Token de prueba clásico, válido
    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
        "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    )

    test(token)


