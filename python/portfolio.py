from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import MongoClient
import streamlit as st
import yfinance as yf

# MongoDB Connection
MONGO_URI = "mongodb+srv://sambuerck:addadd54@meanexample.uod5c.mongodb.net/"
DATABASE_NAME = "WealthWise"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]
portfolios_collection = db["portfolios"]


def portfolio_page():
    st.header("Manage Portfolio", anchor=False)
    
    if "user_id" not in st.session_state:
        st.error("You must be logged in to manage your portfolio.")
        st.stop()

    user_id = ObjectId(st.session_state.user_id)

    # Fetch or initialize portfolio
    portfolio = portfolios_collection.find_one({"user_id": user_id})
    if not portfolio:
        portfolios_collection.insert_one({"user_id": user_id, "holdings": {}})
        portfolio = {"holdings": {}}

    holdings = portfolio.get("holdings", {})

    # Helper function to get live price
    def get_live_price(ticker):
        try:
            stock = yf.Ticker(ticker)
            live_price = stock.history(period='1d')['Close'].iloc[-1]
            return live_price
        except:
            return None

    # Display current holdings with live prices
    st.subheader("Current Holdings", anchor=False)
    if holdings:
        for stock, qty in holdings.items():
            live_price = get_live_price(stock)
            if live_price:
                total_value = qty * live_price
                st.write(f"**{stock}**: {qty} shares @ \${live_price:.2f} (Total: \${total_value:.2f})")
            else:
                st.write(f"**{stock}**: {qty} shares (Live price unavailable)")
    else:
        st.write("You don't have any holdings yet.")

    # Form to add/remove stocks
    st.subheader("Update Holdings", anchor=False)
    with st.form("update_portfolio"):
        stock_symbol = st.text_input("Stock Symbol (e.g., AAPL)").upper().strip()
        quantity = st.number_input("Quantity", min_value=0.0, step=0.01, format="%.2f", placeholder=0.0)
        action = st.radio("Action", ["Add", "Remove"])
        submit = st.form_submit_button("Update Portfolio")

        if submit:
            if not stock_symbol:
                st.error("Stock symbol cannot be empty.")
            else:
                updated_qty = holdings.get(stock_symbol, 0)
                if action == "Add":
                    updated_qty += quantity
                elif action == "Remove":
                    if quantity > updated_qty:
                        st.error(f"You only own {updated_qty} shares of {stock_symbol}. Cannot remove more.")
                        st.stop()
                    updated_qty -= quantity

                if updated_qty > 0:
                    holdings[stock_symbol] = updated_qty
                elif stock_symbol in holdings:
                    del holdings[stock_symbol]

                portfolios_collection.update_one(
                    {"user_id": user_id},
                    {"$set": {"holdings": holdings}}
                )
                st.success(f"Portfolio updated! {stock_symbol}: {updated_qty} shares")
                st.rerun()
    st.write("---")

    st.subheader("Search Stocks", anchor=False)

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
            st.subheader(f"Company Profile for {symbol}", anchor=False)
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
    st.subheader("Market Trends (Historical Data)", anchor=False)

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

    




