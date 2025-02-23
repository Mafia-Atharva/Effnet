import streamlit as st

st.sidebar.button("Logout", on_click=lambda: (st.session_state.update({"authenticated": False})))
    