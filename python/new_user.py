import streamlit as st
import sqlite3
from navigation import main_page  # Import main_page from navigation.py
from hashlib import sha256
import re
from create import generate_id
from create import add_user


def new_userPage():

    def check_password(password):
        if len(password) < 8:
            st.write("invalid password")
            return

        has_upper_case = bool(re.search(r'[A-Z]', password))
        has_lower_case = bool(re.search(r'[a-z]', password))
        has_numbers = bool(re.search(r'\d', password))
        has_non_alphas = bool(re.search(r'\W', password))

        if sum([has_upper_case, has_lower_case, has_numbers, has_non_alphas]) < 3:
            st.write("invalid password")
            st.write("Password must contain at least 3 of the following:")
            st.write("Uppercase letter, lowercase letter, number, special character")
            return

    st.title("New User Registration")
    with st.form(key="new_user_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        while password != password_confirm:
            st.write("Passwords do not match")
        while first_name == "":
            st.write("Invalid first name")
        while last_name == "":
            st.write("Invalid last name")
        
        submit = st.form_submit_button("Register", disabled=not (
            first_name and last_name and email and password and password_confirm and
            password == password_confirm and
            re.match(r"[^@]+@[^@]+\.[^@]+", email) and
            check_password(password) is None
        ))
        

    if submit:
        check_password(password)
        while password != password_confirm:
            st.error("Passwords do not match")
            st.write("Passwords do not match")
        with sqlite3.connect("/app/test.db") as conn:
        #with sqlite3.connect("test.db") as conn:
            cursor = conn.execute("SELECT * FROM customers WHERE email = ? AND password = ?", (email, sha256(password.encode()).hexdigest()))
            if cursor.fetchone():
                st.error("User already exists")
                st.write("User already exists")
            else:
                add_user(first_name, last_name, email, password)
                st.success("User registered")
                st.write("User registered")
                st.session_state.logged_in = True
                st.rerun()
                
