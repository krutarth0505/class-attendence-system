import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGODB_ATLAS_URI") or "mongodb://localhost:27017"
DB_NAME = os.getenv("DB_NAME", "classroom_management")
MONGO_SERVER_SELECTION_TIMEOUT_MS = int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", "5000"))

APP_TITLE = "Classroom Management System"
DEFAULT_SUBJECT_NAME = "Classroom Subject"
DEFAULT_TOTAL_LECTURES = 20
