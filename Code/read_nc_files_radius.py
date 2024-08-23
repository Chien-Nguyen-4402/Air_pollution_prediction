import xarray as xr
import numpy as np
import pandas as pd
from haversine import haversine, Unit

# Coordinates of the US Embassy
us_embassy_coords = (28.5967, 77.1870)

# Load the sfc file
file_path = r"C:\Users\cn2802\Downloads\ML Project\era5_sfc_DELHI_2023.nc"
# Load the new NetCDF file for 'pblh'
nc_file_path_blh = r"C:\Users\cn2802\Downloads\ML Project\era5_pblh_DELHI_2023.nc"
# Load the new NetCDF file for 't'
nc_file_path_t = r"C:\Users\cn2802\Downloads\ML Project\era5_t_DELHI_2023.nc"
# Load the new CSV file
csv_file_path = r"C:\Users\cn2802\Downloads\ML Project\NewDelhi_PM2.5_2023_YTD.csv"
# Output path
output_file_name = r"C:\Users\cn2802\Downloads\ML Project\2023_lag30min_70km_3_var_no_subtract.csv"


ds = xr.open_dataset(file_path)

# Extract longitude, latitude, and the data variables
longitudes = ds['longitude'].values
latitudes = ds['latitude'].values
time = ds['time'].values

# Create a meshgrid for the longitudes and latitudes
lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)

# Calculate distances using Haversine formula
distances = np.array([
    [haversine(us_embassy_coords, (lat, lon), unit=Unit.KILOMETERS) for lon in longitudes]
    for lat in latitudes
])

# Find all stations within a 30 km radius
indices_within_radius = np.where(distances <= 70)

# Print coordinates of all stations found
stations_coords = [(latitudes[i], longitudes[j]) for i, j in zip(*indices_within_radius)]
print("Number of stations found: ", len(stations_coords))
print("Coordinates of stations within 70 km radius:")
for coord in stations_coords:
    print(coord)

# Average the data for all variables over the stations within 30 km
variables = ['u10', 'v10', 'd2m', 't2m', 'sp', 'tp']
averaged_data = {}

for var in variables:
    data = ds[var].values
    averaged_data[var] = data[:, indices_within_radius[0], indices_within_radius[1]].mean(axis=1)

# Create a DataFrame to store the averaged values
data_dict = {
    'time': time,
}

# Add the averaged values for each variable to the dictionary
for var in variables:
    data_dict[var] = averaged_data[var]

# Create the DataFrame
df = pd.DataFrame(data_dict)

# Display the DataFrame to the user
print("Averaged data for all stations within 70 km radius:")
print(df)





ds_blh = xr.open_dataset(nc_file_path_blh)

# Extract longitude, latitude, and the blh data variable
longitudes_blh = ds_blh['longitude'].values
latitudes_blh = ds_blh['latitude'].values
time_blh = ds_blh['time'].values
blh = ds_blh['blh'].values  # Corrected variable name

# Create a meshgrid for the longitudes and latitudes
lon_grid_blh, lat_grid_blh = np.meshgrid(longitudes_blh, latitudes_blh)

# Calculate distances using Haversine formula
distances_blh = np.array([
    [haversine(us_embassy_coords, (lat, lon), unit=Unit.KILOMETERS) for lon in longitudes_blh]
    for lat in latitudes_blh
])

# Find all stations within a 70 km radius
indices_within_radius_blh = np.where(distances_blh <= 70)

# Print coordinates of all stations found
stations_coords_blh = [(latitudes_blh[i], longitudes_blh[j]) for i, j in zip(*indices_within_radius_blh)]
print("Number of blh stations found: ", len(stations_coords_blh))
print("Coordinates of blh stations within 70 km radius:")
for coord in stations_coords_blh:
    print(coord)

# Average the data for the blh variable over the stations within 70 km
averaged_blh = blh[:, indices_within_radius_blh[0], indices_within_radius_blh[1]].mean(axis=1)

# Convert the time array to pandas datetime format
time_blh = pd.to_datetime(time_blh)

# Create a DataFrame for the blh variable with time
blh_df = pd.DataFrame({
    'time': time_blh,
    'blh': averaged_blh
})
print(blh_df)

# # Resample to daily averages
# daily_blh_df = blh_df.resample('D', on='time').mean().reset_index()

# Merge with the existing data
df['time'] = pd.to_datetime(df['time'])
df = pd.merge(df, blh_df, on='time', how='left')
print(df)




# Load the new NetCDF file for 't'
ds_t = xr.open_dataset(nc_file_path_t)

# Extract longitude, latitude, and the t data variable
longitudes_t = ds_t['longitude'].values
latitudes_t = ds_t['latitude'].values
time_t = ds_t['time'].values
t = ds_t['t'].values  # Assuming the variable name is 't'

# Create a meshgrid for the longitudes and latitudes
lon_grid_t, lat_grid_t = np.meshgrid(longitudes_t, latitudes_t)

# Calculate distances using Haversine formula
distances_t = np.array([
    [haversine(us_embassy_coords, (lat, lon), unit=Unit.KILOMETERS) for lon in longitudes_t]
    for lat in latitudes_t
])

# Find all stations within a 70 km radius
indices_within_radius_t = np.where(distances_t <= 70)

# Print coordinates of all stations found
stations_coords_t = [(latitudes_t[i], longitudes_t[j]) for i, j in zip(*indices_within_radius_t)]
print("Number of t stations found: ", len(stations_coords_t))
print("Coordinates of t stations within 70 km radius:")
for coord in stations_coords_t:
    print(coord)

# Average the data for the t variable over the stations within 70 km along the level dimension
averaged_t_level1 = t[:, 0, indices_within_radius_t[0], indices_within_radius_t[1]].mean(axis=1)
averaged_t_level2 = t[:, 1, indices_within_radius_t[0], indices_within_radius_t[1]].mean(axis=1)

# Convert the time array to pandas datetime format
time_t = pd.to_datetime(time_t)

# Create a DataFrame for the t variable with time
t_df_level1 = pd.DataFrame({
    'time': time_t,
    't_level1': averaged_t_level1
})

t_df_level2 = pd.DataFrame({
    'time': time_t,
    't_level2': averaged_t_level2
})

print(t_df_level1)
print(t_df_level2)

# Merge with the existing data
df['time'] = pd.to_datetime(df['time'])
df = pd.merge(df, t_df_level1, on='time', how='left')
df = pd.merge(df, t_df_level2, on='time', how='left')
print(df)
# Subtract t2m from t_level1 and t_level2 and add as new columns
df['t_level1_minus_t2m'] = df['t_level1'] - df['t2m']
df['t_level2_minus_t2m'] = df['t_level2'] - df['t2m']





# Load the new CSV file
pm25_data = pd.read_csv(csv_file_path)

# Filter the data to only include rows where 'QC Name' is 'Valid'
filtered_pm25_data = pm25_data[pm25_data['QC Name'] == 'Valid']

# Convert 'Date (LT)' to datetime and match it with the time in data_dict
filtered_pm25_data['Date (LT)'] = pd.to_datetime(filtered_pm25_data['Date (LT)'])

# Adjust the time in 'Date (LT)' by subtracting 5 hours
filtered_pm25_data['Date (LT)'] = filtered_pm25_data['Date (LT)'] - pd.Timedelta(hours=6)

# Convert the time variable to datetime for matching
df['time'] = pd.to_datetime(df['time'])

# Filter the df DataFrame to only include times that are present in the filtered_pm25_data
valid_times = filtered_pm25_data['Date (LT)']
df = df[df['time'].isin(valid_times)]

# Merge the filtered PM2.5 data with the averaged data on the time column
merged_data = pd.merge(df, filtered_pm25_data[['Date (LT)', 'Raw Conc.']], left_on='time', right_on='Date (LT)', how='left')

# Drop the extra 'Date (LT)' column
merged_data.drop(columns=['Date (LT)'], inplace=True)

# Save the merged DataFrame to a CSV file
merged_data.to_csv(output_file_name, index=False)

print("Merged data saved to:", output_file_name)
print(merged_data)