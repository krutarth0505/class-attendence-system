import os
import streamlit as st

try:
	from dotenv import load_dotenv
except ModuleNotFoundError:
	# Streamlit Cloud can run without python-dotenv when secrets are configured.
	def load_dotenv() -> bool:
		return False


load_dotenv()


def _secret_or_env(key: str, default: str | None = None) -> str | None:
	if key in st.secrets:
		return str(st.secrets[key])
	return os.getenv(key, default)


MONGO_URI = _secret_or_env("MONGO_URI") or _secret_or_env("MONGODB_ATLAS_URI") or "mongodb://localhost:27017"
DB_NAME = _secret_or_env("DB_NAME", "classroom_management") or "classroom_management"
MONGO_SERVER_SELECTION_TIMEOUT_MS = int(_secret_or_env("MONGO_SERVER_SELECTION_TIMEOUT_MS", "5000") or "5000")

APP_TITLE = "Classroom Management System"
DEFAULT_SUBJECT_NAME = "Classroom Subject"
DEFAULT_TOTAL_LECTURES = 20
