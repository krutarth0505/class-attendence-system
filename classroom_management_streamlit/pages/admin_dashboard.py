import pandas as pd
import streamlit as st

from utils.attendance import (
    admin_summary_metrics,
    build_student_attendance_table,
    get_settings,
    update_total_lectures,
)
from utils.helpers import status_tag


def render_admin_dashboard() -> None:
    st.title("Admin Dashboard")

    settings = get_settings()
    subject_name = settings.get("subjectName", "Classroom Subject")
    st.caption(f"Subject: {subject_name}")

    metrics = admin_summary_metrics()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", metrics["total_students"])
    col2.metric("Total Lectures", metrics["total_lectures"])
    col3.metric("Average Attendance", f"{metrics['average_attendance']}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Below 75%", metrics["below_75"])
    col5.metric("75% to 90%", metrics["between_75_90"])
    col6.metric("90% to 100%", metrics["between_90_100"])

    st.divider()
    st.subheader("Manage Total Lectures")
    with st.form("total_lectures_form"):
        total_lectures = st.number_input(
            "Set total lectures",
            min_value=0,
            max_value=500,
            value=int(settings.get("totalLectures", 0)),
            step=1,
        )
        save = st.form_submit_button("Save Lectures")

    if save:
        update_total_lectures(int(total_lectures))
        st.success("Total lectures updated successfully.")
        st.rerun()

    st.divider()
    st.subheader("Student Attendance Table")

    rows = build_student_attendance_table()
    df = pd.DataFrame(rows)

    search = st.text_input("Search by student name or roll number")
    category = st.selectbox(
        "Filter by attendance category",
        ["All", "Low Attendance", "Average", "Excellent"],
        index=0,
    )

    if not df.empty:
        if search:
            search_lower = search.lower()
            df = df[
                df["Student Name"].str.lower().str.contains(search_lower)
                | df["Roll Number"].astype(str).str.contains(search_lower)
            ]

        if category != "All":
            df = df[df["Attendance Status"] == category]

        display_df = df.copy()
        display_df["Attendance Status"] = display_df["Attendance Status"].apply(status_tag)
        st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No students found.")

    st.divider()
    st.subheader("Attendance Analytics")
    chart_data = pd.DataFrame(
        {
            "Category": ["Below 75", "75 to 90", "90 to 100"],
            "Count": [
                metrics["below_75"],
                metrics["between_75_90"],
                metrics["between_90_100"],
            ],
        }
    ).set_index("Category")

    st.bar_chart(chart_data)
