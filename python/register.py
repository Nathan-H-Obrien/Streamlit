import streamlit as st
from pymongo import MongoClient
from hashlib import sha256
import re

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"  # Change if using MongoDB Atlas
DATABASE_NAME = "WealthWise"  # Change this to your database name

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]  # Collection for storing user credentials

def register_page():
    def check_password(password):
        if len(password) < 8:
            return False

        has_upper_case = bool(re.search(r'[A-Z]', password))
        has_lower_case = bool(re.search(r'[a-z]', password))
        has_numbers = bool(re.search(r'\d', password))
        has_non_alphas = bool(re.search(r'\W', password))

        if sum([has_upper_case, has_lower_case, has_numbers, has_non_alphas]) < 3:
            st.write("Password must contain at least 3 of the following:")
            st.write("Uppercase letter, lowercase letter, number, special character")
            return False

        return True

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.header("New User Registration", anchor=False)
        with st.form(key="new_user_form", border=False):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            email = email.lower()  # Normalize email to lowercase
            password = st.text_input("Password", type="password")
            password_confirm = st.text_input("Confirm Password", type="password")
            
            submit = st.form_submit_button("Register", use_container_width=True, type="primary")
        
        if st.button("Already have an account? Login here.", use_container_width=True):
                st.session_state.page_selection = "Login"
                st.rerun()
            
        if submit:
            if not (first_name and last_name and email and password and password_confirm):
                st.error("All fields are required")
            elif password != password_confirm:
                st.error("Passwords do not match")
            elif not check_password(password):
                st.error("""
                Password must contain at least **3 of the following**:
                - Uppercase letter
                - Lowercase letter
                - Number
                - Special character
                """)
            else:
                existing_user = users_collection.find_one({"email": email})
                if existing_user:
                    st.error("User already exists")
                else:
                    hashed_password = sha256(password.encode()).hexdigest()
                    user_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": hashed_password,
                    "subscription": "Basic"
                    }

                    users_collection.insert_one(user_data)  # Insert into MongoDB
                    st.success("User registered")
                    
                    # Store user info in session state
                    st.session_state.logged_in = True
                    st.session_state.user_id = str(user_data["_id"])
                    st.session_state.subscription_type = "Basic"
                    
                    # Redirect to home page
                    st.session_state.page_selection = "🏠 Home"
                    st.rerun()