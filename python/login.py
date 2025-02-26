import streamlit as st
import sqlite3
from navigation import main_page  # Import main_page from navigation.py
from hashlib import sha256

def login_page():
    
    st.title("Login")
    with st.form(key="login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    

    if submit:
        with sqlite3.connect("test.db") as conn:
            cursor = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            if cursor.fetchone():
                user_role = cursor.fetchone()[4]  # Assuming the role is the third column in the users table
                st.session_state.user_role = user_role
                st.success("Login successful")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.write("Invalid username or password")
                st.error("Invalid username or password")
                
    else:
        pass