import pandas as pd

file_name = "acwx_asc.csv"
new_file_name = "acwx_asc_date.csv"

# Read the file
df = pd.read_csv(file_name)

# Convert 'date' column to a common date format for sp500_df
df['full_date'] = pd.to_datetime(df['full_date'], format="%Y/%m/%d")

df.to_csv(new_file_name, index=False)