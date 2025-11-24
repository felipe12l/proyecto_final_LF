import json

from utils.decode import JWTDecoder
from lexer.lexerEncode import EncodedLexer
from lexer.lexerDecode import LexerDecoded
from sintactic.parser import SyntaxAnalyzer
from semantic.semantic import SemanticAnalyzer
from database.db import DatabaseConnector

def analyzeJWT_summary(token):
    """Versión simplificada que solo retorna status, phase y message sin detalles."""
    try:
        lex = EncodedLexer(token)
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
        return {
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
        return {
            "status": "error",
            "phase": "lexico-header",
            "message": str(e)
        }
    
    try:
        payload_tokens = LexerDecoded(payload_json).analyze()
    except Exception as e:
        return {
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
        return {
            "status": "error",
            "phase": "sintactico",
            "message": str(e)
        }

    try:
        header_dict = json.loads(header_json)
        payload_dict = json.loads(payload_json)
    except Exception as e:
        return {
            "status": "error",
            "phase": "json-parser",
            "message": str(e)
        }

    try:
        sem = SemanticAnalyzer(header_dict, payload_dict, signature)
        sem.analyze()
    except Exception as e:
        return {
            "status": "error",
            "phase": "semantic",
            "message": str(e)
        }

    return {
        "status": "ok",
        "message": "Token válido"
    }

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
def analyze_list(tokens):
    results = []
    try:
        for token in tokens:
            result = analyzeJWT(token)
            # Agregar el token al resultado para poder mostrarlo en la tabla
            result["token"] = token
            results.append(result)
    except Exception as e:
        results.append({
            "status": "error",
            "phase": "analyze_list",
            "message": str(e)
        })
    return results
def analyze_repository():
    """
    Recupera todos los tokens del repositorio (MongoDB) y los analiza en lote.
    Retorna una lista con los resultados de cada token.
    """
    try:
        # Recuperar todos los análisis guardados
        analyses = DatabaseConnector.find_analyses({}, 1000)
        
        # Extraer los tokens
        tokens = [analysis["token"] for analysis in analyses if "token" in analysis]
        
        if not tokens:
            return {
                "status": "ok",
                "message": "No hay tokens en el repositorio",
                "results": []
            }
        
        # Analizar todos los tokens
        results = analyze_list(tokens)
        
        return {
            "status": "ok",
            "total": len(tokens),
            "results": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "phase": "analyze_repository",
            "message": str(e)
        }

def analyze_repository_summary():
    """Analiza todos los tokens del repositorio sin detalles, solo status."""
    try:
        analyses = DatabaseConnector.find_analyses({}, 1000)
        tokens = [analysis["token"] for analysis in analyses if "token" in analysis]
        
        if not tokens:
            return {
                "status": "ok",
                "message": "No hay tokens en el repositorio",
                "summary": {
                    "total": 0,
                    "valid": 0,
                    "invalid": 0
                },
                "results": []
            }
        
        results = []
        valid_count = 0
        invalid_count = 0
        
        for token in tokens:
            result = analyzeJWT_summary(token)
            result["token"] = token
            results.append(result)
            
            if result["status"] == "ok":
                valid_count += 1
            else:
                invalid_count += 1
        
        return {
            "status": "ok",
            "summary": {
                "total": len(tokens),
                "valid": valid_count,
                "invalid": invalid_count
            },
            "results": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "phase": "analyze_repository_summary",
            "message": str(e)
        }
    