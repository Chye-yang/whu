import pandas as pd
import random

# Read the CSV file
input_file = "selected_columns.csv"
df = pd.read_csv(input_file)

# Get the number of rows in the original dataframe
original_row_count = len(df)

# Calculate how many rows need to be added to reach 10,000 rows
rows_to_add = 10000 - original_row_count

# Randomly sample rows to add
additional_rows = df.sample(n=rows_to_add, replace=True, random_state=1)

# Concatenate the original dataframe with the additional rows
expanded_df = pd.concat([df, additional_rows])

# Save the expanded dataframe to a new CSV file
output_file = "expanded_selected_columns.csv"
expanded_df.to_csv(output_file, index=False)

print(f"Expanded dataset saved to {output_file}")
