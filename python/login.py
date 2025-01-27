import streamlit as st
import sqlite3
from navigation import main_page  # Import main_page from navigation.py

def login_page():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.button("Login")

    if submit:
        with sqlite3.connect("test.db") as conn:
            cursor = conn.execute("SELECT * FROM admin WHERE email = ? AND password = ?", (email, password))
            cursor2 = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            if cursor.fetchone():
                st.rerun()
            elif cursor2.fetchone():
                st.rerun()
            else:
                st.write("Invalid username or password")
                st.error("Invalid username or password")
                
    else:
        pass