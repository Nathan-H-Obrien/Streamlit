import streamlit as st
import time
from news import news_section

def home_page():
    st.session_state.password_verified = False
    st.title('WealthWise Financial')

    st.write('Welcome to WealthWise Financial! We help you make better financial decisions.')
    news_section()
