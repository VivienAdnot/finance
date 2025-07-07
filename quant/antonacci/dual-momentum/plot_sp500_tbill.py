import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('excess_return.csv')

# Plot the data

#initialize the plot
plt.figure(figsize=(10, 6))
plt.title('Percentage Excess Return and Treasury Bill Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Percentage')

# parameters for the plot
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# plot the data
# Convert the 'date' column to a datetime format
df['date'] = pd.to_datetime(df['date'])
plt.plot(df['date'], df['sp500_excess_return'], color='blue', label='SP500 Percentage Excess Return')
plt.plot(df['date'], df['treasury_bill_rate'], color='red', label='Treasury Bill Rate')
plt.show()
