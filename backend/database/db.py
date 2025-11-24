import os
import certifi
from datetime import datetime
from typing import Any, Dict, Optional, List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi

MONGO_URI = MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = "JWT"
MONGO_TIMEOUT_MS = int(os.getenv("MONGO_TIMEOUT_MS", "30000"))

class DatabaseConnector:
    _client: Optional[MongoClient] = None
    _db = None
    
    def __init__(self):
        self._client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=MONGO_TIMEOUT_MS,
            server_api=ServerApi('1')
        )
    
    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._client is None:
            cls._client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=MONGO_TIMEOUT_MS,
                tlsCAFile=certifi.where(),
                server_api=ServerApi('1')
            )
            cls._client.admin.command("ping")
        return cls._client

    @classmethod
    def get_db(cls):
        if cls._db is None:
            client = cls.get_client()
            cls._db = client[MONGO_DB]
        return cls._db

    @classmethod
    def get_collection(cls, name: str) -> Collection:
        db = cls.get_db()
        return db[name]

    @classmethod
    def init_indexes(cls) -> None:
        """Crea índices útiles si aún no existen."""
        coll = cls.get_collection("analyses")
        coll.create_index("created_at")
        coll.create_index("token")
    
    @classmethod
    def save_analysis(cls, token: str, result: Dict[str, Any]) -> str:
        """Inserta un documento de análisis y retorna el id como string."""
        coll = cls.get_collection("analyses")
        doc = {
            "token": token,
            "result": result,
            "created_at": datetime.now(),
        }
        res = coll.insert_one(doc)
        return str(res.inserted_id)

    @classmethod
    def find_analyses(cls, filter_query: Dict[str, Any] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Consulta documentos en la colección `analyses`."""
        coll = cls.get_collection("analyses")
        q = filter_query or {}
        cursor = coll.find(q).sort("created_at", -1).limit(limit)
        return list(cursor)

    @classmethod
    def clear_analyses(cls) -> int:
        """Elimina todos los documentos en la colección `analyses` y retorna el conteo."""
        coll = cls.get_collection("analyses")
        res = coll.delete_many({})
        return res.deleted_count
    
    @classmethod
    def save_encoded_token(cls, request_data: Dict[str, Any], jwt_result: Dict[str, Any]) -> str:
        """Inserta un documento de token encriptado y retorna el id como string."""
        coll = cls.get_collection("encoded_tokens")
        doc = {
            "header": request_data.get("header"),
            "payload": request_data.get("payload"),
            "secret": request_data.get("secret"),
            "jwt": jwt_result.get("jwt"),
            "created_at": datetime.now(),
        }
        res = coll.insert_one(doc)
        return str(res.inserted_id)
    
    @classmethod
    def find_encoded_tokens(cls, filter_query: Dict[str, Any] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Consulta documentos en la colección `encoded_tokens`."""
        coll = cls.get_collection("encoded_tokens")
        q = filter_query or {}
        cursor = coll.find(q).sort("created_at", -1).limit(limit)
        return list(cursor)
    
    @classmethod
    def clear_encoded_tokens(cls) -> int:
        """Elimina todos los documentos en la colección `encoded_tokens` y retorna el conteo."""
        coll = cls.get_collection("encoded_tokens")
        res = coll.delete_many({})
        return res.deleted_count
