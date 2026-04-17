"""
MongoDB connection and collection accessors
"""

from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client: AsyncIOMotorClient = None


def get_client() -> AsyncIOMotorClient:
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.MONGODB_URI)
    return client


def get_db():
    return get_client()[settings.MONGODB_DB_NAME]


def get_sessions_collection():
    return get_db()["interview_sessions"]
