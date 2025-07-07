def calculate_percentage_change(initial_value, final_value):
    """
    Calculates the percentage change between two values.

    Parameters:
        value1 (float): The initial value.
        value2 (float): The final value.

    Returns:
        float: The percentage change between value1 and value2.
    """
    percentage_change = ((final_value - initial_value) / initial_value) * 100
    return percentage_change

# Example usage
initial_value = 99
final_value = 115

percentage_change = calculate_percentage_change(initial_value, final_value)
print(f"The percentage change is: {percentage_change:.2f}%")
