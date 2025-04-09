import streamlit as st
from pymongo import MongoClient
from hashlib import sha256
from bson.objectid import ObjectId  # Import ObjectId for querying MongoDB
import re

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"  # Change if using MongoDB Atlas
DATABASE_NAME = "WealthWise"  # Change this to your database name
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]  # Collection for storing user credentials

def check_password(password):
    if len(password) < 8:
        st.write("Invalid password")
        return False

    has_upper_case = bool(re.search(r'[A-Z]', password))
    has_lower_case = bool(re.search(r'[a-z]', password))
    has_numbers = bool(re.search(r'\d', password))
    has_non_alphas = bool(re.search(r'\W', password))

    if sum([has_upper_case, has_lower_case, has_numbers, has_non_alphas]) < 3:
        st.write("Invalid password")
        st.write("Password must contain at least 3 of the following:")
        st.write("Uppercase letter, lowercase letter, number, special character")
        return False

    return True
def user_management_page():
    st.title("User Management")
    
    # Create tabs
    tabs = st.tabs([
        "Payment & Subscription", 
        "Chat with Advisor", 
        "Manage Portfolio", 
        "View Events/Meetings",
        "View Info & Delete Account"
    ])
    
    # Tab 1: Payment & Subscription
    with tabs[0]:
        st.header("Payment & Subscription")
        st.write("Update your payment method and manage your subscription.")
        # Add logic for payment and subscription management here

    # Tab 2: Chat with Advisor
    with tabs[1]:
        st.header("Chat with Advisor")
        st.write("Start a conversation with your advisor.")
        # Add chat functionality here

    # Tab 3: Manage Portfolio
    with tabs[2]:
        st.header("Manage Portfolio")
        st.write("Add, manage, and view your stocks and portfolio.")
        # Add portfolio management functionality here

    # Tab 4: View Events/Meetings
    with tabs[3]:
        st.header("View Events/Meetings")
        st.write("View your registered events or scheduled meetings.")
        # Add event/meeting management functionality here

    # Tab 5: View Info & Delete Account
    with tabs[4]:
        st.header("Account Info")
        st.write("To view or edit your sensitive information, please re-enter your password.")
        
        # Ensure the user is logged in and their _id is available
        if "user_id" not in st.session_state:
            st.error("You must be logged in to view this page.")
            return
        
        # Initialize session state for password verification
        if "password_verified" not in st.session_state:
            st.session_state.password_verified = False
        
        if not st.session_state.password_verified:
            # Password input for verification
            password = st.text_input("Enter your password", type="password")
            if st.button("Verify Password"):
                # Verify the entered password
                hashed_password = sha256(password.encode()).hexdigest()
                try:
                    user = users_collection.find_one({"_id": ObjectId(st.session_state.user_id)})
                except Exception as e:
                    st.error("Invalid user ID format.")
                    return

                if user and hashed_password == user["password"]:
                    st.success("Password verified!")
                    st.session_state.password_verified = True
                    st.rerun()  # Force the app to refresh and show the editable fields
                else:
                    st.error("Incorrect password. Please try again.")
        else:
            # Query the database for the user's information
            try:
                user = users_collection.find_one({"_id": ObjectId(st.session_state.user_id)})
            except Exception as e:
                st.error("Invalid user ID format.")
                return

            if not user:
                st.error("User not found.")
                return
            
            # Display user information
            st.write(f"First Name: {user.get('first_name', 'N/A')}")
            st.write(f"Last Name: {user.get('last_name', 'N/A')}")
            st.write(f"Email: {user.get('email', 'N/A')}")
            
            # Editable fields
            first_name = st.text_input("Edit First Name", value=user.get("first_name", ""))
            last_name = st.text_input("Edit Last Name", value=user.get("last_name", ""))
            email = st.text_input("Edit Email", value=user.get("email", ""))
            new_password = st.text_input("Edit Password", type="password")
            password_confirm = st.text_input("Confirm New Password", type="password")
            
            if st.button("Save Changes"):
                # Error checking
                if not first_name or not last_name or not email or not new_password:
                    st.error("All fields are required.")
                elif "@" not in email:
                    st.error("Invalid email address.")
                elif new_password != password_confirm:
                    st.error("Passwords do not match")
                elif not check_password(new_password):
                    st.error("Invalid password")
                else:
                    # Hash the new password
                    hashed_new_password = sha256(new_password.encode()).hexdigest()
                    
                    # Update the user's information in the database
                    users_collection.update_one(
                        {"_id": ObjectId(st.session_state.user_id)},
                        {"$set": {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "password": hashed_new_password
                        }}
                    )
                    st.success("Changes saved successfully!")