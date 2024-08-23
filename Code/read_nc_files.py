import xarray as xr
import numpy as np
import pandas as pd

# Coordinates of the US Embassy
us_embassy_coords = (28.5967, 77.1870)

# Load the .nc file
file_path = r"C:\Users\cn2802\Downloads\ML Project\era5_sfc_DELHI_2015.nc"
# Load the new CSV file
csv_file_path = r"C:\Users\cn2802\Downloads\ML Project\NewDelhi_PM2.5_2015_YTD.csv"

ds = xr.open_dataset(file_path)

# Extract longitude, latitude, and the data variables
longitudes = ds['longitude'].values
latitudes = ds['latitude'].values
time = ds['time'].values

# Create a meshgrid for the longitudes and latitudes
lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)

# Calculate the distances
distances = np.sqrt((lon_grid - us_embassy_coords[1])**2 + (lat_grid - us_embassy_coords[0])**2)

# Find the index of the minimum distance
min_index = np.unravel_index(np.argmin(distances), distances.shape)
closest_coordinates = (latitudes[min_index[1]], longitudes[min_index[0]])

# Print the closest coordinates
print("Closest coordinates:", closest_coordinates)

# Extract the 8760 values for the closest coordinate pair for all required variables
variables = ['u10', 'v10', 'd2m', 't2m', 'sp', 'tp']
closest_values = {}

for var in variables:
    data = ds[var].values
    closest_values[var] = data[:, min_index[1], min_index[0]]

# Create a DataFrame to store the values
data_dict = {
    'time': time,
}

# Add the values for each variable to the dictionary
for var in variables:
    data_dict[var] = closest_values[var]

# Create the DataFrame
df = pd.DataFrame(data_dict)

# Save the DataFrame to a CSV file
# df.to_csv('/mnt/data/extracted_data_table.csv', index=False)
print(df)

# Displaying the first few rows of the DataFrame for verification
df.head()

# Load the new CSV file
pm25_data = pd.read_csv(csv_file_path)

# Filter the data to only include rows where 'QC Name' is 'Valid'
filtered_pm25_data = pm25_data[pm25_data['QC Name'] == 'Valid']

# Convert 'Date (LT)' to datetime
filtered_pm25_data['Date (LT)'] = pd.to_datetime(filtered_pm25_data['Date (LT)'])

# Adjust the time in 'Date (LT)' by subtracting 5 hours
filtered_pm25_data['Date (LT)'] = filtered_pm25_data['Date (LT)'] - pd.Timedelta(hours=4)

# Convert the time variable to datetime for matching
df['time'] = pd.to_datetime(df['time'])

# Filter the df DataFrame to only include times that are present in the filtered_pm25_data
valid_times = filtered_pm25_data['Date (LT)']
df = df[df['time'].isin(valid_times)]

# Merge the filtered PM2.5 data with the extracted data on the time column
merged_data = pd.merge(df, filtered_pm25_data[['Date (LT)', 'Raw Conc.']], left_on='time', right_on='Date (LT)', how='left')

# Drop the extra 'Date (LT)' column
merged_data.drop(columns=['Date (LT)'], inplace=True)

# Save the merged DataFrame to a CSV file
merged_csv_path = r"C:\Users\cn2802\Downloads\ML Project\merged_data_table_lag90min.csv"
merged_data.to_csv(merged_csv_path, index=False)

print("Merged data saved to:", merged_csv_path)
print(merged_data)