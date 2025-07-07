import pandas as pd

# Read the sp500.csv file
sp500_df = pd.read_csv("sp500_asc_date.csv")

# Read the .csv file
treasury_bill_df = pd.read_csv("treasury_bill.csv")

agg_df = pd.read_csv("agg_asc_date.csv")

acwx_df = pd.read_csv("acwx_asc_date.csv")

# Merge the DataFrames on the 'date' column
merged_df = pd.merge(sp500_df, treasury_bill_df, on='full_date')
merged_df = pd.merge(merged_df, agg_df, on='full_date')
merged_df = pd.merge(merged_df, acwx_df, on='full_date')

# Rename the columns
merged_df.columns = ['date', 'year', 'month', 'sp500_monthly_price', 'treasury_bill_rate', 'agg_monthly_price', 'acwx_monthly_price']

# Write the merged DataFrame to a new CSV file
merged_df.to_csv("merged_data.csv", index=False)
