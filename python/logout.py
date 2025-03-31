import streamlit as st
def logout_page():
    st.session_state.logged_in = False
    st.title("Logout")
    st.write("You have successfully logged out.")
    st.write("Thank you for using our application!")
    st.write("We hope to see you again soon.")
    # Add a button to go back to the login page
    
    
    if st.button("Back to Login"):
        # Redirect to the login page
        st.session_state.page_selection = "Login"
        st.experimental_rerun() 