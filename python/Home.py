import streamlit as st
import time
from news import news_section

def home_page():
    st.title('WealthWise Financial')

    st.write('Welcome to WealthWise Financials! We help you make better financial decisions.')
    news_section()
