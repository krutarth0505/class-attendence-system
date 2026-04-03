from datetime import datetime
from typing import Dict, List, Optional

from bson import ObjectId

from config import DEFAULT_SUBJECT_NAME, DEFAULT_TOTAL_LECTURES
from db import attendance_collection, settings_collection, users_collection


def get_settings() -> dict:
    settings = settings_collection().find_one({"key": "app_settings"})
    if not settings:
        settings = {
            "key": "app_settings",
            "subjectName": DEFAULT_SUBJECT_NAME,
            "totalLectures": DEFAULT_TOTAL_LECTURES,
        }
        settings_collection().insert_one(settings)
    return settings


def update_total_lectures(total_lectures: int) -> None:
    settings_collection().update_one(
        {"key": "app_settings"},
        {
            "$set": {
                "totalLectures": int(total_lectures),
                "updatedAt": datetime.utcnow(),
            },
            "$setOnInsert": {
                "key": "app_settings",
                "subjectName": DEFAULT_SUBJECT_NAME,
                "createdAt": datetime.utcnow(),
            },
        },
        upsert=True,
    )


def get_students() -> List[dict]:
    return list(users_collection().find({"role": "student"}).sort("rollNo", 1))


def get_lecture(lecture_no: int) -> Optional[dict]:
    return attendance_collection().find_one({"lectureNo": int(lecture_no)})


def list_lectures() -> List[dict]:
    return list(attendance_collection().find({}).sort("lectureNo", 1))


def _build_attendance_payload(status_map: Dict[str, str]) -> List[dict]:
    payload = []
    for student_id, status in status_map.items():
        payload.append(
            {
                "studentId": ObjectId(student_id),
                "status": status,
            }
        )
    return payload


def create_lecture_attendance(lecture_no: int, date_value, status_map: Dict[str, str]) -> bool:
    if get_lecture(lecture_no):
        return False

    attendance_collection().insert_one(
        {
            "lectureNo": int(lecture_no),
            "date": date_value.isoformat(),
            "attendance": _build_attendance_payload(status_map),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
    )
    return True


def update_lecture_attendance(lecture_no: int, date_value, status_map: Dict[str, str]) -> bool:
    result = attendance_collection().update_one(
        {"lectureNo": int(lecture_no)},
        {
            "$set": {
                "date": date_value.isoformat(),
                "attendance": _build_attendance_payload(status_map),
                "updatedAt": datetime.utcnow(),
            }
        },
    )
    return result.matched_count > 0


def _status_by_percentage(percent: float, student_view: bool = False) -> str:
    if percent < 75:
        return "Low Attendance"
    if percent < 90:
        return "Good Attendance" if student_view else "Average"
    return "Excellent"


def _attended_count(student_id: ObjectId, lectures: List[dict]) -> int:
    attended = 0
    for lecture in lectures:
        for item in lecture.get("attendance", []):
            if item.get("studentId") == student_id and item.get("status") == "Present":
                attended += 1
    return attended


def build_student_attendance_table() -> List[dict]:
    settings = get_settings()
    total_lectures = int(settings.get("totalLectures", 0))
    lectures = list_lectures()

    rows = []
    for student in get_students():
        student_id = student.get("_id")
        attended = _attended_count(student_id, lectures)
        percentage = round((attended / total_lectures) * 100, 2) if total_lectures > 0 else 0.0
        rows.append(
            {
                "studentId": str(student_id),
                "Student Name": student.get("name", ""),
                "Roll Number": student.get("rollNo", ""),
                "Lectures Attended": attended,
                "Total Lectures": total_lectures,
                "Attendance Percentage": percentage,
                "Attendance Status": _status_by_percentage(percentage),
            }
        )
    return rows


def admin_summary_metrics() -> dict:
    rows = build_student_attendance_table()
    total_students = len(rows)
    total_lectures = int(get_settings().get("totalLectures", 0))

    percentages = [row["Attendance Percentage"] for row in rows]
    average_attendance = round(sum(percentages) / total_students, 2) if total_students else 0.0

    below_75 = len([x for x in percentages if x < 75])
    between_75_90 = len([x for x in percentages if 75 <= x < 90])
    between_90_100 = len([x for x in percentages if 90 <= x <= 100])

    return {
        "total_students": total_students,
        "total_lectures": total_lectures,
        "average_attendance": average_attendance,
        "below_75": below_75,
        "between_75_90": between_75_90,
        "between_90_100": between_90_100,
    }


def lecture_history_rows() -> List[dict]:
    rows = []
    for lecture in list_lectures():
        present_count = len([x for x in lecture.get("attendance", []) if x.get("status") == "Present"])
        rows.append(
            {
                "Lecture Number": lecture.get("lectureNo"),
                "Date": lecture.get("date"),
                "Present Students": present_count,
            }
        )
    return rows


def student_personal_summary(student_id: str) -> dict:
    settings = get_settings()
    total_lectures = int(settings.get("totalLectures", 0))
    lectures = list_lectures()

    object_id = ObjectId(student_id)
    attended = _attended_count(object_id, lectures)
    percentage = round((attended / total_lectures) * 100, 2) if total_lectures > 0 else 0.0

    return {
        "total_lectures": total_lectures,
        "lectures_attended": attended,
        "percentage": percentage,
        "status": _status_by_percentage(percentage, student_view=True),
    }


def student_lecture_wise_rows(student_id: str) -> List[dict]:
    object_id = ObjectId(student_id)
    rows = []

    for lecture in list_lectures():
        status = "Absent"
        for item in lecture.get("attendance", []):
            if item.get("studentId") == object_id:
                status = item.get("status", "Absent")
                break

        rows.append(
            {
                "Lecture Number": lecture.get("lectureNo"),
                "Date": lecture.get("date"),
                "Status": status,
            }
        )

    return rows
