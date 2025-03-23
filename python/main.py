import streamlit as st
from login import login_page
from Home import home_page
from calculator import calculator_page
from advisorMeeting import meeting_page
import time

# Set page configuration
st.set_page_config(
    page_title="WealthWise Financials",
    page_icon="pictures/Logo.jpg",  # Use the local image
    layout="wide"
)

# Inject custom CSS for the logo and background
st.markdown(
    """
    <style>
    body {
        background-color: #0e2537;
        color: #ceaa61;
        font-family: 'Times New Roman', Times, serif;
    }
    .centered-image {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .logo {
        position: fixed;
        top: 75px;  /* Adjust this value to move the logo down */
        right: 10px;  /* Position the logo in the top right corner */
        width: 100px;
        z-index: 1000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the logo image in the top right corner
logo_url = 'pictures/Logo.jpg'
st.markdown(f'<img src="{logo_url}" class="logo">', unsafe_allow_html=True)

def logo_screen():
    # Initialize session state
    if 'startup_displayed' not in st.session_state:
        st.session_state.startup_displayed = False

    # Display the mainscreen image for 5 seconds if not already displayed
    if not st.session_state.startup_displayed:
        mainscreen_url = 'pictures/mainscreen.png'  # Use the local image
        mainscreen_placeholder = st.empty()
        with mainscreen_placeholder.container():
            st.markdown(f'<div class="centered-image"><img src="{mainscreen_url}" style="width: 100%; max-width: 800px;"></div>', unsafe_allow_html=True)
        time.sleep(5)
        mainscreen_placeholder.empty()
        st.session_state.startup_displayed = True

def main_page():
    # Define the pages
    PAGES = {
        "🏠 Home": home_page,
        "🧮 Calculator": calculator_page,
        "💻 Advisor Info": meeting_page
    }

    st.sidebar.title('What can we help you with today?')

    # Initialize session state for page selection
    if 'page_selection' not in st.session_state:
        st.session_state.page_selection = list(PAGES.keys())[0]

    # Create a button for each page
    for page_name in PAGES.keys():
        if st.sidebar.button(page_name):
            st.session_state.page_selection = page_name

    # Display the selected page
    page = PAGES[st.session_state.page_selection]
    page()

# Display the splash screen
logo_screen()

# Check if the user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Display the login page if the user is not logged in
if not st.session_state.logged_in:
    login_page()
else:
    main_page()