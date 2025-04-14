import streamlit as st
from login import login_page
from Home import home_page
from calculator import calculator_page
from meetings import meetings_page
from user_management import user_management_page
from Stocks import stock_page
from advisor import advisor_management_page
from admin import admin_management_page

# Set page configuration
st.set_page_config(
    page_title="WealthWise Financial",
    page_icon="pictures/Logo.jpg",  # Use the local image
    layout="wide"
)

def main_page():
    # Define the pages
    PAGES = {
        "🏠 Home": home_page,
        "🧮 Calculator": calculator_page,
        "💻 Meetings": meetings_page,
        "📈 Stocks": stock_page,
    }
    if st.session_state.subscription_type in ["Basic", "Elite"]:
        PAGES["👤 User Management"] = user_management_page
    if st.session_state.subscription_type == "Advisor":
        PAGES["👤 Advisor Management"] = advisor_management_page
    if st.session_state.subscription_type == "Admin":
        PAGES["👤 Admin Management"] = admin_management_page

    st.sidebar.title('What can we help you with today?', anchor=False)

    if st.session_state.logged_in == True:
        # Initialize session state for page selection
        if 'page_selection' not in st.session_state:
            st.session_state.page_selection = list(PAGES.keys())[0]

        # Create a button for each page
        for page_name in PAGES.keys():
            if st.sidebar.button(page_name):
                st.session_state.page_selection = page_name

        # Separator line
        st.sidebar.markdown("""---""")

        # Empty space placeholder for alignment
        bottom_placeholder = st.sidebar.empty()

        # Logout button at the bottom
        if bottom_placeholder.button("🔒 Logout"):
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
