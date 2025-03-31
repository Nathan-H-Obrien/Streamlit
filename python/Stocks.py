import os
import streamlit as st
import pandas as pd
from polygon import RESTClient


def stock_page():
    st.title("Stocks")

    # Set up the API key
    api_key = "ZgFptzp39IOpFdfDnnpJUarLO9rN9jQ2"
    if not api_key:
        st.error("API key not found. Please set the POLYGON_API_KEY environment variable.")
        return
    
    symbol = st.text_input("Enter a stock symbol")
    if not symbol:
        st.info("Enter a stock symbol to get started")
        return
    # Create a REST client
    client = RESTClient(api_key)

    col1, col2, col3 = st.columns(3)

    if col1.button("Company Profile"):
        company = client.stocks_equities(symbol)
        st.write(company)

    if col2.button("Daily Open/Close"):
        open_close = client.stocks_equities_aggregates(symbol, 1, "day", "2021-01-01", "2021-01-05")
        st.write(open_close)

    if col3.button("Last Trade"):
        last_trade = client.stocks_equities_last_trade(symbol)
        st.write(last_trade)
    
