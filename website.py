import streamlit as st

home_tab, calculator_tab = st.tabs(['Home', 'Calculator'])
with home_tab:
    st.title('WealthWise Financials')
    st.write('Welcome to WealthWise Financials! We help you make better financial decisions.')
with calculator_tab:
    st.title('WealthWise Financial Calculators')
    st.write('Use our calculators to make better financial decisions.')
    st.write('Select a calculator from the dropdown menu below.')
    loan_calculator, investment_calculator = st.tabs(['Loan Calculator', 'Investment Calculator'])
    with loan_calculator:
        st.write('Loan Calculator')
        # Loan Amount
        loan_amount = st.number_input('Loan Amount', min_value=0, value=1000, step=100)
        # Interest Rate
        interest_rate = st.number_input('Interest Rate (%)', min_value=0.0, value=5.0, step=0.1)

        # Loan Term (Months)
        loan_term_months = st.number_input('Loan Term (Months)', min_value=1, value=12, step=1)

        # Calculate Monthly Payment
        if st.button('Calculate Loan Payment'):
            monthly_interest_rate = interest_rate / 100 / 12
            if interest_rate == 0:
                monthly_payment = loan_amount / loan_term_months
            else:
                monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
            
            st.write(f'Monthly Payment: ${monthly_payment:.2f}')
    
    with investment_calculator:
        st.write('Investment Calculator')
        # Investment Amount
        investment_amount = st.number_input('Investment Amount', min_value=0, value=1000, step=100)
        # Interest Rate
        interest_rate2 = st.number_input('Interest Rate (%)', min_value=0.0, value=5.0, step=0.1)

        # Investment Term (Years)
        investment_term_years = st.number_input('Investment Term (Years)', min_value=1, value=1, step=1)

        # Calculate Future Value
        if st.button('Calculate Future Value'):
            future_value = investment_amount * (1 + interest_rate2 / 100) ** investment_term_years
            st.write(f'Future Value: ${future_value:.2f}')