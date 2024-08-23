import xarray as xr

# Load the new NetCDF file to peek into it
nc_file_path_t = r"C:\Users\cn2802\Downloads\ML Project\era5_t_DELHI_2015.nc"
ds_t = xr.open_dataset(nc_file_path_t)

# Print the dataset information to understand its structure
print(ds_t)