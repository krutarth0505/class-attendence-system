from datetime import datetime

from config import DEFAULT_SUBJECT_NAME, DEFAULT_TOTAL_LECTURES
from db import attendance_collection, ensure_indexes, settings_collection, users_collection


def seed_users() -> None:
    fixed_users = [
        {
            "username": "admin",
            "password": "admin123",
            "role": "admin",
            "name": "College Admin",
        },
        {
            "username": "teacher",
            "password": "teacher123",
            "role": "teacher",
            "name": "Teacher",
        },
        {
            "username": "student1",
            "password": "student123",
            "role": "student",
            "name": "Student 1",
            "rollNo": 101,
        },
        {
            "username": "student2",
            "password": "student123",
            "role": "student",
            "name": "Student 2",
            "rollNo": 102,
        },
        {
            "username": "student3",
            "password": "student123",
            "role": "student",
            "name": "Student 3",
            "rollNo": 103,
        },
        {
            "username": "student4",
            "password": "student123",
            "role": "student",
            "name": "Student 4",
            "rollNo": 104,
        },
        {
            "username": "student5",
            "password": "student123",
            "role": "student",
            "name": "Student 5",
            "rollNo": 105,
        },
    ]

    users = users_collection()
    for user in fixed_users:
        users.update_one(
            {"username": user["username"]},
            {"$set": user, "$setOnInsert": {"createdAt": datetime.utcnow()}},
            upsert=True,
        )


def seed_settings() -> None:
    settings = settings_collection()
    settings.update_one(
        {"key": "app_settings"},
        {
            "$set": {
                "subjectName": DEFAULT_SUBJECT_NAME,
                "totalLectures": DEFAULT_TOTAL_LECTURES,
                "updatedAt": datetime.utcnow(),
            },
            "$setOnInsert": {"key": "app_settings", "createdAt": datetime.utcnow()},
        },
        upsert=True,
    )


def seed_attendance() -> None:
    """Keep attendance collection present but empty for a fresh project."""
    attendance_collection().delete_many({})


def run_seed() -> None:
    ensure_indexes()
    seed_users()
    seed_settings()
    seed_attendance()


if __name__ == "__main__":
    run_seed()
    print("Seed completed successfully.")
