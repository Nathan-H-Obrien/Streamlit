import streamlit as st
from Home import home_page
from calculator import calculator_page

def main_page():
    # Define the pages
    PAGES = {
        "🏠 Home": home_page,
        "🧮 Calculator": calculator_page
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