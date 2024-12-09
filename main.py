import streamlit as st
from Home import home_page
from calculator import calculator_page
import time

def logo_screen():
    # Initialize session state
    if 'startup_displayed' not in st.session_state:
        st.session_state.startup_displayed = False

    # Inject custom CSS
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
            top: 75px;
            left: 10px;
            width: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display the mainscreen image for 5 seconds if not already displayed
    if not st.session_state.startup_displayed:
        mainscreen_url = 'https://raw.githubusercontent.com/Nathan-H-Obrien/Streamlit/main/mainscreen.png'
        mainscreen_placeholder = st.empty()
        with mainscreen_placeholder.container():
            st.markdown(f'<div class="centered-image"><img src="{mainscreen_url}" style="width: 100%; max-width: 800px;"></div>', unsafe_allow_html=True)
        time.sleep(5)
        mainscreen_placeholder.empty()
        st.session_state.startup_displayed = True

        # Display the logo image in the top left corner
        logo_url = 'https://raw.githubusercontent.com/Nathan-H-Obrien/Streamlit/main/Logo.jpg'
        st.markdown(f'<img src="{logo_url}" class="logo">', unsafe_allow_html=True)

logo_screen()
# Define the pages
PAGES = {
    "🏠 Home": home_page,
    "🧮 Calculator": calculator_page
}

st.sidebar.title('What can we help you with today?')

# Create a button for each page
selection = None
for page_name, page_func in PAGES.items():
    if st.sidebar.button(page_name):
        selection = page_name

# Default to the first page if no button has been pressed
if selection is None:
    selection = list(PAGES.keys())[0]

# Display the selected page
page = PAGES[selection]
page()