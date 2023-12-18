import pandas as pd

# Sample result_df
result_data = {'hostname': ['abc1.com', 'abc2.com', 'abc3.com', 'abc4.com', 'abc5.com', 'abc6.com'],
               'value': [10, 20, 30, 40, 50, 60]}
result_df = pd.DataFrame(result_data)

# Set the full path for the result file
result_file = '/home/ravi/scriptoutput/result_history.csv'

# Read the existing CSV file and keep only the last 47 entries (including the current run)
result_df_history = pd.read_csv(result_file)
result_df_history = result_df_history.tail(47)

# Set the timestamp for the current run
current_timestamp = pd.to_datetime('now')

# Add the current run to the history DataFrame
result_df_history = result_df_history.append({"Timestamp": current_timestamp, **result_df.set_index('hostname').to_dict()['value']}, ignore_index=True)

# Save the history DataFrame back to the CSV file
result_df_history.to_csv(result_file, index=False)
