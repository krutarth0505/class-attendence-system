import streamlit as st

from config import APP_TITLE
from db import ensure_indexes
from pages.admin_dashboard import render_admin_dashboard
from pages.login import render_login_page
from pages.student_dashboard import render_student_dashboard
from pages.teacher_dashboard import render_teacher_dashboard
from utils.auth import current_user, ensure_auth_state, is_authenticated, logout_user, require_role
from utils.helpers import inject_base_styles, show_role_sidebar


st.set_page_config(page_title=APP_TITLE, page_icon="🏫", layout="wide")


def _logout_button() -> None:
    _, right = st.columns([0.84, 0.16])
    with right:
        if st.button("Logout", use_container_width=True):
            logout_user()
            st.rerun()


def main() -> None:
    ensure_indexes()
    ensure_auth_state()
    inject_base_styles()

    if not is_authenticated():
        render_login_page()
        return

    user = current_user()
    show_role_sidebar(user)
    _logout_button()

    role = user.get("role")
    if role == "admin":
        if require_role("admin"):
            render_admin_dashboard()
        return

    if role == "teacher":
        if require_role("teacher"):
            render_teacher_dashboard()
        return

    if role == "student":
        if require_role("student"):
            render_student_dashboard(user)
        return

    st.error("Unknown user role. Please contact admin.")


if __name__ == "__main__":
    main()
