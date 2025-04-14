import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# MongoDB connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"
DATABASE_NAME = "WealthWise"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
messages_collection = db["messages"]
meetings_collection = db["appointments"]
users_collection = db["users"]

def advisor_management_page():
    st.title("Advisor Management", anchor=False)
    st.write("Manage business with Users.")

    if "subscription_type" not in st.session_state or st.session_state.subscription_type != "Advisor":
        st.error("Access denied. This page is only for advisors.")
        return

    # Create tabs
    tabs = st.tabs([
        "Chat with Users",
        "Scheduled Meetings"
    ])

    # Chat with Users
    with tabs[0]:
        advisor_id = st.session_state.user_id  # Current logged-in advisor's ID

        # Fetch distinct user IDs who have messaged this advisor
        user_ids = messages_collection.distinct("customerId", {"advisorId": advisor_id})
        if not user_ids:
            st.write("No messages yet.")
            return

        # Select user conversation
        selected_user_id = st.selectbox(
            "Select a user to view their conversation:",
            user_ids, 
            format_func=lambda uid: get_user_name(uid)
        )

        # Fetch conversation messages for this user and this advisor
        messages = list(messages_collection.find({
            "customerId": selected_user_id,
            "advisorId": advisor_id
        }).sort("timestamp", 1))

        # Display conversation
        st.subheader("Conversation", anchor=False)
        for msg in messages:
            sender = msg.get("sender", "user")
            if sender.lower() == "user":
                st.write(f"**💬 {get_user_name(msg['customerId'])}:** {msg['message']}")
            else:
                st.write(f"**🟢 You:** {msg['message']}")

        st.write("---")

        # Send new advisor message
        new_message = st.text_input("Your message:", key="advisor_message_input")
        if st.button("Send Message"):
            if new_message.strip() != "":
                messages_collection.insert_one({
                    "customerId": selected_user_id,
                    "advisorId": advisor_id,
                    "sender": "Advisor",
                    "message": new_message,
                    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                })
                st.rerun()


    # Scheduled Meetings (Advisor View)
    with tabs[1]:
        st.write("Scheduled Meetings:", anchor=False)

        if "user_id" not in st.session_state or st.session_state.subscription_type != "Advisor":
            st.error("Access denied. This section is for advisors only.")
            st.stop()

        advisor_id = st.session_state.user_id

        # Fetch meetings for this advisor
        meetings = list(meetings_collection.find({"advisorId": advisor_id}).sort("scheduled_at", 1))

        if not meetings:
            st.write("No meetings scheduled.")
        else:
            for meeting in meetings:
                # Get customer info
                customer = users_collection.find_one({"_id": ObjectId(meeting["customerId"])})
                customer_name = f"{customer['first_name']} {customer['last_name']}" if customer else "Unknown User"

                # Format datetime
                meeting_time = meeting["scheduled_at"].strftime("%B %d, %Y at %I:%M %p")

                # Display meeting info
                st.write(f"**{customer_name}:** {meeting_time}")
                st.write("---")


def get_user_name(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return f"{user.get('first_name', 'Unknown')} {user.get('last_name', '')}"
    return "Unknown User"
