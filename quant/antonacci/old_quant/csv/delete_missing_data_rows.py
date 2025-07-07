import pandas as pd

# Read the truncated_treasury_bill.csv file
merged_data = pd.read_csv("merged_data.csv")

# Delete rows with value "." in the 'treasury_bill_rate' column
merged_data = merged_data[merged_data['treasury_bill_rate'] != "."]

# Save the cleaned DataFrame to a new CSV file
merged_data.to_csv("merged_data_cleaned.csv", index=False)
