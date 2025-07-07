import pandas as pd

file_name = "acwx.csv"
reversed_file_name = "acwx_asc.csv"

# Read the file
df = pd.read_csv(file_name)

# Reverse the DataFrame
reversed_df = df.iloc[::-1].reset_index(drop=True)

reversed_df.to_csv(reversed_file_name, index=False)