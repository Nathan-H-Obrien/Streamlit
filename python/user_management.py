import streamlit as st
from pymongo import MongoClient
from hashlib import sha256
from bson.objectid import ObjectId  # Import ObjectId for querying MongoDB
import re
import yfinance as yf
from datetime import datetime, timedelta

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"
DATABASE_NAME = "WealthWise"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]
portfolios_collection = db["portfolios"]
meetings_collection = db["appointments"]
advisors_collection = db["advisors"]
messages_collection = db["messages"]

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
        "Chat with Advisor", 
        "Manage Portfolio", 
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

    # Tab 2 Chat with Advisor
    with tabs[1]:
        st.header("Chat with Advisor", anchor=False)
        st.write("Start a conversation with your advisor.")

        if "user_id" not in st.session_state:
            st.error("You must be logged in to chat with your advisor.")
            st.stop()

        user_id = st.session_state.user_id

        # Get advisor list (only Advisor subscription type)
        advisors = list(users_collection.find({"subscription": "Advisor"}))
        if not advisors:
            st.warning("No advisors available right now.")
        else:
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



    # Tab 3: Manage Portfolio
    with tabs[2]:
        st.header("Manage Portfolio", anchor=False)
        
        if "user_id" not in st.session_state:
            st.error("You must be logged in to manage your portfolio.")
            st.stop()

        user_id = ObjectId(st.session_state.user_id)

        # Fetch or initialize portfolio
        portfolio = portfolios_collection.find_one({"user_id": user_id})
        if not portfolio:
            portfolios_collection.insert_one({"user_id": user_id, "holdings": {}})
            portfolio = {"holdings": {}}

        holdings = portfolio.get("holdings", {})

        # Helper function to get live price
        def get_live_price(ticker):
            try:
                stock = yf.Ticker(ticker)
                live_price = stock.history(period='1d')['Close'].iloc[-1]
                return live_price
            except:
                return None

        # Display current holdings with live prices
        st.subheader("Current Holdings", anchor=False)
        if holdings:
            for stock, qty in holdings.items():
                live_price = get_live_price(stock)
                if live_price:
                    total_value = qty * live_price
                    st.write(f"**{stock}**: {qty} shares @ \${live_price:.2f} (Total: \${total_value:.2f})")
                else:
                    st.write(f"**{stock}**: {qty} shares (Live price unavailable)")
        else:
            st.write("You don't have any holdings yet.")

        # Form to add/remove stocks
        st.subheader("Update Holdings", anchor=False)
        with st.form("update_portfolio"):
            stock_symbol = st.text_input("Stock Symbol (e.g., AAPL)").upper().strip()
            quantity = st.number_input("Quantity", min_value=0.0, step=0.01, format="%.2f", placeholder=0.0)
            action = st.radio("Action", ["Add", "Remove"])
            submit = st.form_submit_button("Update Portfolio")

            if submit:
                if not stock_symbol:
                    st.error("Stock symbol cannot be empty.")
                else:
                    updated_qty = holdings.get(stock_symbol, 0)
                    if action == "Add":
                        updated_qty += quantity
                    elif action == "Remove":
                        if quantity > updated_qty:
                            st.error(f"You only own {updated_qty} shares of {stock_symbol}. Cannot remove more.")
                            st.stop()
                        updated_qty -= quantity

                    if updated_qty > 0:
                        holdings[stock_symbol] = updated_qty
                    elif stock_symbol in holdings:
                        del holdings[stock_symbol]

                    portfolios_collection.update_one(
                        {"user_id": user_id},
                        {"$set": {"holdings": holdings}}
                    )
                    st.success(f"Portfolio updated! {stock_symbol}: {updated_qty} shares")
                    st.rerun()


    # Tab 4: View Events/Meetings
    with tabs[3]:
        if "user_id" not in st.session_state:
            st.error("You must be logged in to view your meetings.")
            st.stop()

        user_id = st.session_state.user_id

        # Fetch all meetings for the user
        meetings = list(meetings_collection.find({"customerId": user_id}))

        if not meetings:
            st.write("You have no scheduled meetings.")
            return

        # Get current date to compare with meeting dates
        current_date = datetime.now()

        # Separate meetings into past and future

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


    # Tab 5: View Info & Delete Account
    with tabs[4]:
        st.header("Account Info", anchor=False)
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