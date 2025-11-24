import os
from datetime import datetime
from typing import Any, Dict, Optional, List

from pymongo import MongoClient
from pymongo.collection import Collection


MONGO_URI = os.getenv("MONGO_URI") or "mongodb://jwt-mongo:27017"
MONGO_DB = "JWT"
MONGO_TIMEOUT_MS = int(os.getenv("MONGO_TIMEOUT_MS", "2000"))


_client: Optional[MongoClient] = None
_db = None

def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT_MS)
        
        _client.admin.command("ping")
    return _client

def get_db():
    global _db
    if _db is None:
        client = get_client()
        _db = client[MONGO_DB]
    return _db

def get_collection(name: str) -> Collection:
    db = get_db()
    return db[name]

def init_indexes() -> None:
    """Crea índices útiles si aún no existen."""
    coll = get_collection("analyses")
    
    coll.create_index("created_at")
    
    coll.create_index("token")
 

def save_analysis(token: str, result: Dict[str, Any]) -> str:
    """Inserta un documento de análisis y retorna el id como string."""
    coll = get_collection("analyses")
    doc = {
        "token": token,
        "result": result,
        "created_at": datetime.now(),
    }
    res = coll.insert_one(doc)
    return str(res.inserted_id)

def find_analyses(filter_query: Dict[str, Any] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Consulta documentos en la colección `analyses`."""
    coll = get_collection("analyses")
    q = filter_query or {}
    cursor = coll.find(q).sort("created_at", -1).limit(limit)
    return list(cursor)

def clear_analyses() -> int:
    """Elimina todos los documentos en la colección `analyses` y retorna el conteo."""
    coll = get_collection("analyses")
    res = coll.delete_many({})
    return res.deleted_count

if __name__ == "__main__":
    try:
        print("Conectando a MongoDB en", MONGO_URI)
        get_client()
        init_indexes()
        sample_id = save_analysis("prueba-token", {"status": "ok", "note": "ejemplo"})
        print("Inserción OK, id =", sample_id)
        print("Últimos documentos:", find_analyses(limit=5))
    except Exception as e:
        print("Error al conectar a MongoDB:", e)
