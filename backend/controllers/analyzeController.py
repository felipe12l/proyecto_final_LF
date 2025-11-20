import json

from utils.decode import JWTDecoder
from lexer.lexerEncode import EncodedLexer
from lexer.lexerDecode import LexerDecoded
from semantic.semantic import SemanticAnalyzer

def analyzeJWT(token):
    lex =EncodedLexer(token)
    encodedToken = lex.tokenize()
    
    
    decoded = JWTDecoder(token)
    decodedToken = decoded.decode()

    header_json = decodedToken["header_json"]
    payload_json = decodedToken["payload_json"]
    signature = decodedToken["signature_b64"]

    header_tokens = LexerDecoded(header_json).analyze()
    payload_tokens = LexerDecoded(payload_json).analyze()

    header_dict = json.loads(header_json)
    payload_dict = json.loads(payload_json)

    sem = SemanticAnalyzer(header_dict, payload_dict, signature)
    sem.analyze()

    return {
        "status": "ok",
        "header": header_dict,
        "payload": payload_dict,
        "signature": signature,
        "tokens": {
            "encoded": encodedToken,
            "header": header_tokens,
            "payload": payload_tokens
        }
    }