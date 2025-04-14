import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"
DATABASE_NAME = "WealthWise"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]
meetings_collection = db["appointments"]
messages_collection = db["messages"]

@st.dialog("Delete User?")
def delete_user(user):
    st.write("Are you sure you want to delete this user?", anchor=False)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirm", type="primary", use_container_width=True):
            users_collection.delete_one({"_id": user["_id"]})
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

def admin_management_page():
    st.title("Admin Management", anchor=False)

    if "subscription_type" not in st.session_state or st.session_state.subscription_type != "Admin":
        st.error("Access denied. This page is only for admins.")
        return

    tabs = st.tabs(["User List", "All Meetings", "All Messages", "Add New User"])

    # Tab 1: User List
    with tabs[0]:
        st.subheader("Registered Users", anchor=False)
        users = list(users_collection.find())
        for user in users:
            st.write(f"**Name:** {user['first_name']} {user['last_name']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Subscription:** {user.get('subscription')}")
            if st.button(f"Delete {user['email']}", key=f"del_{user['_id']}", type="primary"):
                delete_user(user)
            st.write("---")

    # Tab 2: All Meetings
    with tabs[1]:
        st.subheader("All Scheduled Meetings", anchor=False)
        meetings = list(meetings_collection.find())
        for meeting in meetings:
            advisor = users_collection.find_one({"_id": ObjectId(meeting["advisorId"])})
            customer = users_collection.find_one({"_id": ObjectId(meeting["customerId"])})
            st.write(f"**Advisor:** {advisor['first_name']} {advisor['last_name'] if advisor else 'Unknown'}")
            st.write(f"**Customer:** {customer['first_name']} {customer['last_name'] if customer else 'Unknown'}")
            st.write(f"**Date & Time:** {meeting['date']} {meeting['time']}")
            st.write("---")

    # Tab 3: All Messages
    with tabs[2]:
        st.subheader("All Messages", anchor=False)
        messages = list(messages_collection.find())
        for message in messages:
            customer = users_collection.find_one({"_id": ObjectId(message["customerId"])})
            advisor = users_collection.find_one({"_id": ObjectId(message["advisorId"])})
            st.write(f"**From:** {customer['first_name']} {customer['last_name'] if customer else 'Unknown'}")
            st.write(f"**To:** {advisor['first_name']} {advisor['last_name'] if advisor else 'Unknown'}")
            st.write(f"**Message:** {message['message']}")
            if "response" in message:
                st.success(f"Advisor Response: {message['response']}")
            st.write(f"**Timestamp:** {message['timestamp']}")
            st.write("---")

    # Tab 4: Add New User
    with tabs[3]:
        st.subheader("Add New User", anchor=False)
        with st.form("add_user_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            subscription_type = st.selectbox("Subscription Type", ["Basic", "Elite", "Advisor", "Admin"])
            submit = st.form_submit_button("Add User")

            if submit:
                users_collection.insert_one({
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                    "subscription_type": subscription_type
                })
                st.success(f"User {email} added successfully!")
                st.rerun()
