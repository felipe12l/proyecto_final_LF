import os
from datetime import datetime
from typing import Any, Dict, Optional, List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi


MONGO_URI = os.getenv("MONGO_URI") or "mongodb://jwt-mongo:27017"
MONGO_DB = "JWT"
MONGO_TIMEOUT_MS = int(os.getenv("MONGO_TIMEOUT_MS", "10000"))

class DatabaseConnector:
    _client: Optional[MongoClient] = None
    _db = None
    def __init__(self):
        self._client=MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT_MS, server_api=ServerApi('1'))
    @classmethod
    def get_client(self) -> MongoClient:
        if self._client is None:
            self._client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT_MS)
            self._client.admin.command("ping")
        return self._client

    @classmethod
    def get_db(self):
        if self._db is None:
            client = self.get_client()
            self._db = client[MONGO_DB]
        return self._db

    @classmethod
    def get_collection(self, name: str) -> Collection:
        db = self.get_db()
        return db[name]

    @classmethod
    def init_indexes(self) -> None:
        """Crea índices útiles si aún no existen."""
        coll = self.get_collection("analyses")
        coll.create_index("created_at")
        coll.create_index("token")
    
    @classmethod
    def save_analysis(self, token: str, result: Dict[str, Any]) -> str:
        """Inserta un documento de análisis y retorna el id como string."""
        coll = self.get_collection("analyses")
        doc = {
            "token": token,
            "result": result,
            "created_at": datetime.now(),
        }
        res = coll.insert_one(doc)
        return str(res.inserted_id)

    @classmethod
    def find_analyses(self, filter_query: Dict[str, Any] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Consulta documentos en la colección `analyses`."""
        coll = self.get_collection("analyses")
        q = filter_query or {}
        cursor = coll.find(q).sort("created_at", -1).limit(limit)
        return list(cursor)

    @classmethod
    def clear_analyses(self) -> int:
        """Elimina todos los documentos en la colección `analyses` y retorna el conteo."""
        coll = self.get_collection("analyses")
        res = coll.delete_many({})
        return res.deleted_count
""" 
if __name__ == "__main__":
    try:
        print("Conectando a MongoDB en", MONGO_URI)
        DatabaseConnector.get_client()
        DatabaseConnector.init_indexes()
        sample_id = DatabaseConnector.save_analysis("prueba-token", {"status": "ok", "note": "ejemplo"})
        print("Inserción OK, id =", sample_id)
        
    except Exception as e:
        print("Error al conectar a MongoDB:", e)
 """