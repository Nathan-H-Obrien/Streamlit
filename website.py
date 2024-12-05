import streamlit as st

st.title('WealthWise Financials')
st.write('Loan Calculator')

# Loan Amount
loan_amount = st.number_input('Loan Amount', min_value=0, value=1000, step=100)
# Interest Rate
interest_rate = st.number_input('Interest Rate (%)', min_value=0.0, value=5.0, step=0.1)

# Loan Term (Years)
loan_term_years = st.number_input('Loan Term (Years)', min_value=1, value=1, step=1)

# Calculate Monthly Payment
if st.button('Calculate'):
    monthly_interest_rate = interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    if interest_rate == 0:
        monthly_payment = loan_amount / number_of_payments
    else:
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    
    st.write(f'Monthly Payment: ${monthly_payment:.2f}')
