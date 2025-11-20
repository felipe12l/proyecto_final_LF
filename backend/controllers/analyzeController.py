import json

from utils.decode import JWTDecoder
from lexer.lexerEncode import EncodedLexer
from lexer.lexerDecode import LexerDecoded
from sintactic.parser import SyntaxAnalyzer
from semantic.semantic import SemanticAnalyzer

def analyzeJWT(token):

    try:
        lex =EncodedLexer(token)
        encodedToken = lex.tokenize()
    except Exception as e:
        return {
            "status": "error",
            "phase": "lexico-codificado",
            "message": str(e)
        }
    
    try:
        decoded = JWTDecoder(token)
        decodedToken = decoded.decode()
    except Exception as e:
        return{
            "status": "error",
            "phase": "decode",
            "message": str(e)
        }

    header_json = decodedToken["header_json"]
    payload_json = decodedToken["payload_json"]
    signature = decodedToken["signature_b64"]


    try:
        header_tokens = LexerDecoded(header_json).analyze()
    except Exception as e:
        return{
            "status": "error",
            "phase": "lexico-header",
            "message": str(e)
        }
    
    try:
        payload_tokens = LexerDecoded(payload_json).analyze()
    except Exception as e:
        return{
            "status": "error",
            "phase": "lexico-payload",
            "message": str(e)
        }
    

    try:
        parser = SyntaxAnalyzer(
            encoded_tokens=encodedToken,
            header_tokens=header_tokens,
            payload_tokens=payload_tokens
        )
        parser.analyze() 
    except Exception as e:
        return{
            "status": "error",
            "phase": "sintactico",
            "message": str(e)
        }

    try:
        header_dict = json.loads(header_json)
        payload_dict = json.loads(payload_json)
    except Exception as e:
        return{
            "status": "error",
            "phase": "json-parser",
            "message": str(e)
        }
    

    try:
        sem = SemanticAnalyzer(header_dict, payload_dict, signature)
        sem.analyze()
    except Exception as e:
        return{
            "status": "error",
            "phase": "semantic",
            "message": str(e)
        }
    

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