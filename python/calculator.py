import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def calculator_page():
    st.session_state.password_verified = False
    """Displays the calculator page with options for Loan and Investment calculators."""
    st.title('Financial Calculator', anchor=False)

    # Dropdown to select the type of calculator
    calculator = st.selectbox('Choose a calculator:', ['Investment', 'Loan'])

    # Loan Calculator
    if calculator == 'Loan':
        st.header('Loan Calculator', anchor=False)

        # Input fields for loan details
        loan_amount = st.number_input('Loan Amount ($)', min_value=0.00, value=1000.00, step=100.00)
        interest_rate = st.number_input('Annual Interest Rate (%)', min_value=0.0, value=5.0, step=0.1)
        loan_term_months = st.number_input('Loan Term (Months)', min_value=1, value=12, step=1)
        additional_payment = st.number_input('Additional Monthly Payment ($)', min_value=0.00, value=0.00, step=10.00)

        # Calculate button
        if st.button('Calculate Loan Details'):
            # Calculate monthly interest rate
            monthly_interest_rate = interest_rate / 100 / 12

            # Calculate monthly payment
            if interest_rate == 0:
                monthly_payment = loan_amount / loan_term_months
            else:
                monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / \
                                  ((1 + monthly_interest_rate) ** loan_term_months - 1)

            # Initialize totals and data for the table and graph
            total_payment = 0
            total_interest = 0
            monthly_data = []
            remaining_balances = []  # For graph
            months = []  # For graph

            # Display loan details month by month
            for month in range(1, loan_term_months + 1):
                interest_paid = loan_amount * monthly_interest_rate
                principal_paid = monthly_payment - interest_paid + additional_payment
                loan_amount -= principal_paid

                # Prevent negative loan balance
                if loan_amount < 0:
                    loan_amount = 0

                total_payment += monthly_payment + additional_payment
                total_interest += interest_paid

                # Store data for the table
                monthly_data.append({
                    "Month": month,
                    "Interest Paid ($)": round(interest_paid, 2),
                    "Principal Paid ($)": round(principal_paid, 2),
                    "Remaining Loan ($)": round(loan_amount, 2)
                })

                # Store data for the graph
                remaining_balances.append(round(loan_amount, 2))
                months.append(month)

                # Stop if the loan is fully paid
                if loan_amount == 0:
                    break

            # Convert monthly data to a DataFrame
            df = pd.DataFrame(monthly_data)

            # Display the table in a scrollable format
            st.subheader('Payment Breakdown', anchor=False)
            st.dataframe(df, height=400)

            # Display total payment and interest
            st.subheader('Summary', anchor=False)
            st.write(f"**Total Payment:** ${total_payment:.2f}")
            st.write(f"**Total Interest Paid:** ${total_interest:.2f}")

            # Plot the graph for remaining loan balance
            st.subheader('Remaining Loan Balance Over Time', anchor=False)
            plt.figure(figsize=(10, 5))
            plt.plot(months, remaining_balances, marker='o', linestyle='-', color='r')
            plt.title('Remaining Loan Balance Over Time')
            plt.xlabel('Month')
            plt.ylabel('Remaining Loan ($)')
            plt.grid(True)
            st.pyplot(plt)

    # Investment Calculator
    elif calculator == 'Investment':
        st.header('Investment Calculator', anchor=False)

        # Input fields for investment details
        investment_amount = st.number_input('Initial Investment Amount ($)', min_value=0, value=1000, step=100)
        interest_rate = st.number_input('Annual Interest Rate (%)', min_value=0.0, value=5.0, step=0.1)
        investment_term_years = st.number_input('Investment Term (Years)', min_value=1, value=1, step=1)
        additional_contribution = st.number_input('Annual Contribution ($)', min_value=0, value=0, step=100)

        # Calculate button
        if st.button('Calculate Future Value'):
            # Initialize total investment and data for the table and graph
            total_investment = investment_amount
            yearly_data = []
            yearly_interest = []
            years = []

            # Display investment details year by year
            for year in range(1, investment_term_years + 1):
                total_investment += additional_contribution
                interest_earned = total_investment * (interest_rate / 100)
                total_investment += interest_earned

                # Store data for the table and graph
                yearly_data.append({
                    "Year": year,
                    "Starting Amount ($)": round(total_investment - interest_earned, 2),
                    "Interest Earned ($)": round(interest_earned, 2),
                    "Total Value ($)": round(total_investment, 2)
                })
                yearly_interest.append(interest_earned)
                years.append(year)

            # Convert yearly data to a DataFrame
            df = pd.DataFrame(yearly_data)

            # Display the table in a scrollable format
            st.subheader('Yearly Breakdown', anchor=False)
            st.dataframe(df, height=400)

            # Display final investment value
            st.subheader('Summary', anchor=False)
            st.write(f"**Total Value After {investment_term_years} Years:** ${total_investment:.2f}")

            # Plot the graph
            st.subheader('Interest Earned Over Time', anchor=False)
            plt.figure(figsize=(10, 5))
            plt.plot(years, yearly_interest, marker='o', linestyle='-', color='b')
            plt.title('Yearly Interest Earned')
            plt.xlabel('Year')
            plt.ylabel('Interest Earned ($)')
            plt.grid(True)
            st.pyplot(plt)