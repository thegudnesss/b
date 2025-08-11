"""
Advanced MongoDB Manager
========================
DRY, dynamic, moslashuvchan va avtomatlashtirilgan MongoDB ishlash tizimi.
"""

from __future__ import annotations
from typing import Optional, Type, TypeVar, Generic

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import BaseModel
from src import config, log

T = TypeVar("T", bound=BaseModel)


class MongoManager:
    """Asosiy MongoDB boshqaruv classi."""

    def __init__(self, url: str, db_name: str) -> None:
        self._url = url
        self._db_name = db_name
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None

    async def connect(self) -> None:
        """MongoDB bilan ulanish."""
        self._client = AsyncIOMotorClient(self._url)
        self._db = self._client[self._db_name]
        log.info("✅ MongoDB ulanish o‘rnatildi", db=self._db_name)

    async def disconnect(self) -> None:
        """Ulanishni yopish."""
        if self._client:
            self._client.close()
            log.info("⛔ MongoDB ulanish yopildi")

    def collection(self, name: str) -> AsyncIOMotorCollection:
        """Collection obyektini olish."""
        if not self._db:
            raise RuntimeError("❌ MongoDB ulanmagan!")
        return self._db[name]


class BaseRepository(Generic[T]):
    """
    Har bir collection uchun asosiy CRUD funksiyalar.
    DRY va avtomatlashtirilgan ishlash uchun.
    """

    collection_name: str
    model: Type[T]

    def __init__(self, db: MongoManager) -> None:
        self.db = db

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.db.collection(self.collection_name)

    async def get(self, filter_: dict) -> Optional[T]:
        data = await self.collection.find_one(filter_)
        return self.model(**data) if data else None

    async def create(self, data: T) -> str:
        result = await self.collection.insert_one(data.model_dump())
        return str(result.inserted_id)

    async def update(self, filter_: dict, update_data: dict) -> int:
        result = await self.collection.update_one(filter_, {"$set": update_data})
        return result.modified_count

    async def delete(self, filter_: dict) -> int:
        result = await self.collection.delete_one(filter_)
        return result.deleted_count


# Global Mongo obyekt
mongo = MongoManager(url=config.mongo_uri, db_name=config.mongo_db_name)
