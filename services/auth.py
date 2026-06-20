import streamlit as st
from services.user_manager import get_user

def login(logo_path=None):
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "username" not in st.session_state:
        st.session_state.username = None

    if "role" not in st.session_state:
        st.session_state.role = None

    if st.session_state.authenticated:
        return True

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }

            [data-testid="collapsedControl"] {
                display: none;
            }

            .block-container {
                padding-top: 4rem;
                max-width: 700px;
                margin: auto;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    if logo_path is not None:
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            st.image(str(logo_path), width=140)

    st.markdown(
        """
        <h1 style='text-align:center;color:#1f5ea8;'>
            TalentBridge Login
        </h1>
        <p style='text-align:center;color:gray;'>
            AI-Powered Recruitment Intelligence Platform
        </p>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        user = get_user(username, password)

        if user:
            st.session_state.authenticated = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]
            st.rerun()
        else:
            st.error("Invalid username or password.")

    return False