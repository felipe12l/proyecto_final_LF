from enum import Enum

class TokenType(Enum):
    HEADER_TOKEN = "HEADER_TOKEN"
    PAYLOAD_TOKEN = "PAYLOAD_TOKEN"
    SIGNATURE_TOKEN = "SIGNATURE_TOKEN"

    L_BRACE = "L_BRACE"      
    R_BRACE = "R_BRACE"      
    STRING = "STRING"        
    COLON = "COLON"          
    COMMA = "COMMA"          
    BOOLEAN = "BOOLEAN"      
