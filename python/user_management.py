import streamlit as st
from pymongo import MongoClient
from hashlib import sha256
from bson.objectid import ObjectId  # Import ObjectId for querying MongoDB
import re
from datetime import datetime, timedelta

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"
DATABASE_NAME = "WealthWise"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]
meetings_collection = db["appointments"]
advisors_collection = db["advisors"]
messages_collection = db["messages"]

@st.dialog("Confirm Delete")
def delete_account():
    st.write("Are you sure you want to delete your account? This action is permanent.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Delete", type="primary", use_container_width=True):
            users_collection.delete_one({"_id": ObjectId(st.session_state.user_id)})
            st.success("Your account has been deleted.")
            st.session_state.clear()
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

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
    st.title("User Management", anchor=False)
    
    # Create tabs
    tabs = st.tabs([
        "Payment & Subscription",
        "View Events/Meetings",
        "View Info & Delete Account"
    ])

    # Tab 1: Payment & Subscription
    with tabs[0]:
        st.header("Payment & Subscription", anchor=False)
        st.write("Update your payment method and manage your subscription.")

        if "user_id" not in st.session_state:
            st.error("You must be logged in to manage your subscription.")
            st.stop()

        user_id = ObjectId(st.session_state.user_id)
        user = users_collection.find_one({"_id": user_id})

        # Handle expired Elite subscriptions
        if user.get("subscription") == "Elite" and user.get("subscription_end"):
            try:
                subscription_end = datetime.strptime(user["subscription_end"], "%Y-%m-%d")
                if subscription_end < datetime.now():
                    users_collection.update_one(
                        {"_id": user_id},
                        {"$set": {"subscription": "Basic"},
                        "$unset": {"subscription_start": "", "subscription_end": ""}}
                    )
                    st.warning("Your Elite subscription has expired and you have been downgraded to the Basic plan.")
                    st.rerun()
            except ValueError:
                st.error("Error parsing subscription end date.")

        current_plan = user.get("subscription", "Basic")
        subscription_end = user.get("subscription_end")

        st.subheader("Current Plan", anchor=False)
        st.write(f"You are currently subscribed to the **{current_plan}** plan.")

        # Show subscription expiration date for Elite users
        if current_plan == "Elite":
            if subscription_end:
                end_date = datetime.strptime(subscription_end, "%Y-%m-%d")
                st.success(f"Elite subscription valid until **{end_date.strftime('%B %d, %Y')}**.")
            else:
                st.warning("Elite subscription is active, but no expiration date is set.")
        else:
            st.info("Upgrade to Elite for $100/year to unlock all features.")

            st.subheader("Upgrade to Elite", anchor=False)
            if st.button("Upgrade Now for $100/year"):
                today = datetime.now()
                end_date = today + timedelta(days=365)

                users_collection.update_one(
                    {"_id": user_id},
                    {"$set": {
                        "subscription": "Elite",
                        "subscription_start": today.strftime("%Y-%m-%d"),
                        "subscription_end": end_date.strftime("%Y-%m-%d")
                    }}
                )
                st.success(f"Subscription upgraded to Elite! Valid until {end_date.strftime('%B %d, %Y')}.")
                st.rerun()     

    # Tab 2: View Events/Meetings
    with tabs[1]:
        meetings = []

        if "user_id" not in st.session_state:
            st.error("You must be logged in to view your meetings.")
            st.stop()

        user_id = st.session_state.user_id
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if (user.get("subscription") == "Basic"):
            st.error("Only Elite users can schedule meetings.")

        else:
            # Fetch all meetings for the user
            meetings = list(meetings_collection.find({"customerId": user_id}))

        # Prepare lists
        past_meetings = []
        future_meetings = []

        # Current datetime
        current_datetime = datetime.now()

        # Classify meetings
        for meeting in meetings:
            scheduled_datetime = meeting["scheduled_at"]

            if scheduled_datetime < current_datetime:
                past_meetings.append(meeting)
            else:
                future_meetings.append(meeting)

        # Create two columns
        col1, col2 = st.columns(2, border=True)

        # Future Meetings (left)
        with col1:
            st.subheader("Future Meetings", anchor=False)
            if future_meetings:
                for meeting in future_meetings:
                    advisor = users_collection.find_one({"_id": ObjectId(meeting["advisorId"])})
                    advisor_name = f"{advisor['first_name']} {advisor['last_name']}" if advisor else "Unknown Advisor"
                    meeting_time = meeting["scheduled_at"].strftime("%B %d, %Y at %I:%M %p")
                    st.write(f"**{advisor_name}**: {meeting_time}")
            else:
                st.write("No upcoming meetings.")

        # Past Meetings (right)
        with col2:
            st.subheader("Past Meetings", anchor=False)
            if past_meetings:
                for meeting in past_meetings:
                    advisor = users_collection.find_one({"_id": ObjectId(meeting["advisorId"])})
                    advisor_name = f"{advisor['first_name']} {advisor['last_name']}" if advisor else "Unknown Advisor"
                    meeting_time = meeting["scheduled_at"].strftime("%B %d, %Y at %I:%M %p")
                    st.write(f"**{advisor_name}**: {meeting_time}")
            else:
                st.write("No past meetings.") 

    # Tab 3: View Info & Delete Account
    with tabs[2]:
        st.header("Account Info", anchor=False)
        if (st.session_state.password_verified == False):
            st.write("To view or edit your sensitive information, please re-enter your password.")

        if "user_id" not in st.session_state:
            st.error("You must be logged in to view this page.")
            st.stop()

        if "password_verified" not in st.session_state:
            st.session_state.password_verified = False

        if not st.session_state.password_verified:
            password = st.text_input("Enter your password", type="password")
            if st.button("Verify Password"):
                hashed_password = sha256(password.encode()).hexdigest()
                try:
                    user = users_collection.find_one({"_id": ObjectId(st.session_state.user_id)})
                except Exception as e:
                    st.error("Invalid user ID format.")
                    return

                if user and hashed_password == user["password"]:
                    st.success("Password verified!")
                    st.session_state.password_verified = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")
        else:
            try:
                user = users_collection.find_one({"_id": ObjectId(st.session_state.user_id)})
            except Exception as e:
                st.error("Invalid user ID format.")
                return

            if not user:
                st.error("User not found.")
                return

            st.write(f"**First Name:** {user.get('first_name', 'N/A')}")
            st.write(f"**Last Name:** {user.get('last_name', 'N/A')}")
            st.write(f"**Email:** {user.get('email', 'N/A')}")

            st.write("---")
            st.subheader("Edit Information")

            with st.form("edit_account_form"):
                new_first_name = st.text_input("New First Name", value="")
                new_last_name = st.text_input("New Last Name", value="")
                new_email = st.text_input("New Email", value="")
                new_password = st.text_input("New Password", type="password")
                password_confirm = st.text_input("Confirm New Password", type="password")
                submitted = st.form_submit_button("Save Changes")

                if submitted:
                    updates = {}

                    if new_first_name.strip():
                        updates["first_name"] = new_first_name.strip()
                    if new_last_name.strip():
                        updates["last_name"] = new_last_name.strip()
                    if new_email.strip():
                        if "@" not in new_email:
                            st.error("Invalid email address.")
                            st.stop()
                        updates["email"] = new_email.strip()
                    if new_password.strip():
                        if new_password != password_confirm:
                            st.error("Passwords do not match.")
                            st.stop()
                        elif not check_password(new_password):
                            st.error("Invalid password.")
                            st.stop()
                        else:
                            updates["password"] = sha256(new_password.encode()).hexdigest()

                    if updates:
                        users_collection.update_one(
                            {"_id": ObjectId(st.session_state.user_id)},
                            {"$set": updates}
                        )
                        st.success("Changes saved successfully!")
                        st.rerun()
                    else:
                        st.warning("No changes to save.")

            st.write("---")
            st.subheader("Danger Zone")
            if st.button("Delete Account", type="primary"):
                delete_account()