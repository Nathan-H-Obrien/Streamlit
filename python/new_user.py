import streamlit as st
import sqlite3
from navigation import main_page  # Import main_page from navigation.py
from hashlib import sha256
import re
from create import generate_id


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
        submit = st.form_submit_button("Register")
        

    if submit:
        while len(first_name) > 20 or len(first_name) < 1:
            st.error("Invalid first name")
            st.write("Invalid first name")
            st.write("Enter a valid first name")
            st.text_input("First Name")
        while len(last_name) > 20 or len(last_name) < 1:
            st.error("Invalid last name")
            st.write("Invalid last name")
            st.write("Enter a valid last name")
            st.text_input("Last Name")
        while len(email) > 35 or len(email) < 1:
            st.error("Invalid email")
            st.write("Invalid email")
            st.write("Enter a valid email")
            st.text_input("Email")
        check_password(password)
        with sqlite3.connect("/app/python/test.db") as conn:
            cursor = conn.execute("SELECT * FROM customers WHERE email = ? AND password = ?", (email, sha256(password.encode()).hexdigest()))
            if cursor.fetchone():
                st.success("User already exists")
                st.session_state.logged_in = True
                st.rerun()
            else:
                conn.execute("INSERT INTO customers (customer_id, first_name, last_name, email, password, status, subscription, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", (generate_id(), first_name, last_name, email, sha256(password.encode()).hexdigest(), 'active', 'basic'))
                st.success("User registered")