from bson import ObjectId
from pymongo import MongoClient
import streamlit as st
from datetime import datetime

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"
DATABASE_NAME = "WealthWise"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]
messages_collection = db["messages"]

def chat_page():
    st.header("Chat with Advisor", anchor=False)
    st.write("Start a conversation with your advisor.")

    if "user_id" not in st.session_state:
        st.error("You must be logged in to chat with your advisor.")
        st.stop()

    user_id = st.session_state.user_id

    # Get the user's subscription type
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        st.error("User not found.")
        st.stop()

    subscription = user.get("subscription", "Basic")

    if subscription == "Basic":
        st.warning("Only Elite users can chat with an advisor.")
        if st.button("Upgrade to Elite Subscription here!", use_container_width=True):
            st.session_state.page_selection = "👤 User Management"
            st.rerun()
        return

    # Get advisor list (only Advisor subscription type)
    advisors = list(users_collection.find({"subscription": "Advisor"}))
    if not advisors:
        st.warning("No advisors available right now.")
        return

    advisor_options = {str(a['_id']): f"{a['first_name']} {a['last_name']}" for a in advisors}
    advisor_id = st.selectbox(
        "Select Advisor",
        options=list(advisor_options.keys()),
        format_func=lambda x: advisor_options[x]
    )

    st.subheader("Chat History", anchor=False)

    # Fetch conversation between this user and selected advisor
    messages = messages_collection.find({
        "customerId": user_id,
        "advisorId": advisor_id
    }).sort("timestamp", 1)

    for msg in messages:
        sender = "You" if msg["sender"] == "user" else advisor_options.get(msg["advisorId"], "Advisor")
        if msg["sender"] == "user":
            st.write(f"**🟢 {sender}:** {msg['message']}")
        else:
            st.write(f"**💬 {sender}:** {msg['message']}")

    st.write("---")

    # Message input form
    with st.form("chat_form"):
        message_text = st.text_input("Your message:")
        submitted = st.form_submit_button("Send")

        if submitted and message_text.strip():
            messages_collection.insert_one({
                "customerId": user_id,
                "advisorId": advisor_id,
                "sender": "user",
                "message": message_text.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            })
            st.success("Message sent!")
            st.rerun()
