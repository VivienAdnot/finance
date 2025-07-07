import pandas as pd
import matplotlib.pyplot as plt

def calculate_percentage_change(initial_value, final_value):
    """
    Calculates the percentage change between two values.

    Parameters:
        value1 (float): The initial value.
        value2 (float): The final value.

    Returns:
        float: The percentage change between value1 and value2.
    """
    percentage_change = round(((final_value - initial_value) / initial_value) * 100)
    return percentage_change

def calculate_cumulative_percentage(initial_value, final_value, cumulative_result):
  """
  Calculates the cumulative percentage change between two values.

  Parameters:
      initial_value (float): The initial value.
      final_value (float): The final value.
      cumulative_result (float): The cumulative result.


  Returns:
      float: The cumulative percentage change between value1 and value2.
  """
  percentage_change = ((final_value - initial_value) / initial_value) * 100
  cumulative_result += percentage_change
  return cumulative_result

def compute_annual_returns(df):
  # Resample the data to annual frequency and get the first and last prices of each year
  annual_returns = df['sp500_monthly_price'].resample('Y').ohlc()

  # Calculate the annual return as the percentage change over 12 months
  annual_returns['annual_return'] = calculate_percentage_change(annual_returns['open'], annual_returns['close'])
  return annual_returns

def extract_annual_results(df):
  # Extract the year from the index and create a new column 'year'
  df['year'] = df.index.year

  # Drop the 'date' index and convert it back to a regular column
  # result_df = df.reset_index(drop=False)

  # Display only the 'year' and 'annual_return' columns
  result_df = df[['year', 'annual_return']]
  return result_df

def display_results(df):
  # Drop the 'date' index and convert it back to a regular column
  result_df = df.reset_index(drop=False)
  
  # Convert the DataFrame to a string without printing the index column
  result_string = result_df.to_string(index=False)

  # Print the result DataFrame
  print(result_string)

def compute_cumulative_results(df):
  # Calculate cumulative return
  df['cumulative_return'] = df['annual_return'].cumsum().fillna(0)
  return df

def plot_cumulative_returns(df):
  # Plot the cumulative return over time
  plt.figure(figsize=(10, 6))
  plt.plot(df.index, df['cumulative_return'], marker='o', linestyle='-')
  plt.xlabel('Date')
  plt.ylabel('Cumulative Return')
  plt.title('Cumulative Return Over Time')
  plt.grid(True)
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.show()

def main():
  # Read in the data
  df = pd.read_csv('excess_return.csv', parse_dates=['date'], index_col='date')
  
  # Use compute_annual_returns on the dataframe
  annual_returns = compute_annual_returns(df)

  extracted_annual_results = extract_annual_results(annual_returns)
  # # Write the merged DataFrame to a new CSV file
  annual_returns.to_csv("annual_returns.csv")

  # display_results(extracted_annual_results)

  # cumulative_results = compute_cumulative_results(annual_returns)
  # plot_cumulative_returns(cumulative_results)

if __name__ == '__main__':
  main()