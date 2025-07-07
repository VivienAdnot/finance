import yfinance as yf

# Fetch long-term data for Gold and US 10-Year Treasury Bond Yield
tickers = ['GC=F', '^TNX']  # Gold futures and US 10-Year Treasury Yield
gold_data = yf.download('GC=F', start="1972-11-01", end="2024-12-31", interval="1mo")['Adj Close']
bond_yield_data = yf.download('^TNX', start="1972-11-01", end="2024-12-31", interval="1mo")['Adj Close']

# Display the first few rows of the data to check availability
print("Gold Data (Head):")
print(gold_data.head())
print("\n10-Year Treasury Yield Data (Head):")
print(bond_yield_data.head())

print("\nGold Data (Tail):")
print(gold_data.tail())
print("\n10-Year Treasury Yield Data (Tail):")
print(bond_yield_data.tail())
