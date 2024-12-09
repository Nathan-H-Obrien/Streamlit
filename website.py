import streamlit as st
import time

# Inject custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #0e2537;
        color: #ceaa61;
        font-family: 'Times New Roman', Times, serif;
    }
    .logo {
        position: fixed;
        top: 10px;
        left: 10px;
        width: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the mainscreen image for 5 seconds
mainscreen_url = 'https://github.com/Nathan-H-Obrien/Streamlit/tree/main/mainscreen.jpg'
st.image(mainscreen_url, use_column_width=True)
time.sleep(5)

# Clear the mainscreen image
st.empty()

# Display the logo image in the top left corner
logo_url = 'https://github.com/Nathan-H-Obrien/Streamlit/tree/main/logo.jpg'
st.markdown(f'<img src="{logo_url}" class="logo">', unsafe_allow_html=True)

st.title('WealthWise Financials')
home_tab, calculator_tab = st.tabs(['Home', 'Calculator'])
with home_tab:
    st.write('Welcome to WealthWise Financials! We help you make better financial decisions.')
with calculator_tab:
    calculator = st.selectbox('Choose a calculator:', ['Investment', 'Loan'])
    
    if calculator == 'Loan':
        st.write('Loan Calculator')
        # Loan Amount
        loan_amount = st.number_input('Loan Amount', min_value=0.00, value=1000.00, step=100.00)
        # Interest Rate
        interest_rate = st.number_input('Interest Rate (%)', min_value=0.0, value=5.0, step=0.1)

        # Loan Term (Months)
        loan_term_months = st.number_input('Loan Term (Months)', min_value=1, value=12, step=1)

        # Calculate Monthly Payment
        if st.button('Calculate'):
            monthly_interest_rate = interest_rate / 100 / 12
            if interest_rate == 0:
                monthly_payment = loan_amount / loan_term_months
            else:
                monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
            
            total_payment = monthly_payment * loan_term_months
            total_interest = total_payment - loan_amount
            
            st.write(f'Monthly Payment: ${monthly_payment:.2f}')
            st.write(f'Total Interest Paid: ${total_interest:.2f}')
            
            for i in range(1, loan_term_months + 1):
                interest_paid = loan_amount * monthly_interest_rate
                principal_paid = monthly_payment - interest_paid
                loan_amount = loan_amount - principal_paid
                if loan_amount < 0:
                    loan_amount = 0
                st.write(f'Month {i}: Interest Paid: {interest_paid:.2f}, Principal Paid: {principal_paid:.2f}, Remaining Loan Amount: {loan_amount:.2f}')
    elif calculator == 'Investment':
        st.write('Investment Calculator')
        # Investment Amount
        investment_amount = st.number_input('Investment Amount', min_value=0, value=1000, step=100)
        # Interest Rate
        interest_rate = st.number_input('Interest Rate (%)', min_value=0.0, value=5.0, step=0.1)

        # Investment Term (Years)
        investment_term_years = st.number_input('Investment Term (Years)', min_value=1, value=1, step=1)

        # Calculate Future Value
        if st.button('Calculate Future Value'):
            for i in range(1, investment_term_years + 1):
                current_value = investment_amount * (1 + interest_rate / 100) ** i
                st.write(f'Year {i}: ${current_value:.2f}')