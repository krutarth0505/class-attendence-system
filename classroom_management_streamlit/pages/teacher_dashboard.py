from datetime import date

import pandas as pd
import streamlit as st

from utils.attendance import (
    admin_summary_metrics,
    create_lecture_attendance,
    get_lecture,
    get_settings,
    get_students,
    lecture_history_rows,
    list_lectures,
    update_lecture_attendance,
)


def _attendance_form_fields(students, key_prefix: str, defaults=None):
    status_map = {}
    for student in students:
        sid = str(student["_id"])
        current_default = "Present"
        if defaults and sid in defaults:
            current_default = defaults[sid]

        status_map[sid] = st.radio(
            f"{student.get('name')} (Roll {student.get('rollNo')})",
            options=["Present", "Absent"],
            horizontal=True,
            key=f"{key_prefix}_status_{sid}",
            index=0 if current_default == "Present" else 1,
        )
    return status_map


def render_teacher_dashboard() -> None:
    st.title("Teacher Dashboard")

    settings = get_settings()
    metrics = admin_summary_metrics()
    students = get_students()

    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Subject Name", settings.get("subjectName", "Classroom Subject"))
    col2.metric("Total Students", len(students))
    col3.metric("Total Lectures", settings.get("totalLectures", 0))

    col4, col5, col6 = st.columns(3)
    col4.metric("Below 75%", metrics["below_75"])
    col5.metric("75% to 90%", metrics["between_75_90"])
    col6.metric("90% to 100%", metrics["between_90_100"])

    st.divider()
    tab1, tab2, tab3 = st.tabs(["Mark Attendance", "Update Attendance", "Lecture History"])

    with tab1:
        st.subheader("Mark Attendance Lecture-wise")
        total_lectures = int(settings.get("totalLectures", 0))

        if total_lectures <= 0:
            st.warning("Admin must set total lectures greater than 0 before marking attendance.")
        else:
            with st.form("mark_attendance_form"):
                lecture_no = st.number_input(
                    "Lecture Number",
                    min_value=1,
                    max_value=total_lectures,
                    value=1,
                    step=1,
                )
                lecture_date = st.date_input("Lecture Date", value=date.today())
                st.write("Select attendance for all students:")
                status_map = _attendance_form_fields(students, key_prefix="mark")
                submit_mark = st.form_submit_button("Save Attendance")

            if submit_mark:
                if get_lecture(int(lecture_no)):
                    st.error("Attendance already exists for this lecture. Use Update Attendance tab.")
                else:
                    created = create_lecture_attendance(int(lecture_no), lecture_date, status_map)
                    if created:
                        st.success("Attendance saved successfully.")
                    else:
                        st.error("Unable to save attendance.")

    with tab2:
        st.subheader("Update Existing Attendance")
        lectures = list_lectures()

        if not lectures:
            st.info("No attendance records found to update.")
        else:
            lecture_options = [lec.get("lectureNo") for lec in lectures]
            selected_lecture = st.selectbox("Select Lecture", lecture_options)
            selected_doc = get_lecture(int(selected_lecture))

            default_date = date.today()
            if selected_doc and selected_doc.get("date"):
                default_date = date.fromisoformat(selected_doc.get("date"))

            defaults = {}
            for item in selected_doc.get("attendance", []):
                defaults[str(item.get("studentId"))] = item.get("status", "Absent")

            with st.form("update_attendance_form"):
                new_date = st.date_input("Lecture Date", value=default_date)
                st.write("Edit attendance:")
                status_map = _attendance_form_fields(students, key_prefix="update", defaults=defaults)
                submit_update = st.form_submit_button("Update Attendance")

            if submit_update:
                updated = update_lecture_attendance(int(selected_lecture), new_date, status_map)
                if updated:
                    st.success("Attendance updated successfully.")
                else:
                    st.error("Unable to update attendance.")

    with tab3:
        st.subheader("Lecture History")
        history = lecture_history_rows()
        if history:
            st.dataframe(pd.DataFrame(history), use_container_width=True)
        else:
            st.info("No lecture history available yet.")
