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
users_collection = db["users"]

def advisor_management_page():
    st.title("Advisor Management", anchor=False)

    if "subscription_type" not in st.session_state or st.session_state.subscription_type != "Advisor":
        st.error("Access denied. This page is only for advisors.")
        return

    st.write("View and respond to conversations from users:")

    # Fetch distinct user IDs with messages
    user_ids = messages_collection.distinct("customerId")
    if not user_ids:
        st.write("No messages yet.")
        return

    # Select user conversation
    selected_user_id = st.selectbox("Select a user to view their conversation:",
                                    user_ids, format_func=lambda uid: get_user_name(uid))

    # Fetch conversation messages for this user
    messages = list(messages_collection.find({"customerId": selected_user_id}).sort("timestamp", 1))

    # Display conversation
    st.subheader("Conversation", anchor=False)
    for msg in messages:
        sender = msg.get("sender", "user")
        if sender == "user":
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
                "advisorId": st.session_state.user_id,
                "sender": "Advisor",
                "message": new_message,
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            })
            st.rerun()

def get_user_name(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return f"{user.get('first_name', 'Unknown')} {user.get('last_name', '')}"
    return "Unknown User"
