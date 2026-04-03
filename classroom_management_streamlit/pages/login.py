import streamlit as st

from config import APP_TITLE
from utils.auth import login_user, validate_user


def render_login_page() -> None:
    st.title(APP_TITLE)
    st.subheader("Login")
    st.caption("Use your fixed username/password provided in seed data.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if not username or not password:
            st.warning("Please enter both username and password.")
            return

        user = validate_user(username.strip(), password.strip())
        if not user:
            st.error("Invalid username or password.")
            return

        login_user(user)
        st.success("Login successful.")
        st.rerun()
