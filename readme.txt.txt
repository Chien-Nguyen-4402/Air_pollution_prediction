Lag_30: The ground truth (PM2.5 concentration) is 30 minutes behind the input(meteorological data). For example, if meteorological data was collected at 1:00PM, this data will be used to predict PM2.5 concentration at 1:30 PM.

70_km: We find all stations within 70 kilometers radius from the US Embassy in New Delhi (23 stations in total) and average the meteorological measurements that they have obtained and use this averaged data as input for the Random Forest

3_var_no_subtract: In addition to the first 6 variables (u10, v10, d2m, t2m, sp, tp) which are used as input in the Lag_30_70_km folder, we use 3 more variables (blh, t_level1, t_level2)

5_var_with_subtract: In addition to the first 6 variables (u10, v10, d2m, t2m, sp, tp) which are used as input in the Lag_30_70_km folder, we use 5 more variables (blh, t_level1, t_level2, t_level1 - t2m, t_level2 - t2m)
