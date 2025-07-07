import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch monthly data for Gold and US 10-Year Treasury Yield starting in 2000
gold_data = yf.download('GC=F', start="2000-01-01", end="2024-12-31", interval="1mo")['Adj Close']
bond_yield_data = yf.download('^TNX', start="2000-01-01", end="2024-12-31", interval="1mo")['Adj Close']

# Merge the data into a single DataFrame
data = pd.DataFrame({'Gold': gold_data, 'Bond_Yield': bond_yield_data}).dropna()

# Ensure Bond_Yield is expressed as a decimal (convert percentages to fractions)
data['Bond_Yield'] = data['Bond_Yield'] / 100

# Calculate the ratio: Gold / US 10-Year Treasury Yield
data['Ratio'] = data['Gold'] / data['Bond_Yield']

# Normalize the ratio to start at 100 in January 2000
data['Indexed_Ratio'] = (data['Ratio'] / data['Ratio'].iloc[0]) * 100

# Extract years for x-axis ticks
data['Year'] = data.index.year
years = data['Year'].unique()

# Plot the indexed ratio
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Indexed_Ratio'], label='Gold / US Bond Market (Base 100)', color='gold', linewidth=2)
plt.title('Gold to US Bond Market Ratio (Base 100, Starting Jan 2000)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Indexed Ratio (Base 100)', fontsize=12)
plt.grid(True)

# Set x-axis ticks to show all years
plt.xticks(ticks=[pd.Timestamp(f"{year}-01-01") for year in years], labels=years, rotation=45)

plt.legend()
plt.tight_layout()
plt.show()
