import streamlit as st

st.title('WealthWise Financials')
home_tab, calculator_tab = st.tabs(['Home', 'Calculator'])
with home_tab:
    st.write('Welcome to WealthWise Financials! We help you make better financial decisions.')
with calculator_tab:
    st.write('Loan Calculator')
    # Loan Amount
    loan_amount = st.number_input('Loan Amount', min_value=0, value=1000, step=100)
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
        
        st.write(f'Monthly Payment: ${monthly_payment:.2f}')