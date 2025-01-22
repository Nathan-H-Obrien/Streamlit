import streamlit as st
from python.login import login_page
from python.navigation import main_page  # Import main_page from navigation.py
import time

# Set page configuration
st.set_page_config(
    page_title="WealthWise Financials",
    page_icon="https://raw.githubusercontent.com/Nathan-H-Obrien/Streamlit/main/Logo.jpg",
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
logo_url = 'https://raw.githubusercontent.com/Nathan-H-Obrien/Streamlit/main/Logo.jpg'
st.markdown(f'<img src="{logo_url}" class="logo">', unsafe_allow_html=True)

def logo_screen():
    # Initialize session state
    if 'startup_displayed' not in st.session_state:
        st.session_state.startup_displayed = False

    # Display the mainscreen image for 5 seconds if not already displayed
    if not st.session_state.startup_displayed:
        mainscreen_url = 'https://raw.githubusercontent.com/Nathan-H-Obrien/Streamlit/main/mainscreen.png'
        mainscreen_placeholder = st.empty()
        with mainscreen_placeholder.container():
            st.markdown(f'<div class="centered-image"><img src="{mainscreen_url}" style="width: 100%; max-width: 800px;"></div>', unsafe_allow_html=True)
        time.sleep(5)
        mainscreen_placeholder.empty()
        st.session_state.startup_displayed = True

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