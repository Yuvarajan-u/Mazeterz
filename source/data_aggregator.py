import pandas as pd
import numpy as np

# print(f"Schedule generated and saved to {output_file}")
df = pd.read_csv('data.csv')
# df = pd.DataFrame(data)

# Extract the weekday part from the 'Department_Name' column
df['Weekday'] = df['Department_Name'].apply(lambda x: x.split('_')[1])

# Initialize the result dictionary
result = {
    'Department Name': df.columns[1:],  # All department names
    'Mondays': [df[df['Weekday'] == 'Monday'][dept].tolist() for dept in df.columns[1:]],
    'Tuesdays': [df[df['Weekday'] == 'Tuesday'][dept].tolist() for dept in df.columns[1:]],
    'Wednesdays': [df[df['Weekday'] == 'Wednesday'][dept].tolist() for dept in df.columns[1:]],
    'Thursdays': [df[df['Weekday'] == 'Thursday'][dept].tolist() for dept in df.columns[1:]],
    'Fridays': [df[df['Weekday'] == 'Friday'][dept].tolist() for dept in df.columns[1:]],
}

# Convert result dictionary to DataFrame
result_df = pd.DataFrame(result)

# Save the result to a new CSV file
output_file = 'department_weekday_aggregated_data.csv'
result_df.to_csv(output_file, index=False)

print(f"CSV file generated and saved as {output_file}")