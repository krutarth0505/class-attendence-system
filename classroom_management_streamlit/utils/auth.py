import streamlit as st

from db import users_collection


def get_user_by_username(username: str):
    return users_collection().find_one({"username": username})


def validate_user(username: str, password: str):
    """Simple fixed-password validation from MongoDB users collection."""
    user = get_user_by_username(username)
    if not user:
        return None

    if user.get("password") != password:
        return None

    return user


def login_user(user: dict) -> None:
    st.session_state["is_authenticated"] = True
    st.session_state["current_user"] = {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "role": user.get("role"),
        "name": user.get("name"),
        "rollNo": user.get("rollNo"),
    }


def logout_user() -> None:
    st.session_state["is_authenticated"] = False
    st.session_state["current_user"] = None


def is_authenticated() -> bool:
    return st.session_state.get("is_authenticated", False)


def current_user():
    return st.session_state.get("current_user")


def ensure_auth_state() -> None:
    if "is_authenticated" not in st.session_state:
        st.session_state["is_authenticated"] = False
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None


def require_role(required_role: str) -> bool:
    user = current_user()
    if not user or user.get("role") != required_role:
        st.error("You do not have permission to access this page.")
        return False
    return True
