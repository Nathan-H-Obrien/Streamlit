import os
import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
def stock_page():
    st.session_state.password_verified = False
    st.title("Stocks")


    symbol = st.text_input("Enter a stock symbol (e.g., AAPL)")

    if not symbol:
        st.info("Enter a stock symbol to get started")
        return

    # Fetch the stock ticker object using yfinance
    ticker = yf.Ticker(symbol)

    col1, col2, col3 = st.columns(3)

    if col1.button("Company Profile"):
        try:
            # Get company info
            company_info = ticker.info
            
            # Format market cap with commas
            market_cap = company_info.get('marketCap', 'N/A')
            if market_cap != 'N/A':
                market_cap = f"{market_cap:,}"  # Adds commas for thousands, millions, etc.

            # Display important company details
            st.subheader(f"Company Profile for {symbol}")
            st.write(f"**Company Name**: {company_info.get('longName', 'N/A')}")
            st.write(f"**Sector**: {company_info.get('sector', 'N/A')}")
            st.write(f"**Industry**: {company_info.get('industry', 'N/A')}")
            st.write(f"**Market Cap**: {market_cap}")
            st.write(f"**P/E Ratio**: {company_info.get('trailingPE', 'N/A')}")
            st.write(f"**Dividend Yield**: {company_info.get('dividendYield', 'N/A')}")
            st.write(f"**Website**: {company_info.get('website', 'N/A')}")
            st.write(f"**Business Summary**: {company_info.get('longBusinessSummary', 'N/A')}")
            
            if company_info.get('address1') and company_info.get('city') and company_info.get('state'):
                st.write(f"**Address**: {company_info.get('address1')}, {company_info.get('city')}, {company_info.get('state')}")
            else:
                st.write("**Address**: N/A")

        except Exception as e:
            st.error(f"Error fetching company details: {e}")

    if col2.button("Daily Open/Close"):
        try:
            # Get today's and yesterday's date
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            today_str = today.strftime('%Y-%m-%d')
            yesterday_str = yesterday.strftime('%Y-%m-%d')

            # Try fetching today's data
            historical_data = ticker.history(period="1d", start=yesterday_str, end=today_str)
            
            if historical_data.empty:
                st.warning(f"No data available for {today_str}. The market may be closed. Fetching data for {yesterday_str}...")
                # Fetch previous day's data
                previous_day_data = ticker.history(period="1d", start=yesterday_str, end=yesterday_str)
                
                if previous_day_data.empty:
                    st.error(f"No data available for the previous day ({yesterday_str}).")
                else:
                    st.write(f"Open/Close for {yesterday_str}")
                    st.write(previous_day_data[['Open', 'Close']])
            else:
                # Display today's data (if available)
                st.write(f"Open/Close for {today_str}")
                st.write(historical_data[['Open', 'Close']])

        except Exception as e:
            st.error(f"Error fetching daily open/close data: {e}")

    if col3.button("Last Trade"):

        try:
            # Get the last trade price (most recent close price)
            last_trade = ticker.history(period="1d")['Close'].iloc[-1]  # The last close price as a proxy for the last trade
            st.write(f"Last Trade: ${last_trade:.2f}")
        except Exception as e:
            st.error(f"Error fetching last trade: {e}")

    # Trend Graph Section: Plotting historical data
    st.subheader("Market Trends (Historical Data)")

    # Fetch historical data (last 30 days as an example)
    historical_data = ticker.history(period="30d")  # You can adjust this to 1d, 5d, 1mo, 1y, etc.

    if not historical_data.empty:
        # Create a Plotly graph for better interactive visualization
        import plotly.graph_objects as go
        fig = go.Figure()

        # Add Open and Close price trend lines
        fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data['Open'], mode='lines', name='Open Price'))
        fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data['Close'], mode='lines', name='Close Price'))

        # Update layout for better aesthetics
        fig.update_layout(
            title=f"{symbol} Stock Price Trend (Last 30 Days)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_dark",
            hovermode="x unified"
        )

        # Display the graph
        st.plotly_chart(fig)

    else:
        st.warning("No historical data available for the selected symbol.")

    

