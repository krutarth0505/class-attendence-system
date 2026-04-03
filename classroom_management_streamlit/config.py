import os
from urllib.parse import quote_plus
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

try:
	from dotenv import load_dotenv
except ModuleNotFoundError:
	# Streamlit Cloud can run without python-dotenv when secrets are configured.
	def load_dotenv() -> bool:
		return False


load_dotenv()


def _secret_or_env(key: str, default: str | None = None) -> str | None:
	try:
		if key in st.secrets:
			return str(st.secrets[key])
	except StreamlitSecretNotFoundError:
		pass
	return os.getenv(key, default)


def _atlas_uri_from_parts() -> str | None:
	username = _secret_or_env("MONGODB_USERNAME")
	password = _secret_or_env("MONGODB_PASSWORD")
	host = _secret_or_env("MONGODB_HOST")
	db_name = _secret_or_env("MONGODB_DB_NAME")

	if not (username and password and host):
		return None

	auth_db = db_name or ""
	if auth_db:
		auth_db = f"/{auth_db}"

	encoded_password = quote_plus(password)
	return f"mongodb+srv://{username}:{encoded_password}@{host}{auth_db}?retryWrites=true&w=majority&appName=Cluster0"


MONGO_URI = _secret_or_env("MONGO_URI") or _secret_or_env("MONGODB_ATLAS_URI") or _atlas_uri_from_parts() or "mongodb://localhost:27017"
DB_NAME = _secret_or_env("DB_NAME", "classroom_management") or "classroom_management"
MONGO_SERVER_SELECTION_TIMEOUT_MS = int(_secret_or_env("MONGO_SERVER_SELECTION_TIMEOUT_MS", "15000") or "15000")

APP_TITLE = "Classroom Management System"
DEFAULT_SUBJECT_NAME = "Classroom Subject"
DEFAULT_TOTAL_LECTURES = 20
