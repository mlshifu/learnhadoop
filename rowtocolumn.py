import pandas as pd

# Sample result_df
result_data = {'hostname': ['abc1.com', 'abc2.com', 'abc3.com', 'abc4.com', 'abc5.com', 'abc6.com'],
               'value': [10, 20, 30, 40, 50, 60]}
result_df = pd.DataFrame(result_data)

# Set the timestamp for the current run
current_timestamp = pd.to_datetime('now')

# Create a new DataFrame for the final output
final_result_df = pd.DataFrame(columns=["Timestamp"] + result_df["hostname"].tolist())

# Fill in the values for the final DataFrame
final_result_df.loc[0, "Timestamp"] = current_timestamp
for hostname in result_df["hostname"]:
    value = result_df[result_df["hostname"] == hostname]["value"].tolist()
    final_result_df[hostname] = value

# Set the full path for the result file
result_file = '/home/ravi/scriptoutput/result_history.csv'

# Save the final result DataFrame to the CSV file
final_result_df.to_csv(result_file, index=False)
