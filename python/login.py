import streamlit as st
from navigation import main_page  # Import main_page from navigation.py

def login_page():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.button("Login")

    actual_email = "admin"
    actual_password = "password"

    if submit and email == actual_email and password == actual_password:
        st.success("Login successful")
        st.session_state.logged_in = True
        st.rerun()
    elif submit and email != actual_email and password != actual_password:
        st.error("Login failed")
    else:
        pass