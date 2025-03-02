import streamlit as st

def hide_streamlit_style():
    hide_default_format = """
           <style>
           #MainMenu {visibility: hidden; }
           footer {visibility: hidden;}
           </style>
           """
    st.markdown(hide_default_format, unsafe_allow_html=True)