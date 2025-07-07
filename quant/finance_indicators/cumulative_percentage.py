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

# Example usage
initial_value = 100
final_value = 115
cumulative_result = 0

cumulative_result = calculate_cumulative_percentage(initial_value, final_value, cumulative_result)
print(f"The cumulative percentage change is: {cumulative_result:.2f}%")

cumulative_result = calculate_cumulative_percentage(initial_value, final_value, cumulative_result)
print(f"The cumulative percentage change is: {cumulative_result:.2f}%")

cumulative_result = calculate_cumulative_percentage(initial_value, final_value, cumulative_result)
print(f"The cumulative percentage change is: {cumulative_result:.2f}%")