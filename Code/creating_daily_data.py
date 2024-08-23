import pandas as pd
import os

# Define the folder where the files are located
folder_path = r"C:\Users\cn2802\Downloads\ML Project\lag_30_70km_5_var_with_subtract"

# Initialize an empty list to store the dataframes
dataframes = []

# Loop over all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        # Create the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Read the CSV file into a dataframe
        df = pd.read_csv(file_path)
        
        # Append the dataframe to the list
        dataframes.append(df)

# Concatenate all dataframes into one
data = pd.concat(dataframes, ignore_index=True)

# Convert 'time' column to datetime format
data['time'] = pd.to_datetime(data['time'])

# Set 'time' as the index
data.set_index('time', inplace=True)

# Resample the data to calculate daily averages
daily_averages = data.resample('D').mean()

# Reset index to move 'time' from index back to a column
daily_averages.reset_index(inplace=True)

# Save the daily averages to a new CSV file
output_path = r"C:\Users\cn2802\Downloads\ML Project\lag_30_70km_5_var_with_subtract\daily_avg.csv"
daily_averages.to_csv(output_path, index=False)

# Display the first few rows of the daily averages
print(daily_averages)
print(f"Daily averages saved to: {output_path}")
