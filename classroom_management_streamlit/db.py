from pymongo import MongoClient
from pymongo.errors import PyMongoError
import streamlit as st

from config import DB_NAME, MONGO_SERVER_SELECTION_TIMEOUT_MS, MONGO_URI


@st.cache_resource
def get_client() -> MongoClient:
    """Create and cache one MongoDB client for the app session."""
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_SERVER_SELECTION_TIMEOUT_MS)
    try:
        client.admin.command("ping")
    except PyMongoError as exc:
        raise RuntimeError(
            "Unable to connect to MongoDB. Check MONGO_URI/MONGODB_ATLAS_URI, DB_NAME, and Atlas network access."
        ) from exc
    return client


@st.cache_resource
def get_db():
    """Return database object."""
    return get_client()[DB_NAME]


def users_collection():
    return get_db()["users"]


def settings_collection():
    return get_db()["settings"]


def attendance_collection():
    return get_db()["attendance"]


def ensure_indexes() -> None:
    """Create indexes used by the app for faster and safer lookups."""
    users_collection().create_index("username", unique=True)
    settings_collection().create_index("key", unique=True)
    attendance_collection().create_index("lectureNo", unique=True)
