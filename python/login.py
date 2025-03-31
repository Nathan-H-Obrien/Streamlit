import streamlit as st
from pymongo import MongoClient
from hashlib import sha256
from new_user import new_userPage

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"  # Change if using MongoDB Atlas
DATABASE_NAME = "WealthWise"  # Change this to your database name

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["customers"]  # Collection for storing user credentials

def login_page():
    if "page_selection" not in st.session_state:
        st.session_state.page_selection = "Login"

    if st.session_state.page_selection == "Login":
        st.title("Login")
        
        with st.form(key="login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
        
        if st.button("New User"):
            st.session_state.page_selection = "New User"
            st.rerun()

        if submit:
            hashed_password = sha256(password.encode()).hexdigest()
            email = email.lower()  # Normalize email to lowercase
            user = users_collection.find_one({"email": email, "password": hashed_password})
            
            if user:
                st.success("Login successful")
                st.session_state.logged_in = True
                st.session_state.user_id = str(user["_id"])  # Store user_id in session state
                st.session_state.page_selection = "🏠 Home"   
                st.rerun()
            else:
                st.error("Invalid username or password")
    elif st.session_state.page_selection == "New User":
        new_userPage()
