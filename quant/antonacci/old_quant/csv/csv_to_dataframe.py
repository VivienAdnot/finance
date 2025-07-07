import pandas as pd

sp500_data = pd.read_csv('sp500.csv')

# Set the 'full_date' column as the index
sp500_data.set_index('full_date', inplace=True)

# Print the row with the label '2023/03/01'
print(sp500_data.loc['2023/03/01'])