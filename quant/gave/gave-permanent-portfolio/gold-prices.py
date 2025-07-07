import yfinance as yf
import pandas as pd

# Fetch monthly gold price data for 2020
gold_data_2020 = yf.download('GC=F', start="2019-01-01", end="2020-12-31", interval="1mo")['Adj Close']

# Format the data for readability
gold_data_2020 = gold_data_2020.reset_index()
gold_data_2020.columns = ['Date', 'Gold Price (USD)']

# Print the data
print(gold_data_2020)
