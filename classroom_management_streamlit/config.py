import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = st.secrets("MONGO_URI") or st.secrets("MONGODB_ATLAS_URI") or "mongodb://localhost:27017"
DB_NAME = st.secrets("DB_NAME") or st.secrets("DB_NAME", "classroom_management")
MONGO_SERVER_SELECTION_TIMEOUT_MS = int(st.secrets("MONGO_SERVER_SELECTION_TIMEOUT_MS", "5000"))

APP_TITLE = "Classroom Management System"
DEFAULT_SUBJECT_NAME = "Classroom Subject"
DEFAULT_TOTAL_LECTURES = 20
