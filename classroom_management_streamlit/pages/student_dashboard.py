import pandas as pd
import streamlit as st

from utils.attendance import get_settings, student_lecture_wise_rows, student_personal_summary
from utils.helpers import attendance_progress, status_tag


def render_student_dashboard(user: dict) -> None:
    st.title("Student Dashboard")

    st.subheader("Personal Info")
    col1, col2, col3 = st.columns(3)
    col1.write(f"**Student Name:** {user.get('name')}")
    col2.write(f"**Roll Number:** {user.get('rollNo')}")
    col3.write(f"**Username:** {user.get('username')}")

    st.divider()
    st.subheader("Attendance Summary")
    settings = get_settings()
    summary = student_personal_summary(user.get("id"))

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Lectures", summary["total_lectures"])
    m2.metric("Lectures Attended", summary["lectures_attended"])
    m3.metric("Attendance Percentage", f"{summary['percentage']}%")

    st.markdown(f"Status: {status_tag(summary['status'])}", unsafe_allow_html=True)
    attendance_progress(summary["percentage"])

    st.divider()
    st.subheader("Lecture-wise Attendance")
    lecture_rows = student_lecture_wise_rows(user.get("id"))

    if lecture_rows:
        df = pd.DataFrame(lecture_rows)
        st.dataframe(df, use_container_width=True)

        present_absent = df["Status"].value_counts().to_dict()
        chart_df = pd.DataFrame(
            {
                "Status": ["Present", "Absent"],
                "Count": [present_absent.get("Present", 0), present_absent.get("Absent", 0)],
            }
        ).set_index("Status")
        st.bar_chart(chart_df)
    else:
        st.info("No attendance records found yet.")

    st.caption(f"Subject: {settings.get('subjectName', 'Classroom Subject')}")
