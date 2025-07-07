import pandas as pd

# Read the truncated_treasury_bill.csv file
df = pd.read_csv("merged_data_cleaned.csv")

# Calculate the excess return: (sp500_monthly_price - sp500_monthly_price 12 months ago)
df['sp500_excess_return'] = (df['sp500_monthly_price'].pct_change(periods=12) * 100).round(2)

# Drop the rows with NaN values (due to the shift operation)
df.dropna(inplace=True)

# Save the cleaned DataFrame to a new CSV file
df.to_csv("excess_return.csv", index=False)
