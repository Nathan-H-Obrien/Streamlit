from bson import ObjectId
from pymongo import MongoClient
import streamlit as st
from login import login_page
from Home import home_page
from calculator import calculator_page
from meetings import meetings_page
from user_management import user_management_page
from advisor import advisor_management_page
from admin import admin_management_page
from chat import chat_page
from portfolio import portfolio_page

# Set page configuration
st.set_page_config(
    page_title="WealthWise Financial",
    page_icon="pictures/Logo.jpg",
    layout="wide"
)

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"
DATABASE_NAME = "WealthWise"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]  # Collection for storing user credentials

def main_page():
    user = users_collection.find_one({"_id": ObjectId(st.session_state.user_id)})
    
    # Define the pages
    PAGES = {
        "🏠 Home": home_page,
        "🧮 Calculators": calculator_page,
    }
    if st.session_state.subscription_type in ["Basic", "Elite"]:
        PAGES["📈 Manage Portfolio"] = portfolio_page
        PAGES["💻 Meetings"] = meetings_page
        PAGES["💬 Chat with Advisor"] = chat_page
        PAGES["👤 User Management"] = user_management_page
    if st.session_state.subscription_type == "Advisor":
        PAGES["👤 Advisor Management"] = advisor_management_page
    if st.session_state.subscription_type == "Admin":
        PAGES["👤 Admin Management"] = admin_management_page

    st.sidebar.title(f"Hello {user["first_name"]}!")
    st.sidebar.title('What can we help you with today?', anchor=False)

    if st.session_state.logged_in == True:
        # Initialize session state for page selection
        if 'page_selection' not in st.session_state:
            st.session_state.page_selection = list(PAGES.keys())[0]

        # Create a button for each page
        for page_name in PAGES.keys():
            if st.sidebar.button(page_name, use_container_width=True):
                st.session_state.page_selection = page_name

        # Separator line
        st.sidebar.markdown("""---""")

        # Empty space placeholder for alignment
        bottom_placeholder = st.sidebar.empty()

        # Logout button at the bottom
        if bottom_placeholder.button("🔒 Logout", use_container_width=True):
            logout_page()

    # Display the selected page
        page = PAGES[st.session_state.page_selection]
        page()

def logout_page():
    st.session_state.logged_in = False
    st.session_state.page_selection = "Login"
    st.rerun() 

# Check if the user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Display the login page if the user is not logged in
if not st.session_state.logged_in:
    login_page()
else:
    main_page()
