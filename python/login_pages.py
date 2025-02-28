import streamlit as st
import sqlite3
from login import login_page
from new_user import new_userPage
import re

def login_screens():
    PAGES = {
        "Login": login_page,
        "New User Registration": new_userPage
    }

    st.sidebar.title('Please sign in or register to continue')

    if 'page_selection' not in st.session_state:
        st.session_state.page_selection = list(PAGES.keys())[0]

    for page_name in PAGES.keys():
        if st.sidebar.button(page_name):
            st.session_state.page_selection = page_name

    page = PAGES[st.session_state.page_selection]
    page()