import streamlit as st
import maskpass as mp

def login_page():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username == 'admin' and password == mp.maskpass('admin'):
            st.success('Login successful')
            st.experimental_rerun()
        else:
            st.error('Login failed')
    