import pandas as pd

# Read the .csv file
treasury_bill_df = pd.read_csv("DTB3.csv")

# Filter the DataFrame based on the date range
treasury_bill_df = treasury_bill_df[treasury_bill_df['full_date'] >= '1970-01-01']

# Save the truncated DataFrame to a new CSV file
treasury_bill_df.to_csv("treasury_bill.csv", index=False)
