import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch monthly data starting in 2013 to calculate 2014 performance
tickers = ['^GSPC', 'GLD', 'BIL']  # S&P 500, Gold, and Treasury Bills proxy
data = yf.download(tickers, start="2013-01-01", end="2024-12-31", interval="1mo")['Adj Close']

# Calculate monthly returns
monthly_returns = data.pct_change().dropna()

# Define portfolio weights
weights = np.array([0.33, 0.33, 0.33])

# Calculate portfolio returns
portfolio_returns = monthly_returns.dot(weights)

# Calculate cumulative growth of $100 invested
START_MONEY = 100
cumulative_growth = (1 + portfolio_returns).cumprod() * START_MONEY

# Filter out data before 2014 for visualization
cumulative_growth_filtered = cumulative_growth[cumulative_growth.index >= "2014-01-01"]

# Calculate yearly returns
portfolio_df = pd.DataFrame({'Portfolio': cumulative_growth})
portfolio_df['Year'] = portfolio_df.index.year
yearly_returns = portfolio_df.groupby('Year').last().pct_change()['Portfolio'] * 100  # Convert to percentage

# Plot total portfolio cumulative growth
plt.figure(figsize=(12, 6))
plt.plot(cumulative_growth_filtered.index, cumulative_growth_filtered, label='Portfolio', linewidth=2, color='blue')

# Add background coloring for yearly performance (exclude 2013)
for year in yearly_returns.index:
    if year >= 2014:  # Skip 2013
        start_date = f'{year}-01-01'
        end_date = f'{year+1}-01-01'
        color = 'green' if yearly_returns[year] > 0 else 'red' if yearly_returns[year] < 0 else 'grey'
        plt.axvspan(pd.Timestamp(start_date), pd.Timestamp(end_date), color=color, alpha=0.1)
        
        # Annotate yearly performance
        mid_date = pd.Timestamp(start_date) + (pd.Timestamp(end_date) - pd.Timestamp(start_date)) / 2
        performance_text = f"{yearly_returns[year]:.2f}%"  # Format as percentage with 2 decimals
        plt.text(mid_date, cumulative_growth.max() * 0.9, performance_text,
                 horizontalalignment='center', fontsize=10, color=color, alpha=0.8)

# Set x-axis to display all years
all_years = pd.date_range(start="2014-01-01", end="2024-01-01", freq="YS")  # Year start
plt.xticks(all_years, [str(year.year) for year in all_years], rotation=45)

# Customize the plot
plt.title('Total Portfolio Cumulative Growth of $100 Invested Since 2014', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Portfolio Value ($)', fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
