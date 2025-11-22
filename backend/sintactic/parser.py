from lexer.tokens import TokenType

class SyntaxErrorException(Exception):
    pass


class SyntaxAnalyzer:
    
    def __init__(self, encoded_tokens, header_tokens, payload_tokens):
        self.encoded = encoded_tokens
        self.header = header_tokens
        self.payload = payload_tokens
        self.derivation_tree = {
            "type": "JWT",
            "rule": "JWT → header.payload.signature (G1)",
            "children": []
        }

    def checkEncoded(self):
        if len(self.encoded) != 3:
            raise SyntaxErrorException("El JWT codificado debe tener exactamente 3 secciones (G1).")

        h, p, s = self.encoded

        # Construir nodos del árbol para cada segmento
        encoded_nodes = []
        segment_names = ["header", "payload", "signature"]
        
        for idx, (token_type, segment) in enumerate(self.encoded):
            if not segment.isalnum() and "-" not in segment and "_" not in segment:
                raise SyntaxErrorException(f"Segmento no válido para γ* en G1: {segment}")
            
            encoded_nodes.append({
                "type": segment_names[idx],
                "rule": f"{segment_names[idx]} → γ* (G1)",
                "value": segment,
                "characters": list(segment)
            })
        
        self.derivation_tree["children"].extend(encoded_nodes)


    def parseObject(self, tokens, name):
        tree_node = {
            "type": f"JSON_{name}",
            "rule": f"JSON → {{ pairs }} (G2)",
            "children": []
        }

        i = 0
        length = len(tokens)

        if tokens[i][0] != TokenType.L_BRACE:
            raise SyntaxErrorException(f"JSON {name} debe iniciar con '{{' (G2).")
        
        tree_node["children"].append({
            "type": "L_BRACE",
            "value": "{",
            "rule": "terminal"
        })
        i += 1

        if i < length and tokens[i][0] == TokenType.R_BRACE:
            tree_node["children"].append({
                "type": "R_BRACE",
                "value": "}",
                "rule": "terminal"
            })
            return tree_node

        expecting_key = True
        pair_count = 0

        while i < length:
            tok_type, tok_val = tokens[i]

            if expecting_key:
                if tok_type != TokenType.STRING:
                    raise SyntaxErrorException(f"Se esperaba STRING como clave en {name} (G2).")
                
                pair_node = {
                    "type": "key_value_pair",
                    "rule": "pair → string : value (G2)",
                    "children": []
                }
                
                pair_node["children"].append({
                    "type": "STRING",
                    "value": tok_val,
                    "rule": "key → string"
                })
                i += 1

                if tokens[i][0] != TokenType.COLON:
                    raise SyntaxErrorException(f"Falta ':' después de clave en {name} (G2).")
                
                pair_node["children"].append({
                    "type": "COLON",
                    "value": ":",
                    "rule": "terminal"
                })
                i += 1

                expecting_key = False
                continue

            tok_type, tok_val = tokens[i]
            value_node = None

            if tok_type in (TokenType.STRING, TokenType.BOOLEAN):
                value_node = {
                    "type": tok_type.name,
                    "value": tok_val,
                    "rule": f"value → {tok_type.name.lower()}"
                }
                i += 1

            elif tok_val.isdigit():
                value_node = {
                    "type": "NUMBER",
                    "value": tok_val,
                    "rule": "value → number"
                }
                i += 1

            elif tok_type == TokenType.L_BRACE:
                brace_stack = 1
                j = i + 1
                obj_tokens = [tokens[i]]
                while j < length and brace_stack > 0:
                    obj_tokens.append(tokens[j])
                    if tokens[j][0] == TokenType.L_BRACE:
                        brace_stack += 1
                    if tokens[j][0] == TokenType.R_BRACE:
                        brace_stack -= 1
                    j += 1
                value_node = {
                    "type": "OBJECT",
                    "value": "nested object",
                    "rule": "value → object"
                }
                i = j

            else:
                raise SyntaxErrorException(f"Valor no válido en {name}: {tok_val} (G2).")
            
            if value_node:
                pair_node["children"].append(value_node)
                tree_node["children"].append(pair_node)
                pair_count += 1

            if i >= length:
                break

            if tokens[i][0] == TokenType.COMMA:
                tree_node["children"].append({
                    "type": "COMMA",
                    "value": ",",
                    "rule": "terminal"
                })
                i += 1
                expecting_key = True
                continue
            
            if tokens[i][0] == TokenType.R_BRACE:
                tree_node["children"].append({
                    "type": "R_BRACE",
                    "value": "}",
                    "rule": "terminal"
                })
                return tree_node

            raise SyntaxErrorException(f"Error de estructura en JSON {name} (G2).")

        return tree_node



    def analyze(self):
        self.checkEncoded()

        header_tree = self.parseObject(self.header, "header")
        self.derivation_tree["decoded_header"] = header_tree

        payload_tree = self.parseObject(self.payload, "payload")
        self.derivation_tree["decoded_payload"] = payload_tree

        return True
    
    def get_derivation_tree(self):
        """Retorna el árbol de derivaciones completo"""
        return self.derivation_tree
