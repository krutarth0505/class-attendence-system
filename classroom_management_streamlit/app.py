import streamlit as st

from config import APP_TITLE, MONGO_URI
from db import ensure_indexes
from pages.admin_dashboard import render_admin_dashboard
from pages.login import render_login_page
from pages.student_dashboard import render_student_dashboard
from pages.teacher_dashboard import render_teacher_dashboard
from utils.auth import current_user, ensure_auth_state, is_authenticated, logout_user, require_role
from utils.helpers import inject_base_styles, show_role_sidebar


st.set_page_config(page_title=APP_TITLE, page_icon="🏫", layout="wide")


def _render_db_error(exc: Exception) -> None:
    st.error("Unable to connect to MongoDB Atlas.")
    st.caption(str(exc))

    host_hint = ""
    if "@" in MONGO_URI:
        host_hint = MONGO_URI.split("@", 1)[1].split("/", 1)[0]

    st.markdown("### Fix Checklist")
    st.markdown("1. In Streamlit Cloud Secrets, set `MONGODB_ATLAS_URI` with the real password (not `<db_password>`).")
    st.markdown("2. In MongoDB Atlas Network Access, allow `0.0.0.0/0` for deployment testing.")
    st.markdown("3. In Atlas Database Access, ensure the DB user exists and has read/write on your DB.")
    st.markdown("4. Keep `DB_NAME = \"classroom_management\"` in Streamlit Secrets.")
    if host_hint:
        st.info(f"Atlas host in current URI: `{host_hint}`")


def _logout_button() -> None:
    _, right = st.columns([0.84, 0.16])
    with right:
        if st.button("Logout", use_container_width=True):
            logout_user()
            st.rerun()


def main() -> None:
    try:
        ensure_indexes()
    except Exception as exc:
        _render_db_error(exc)
        st.stop()

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
