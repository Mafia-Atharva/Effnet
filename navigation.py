import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():


    with st.sidebar:
        st.title("Navigation")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/home.py", label="Home", icon="🏠")
            st.page_link("pages/upload.py", label="Upload Image", icon="📷")
            st.page_link("pages/appendix.py", label="Appendix", icon="📄")

            st.write("")

            if st.button("Log out",key="logout"):
                logout()

        elif get_current_page_name() != "app":
            # Redirect unauthorized users back to login page
            st.switch_page("app.py")

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("app.py")
