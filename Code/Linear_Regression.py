import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the merged data
file_path = r"C:\Users\cn2802\Downloads\merged_data_table.csv"
data = pd.read_csv(file_path)

# Drop the 'time' column and rows with NaN values
data = data.drop(columns=['time']).dropna()

# Separate features and target variable
X = data.drop(columns=['Raw Conc.'])
y = data['Raw Conc.']

# Split the data into training (70%), validation (10%), and testing (20%) sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=2/3, random_state=42)  # 10% for validation, 20% for testing

# Normalize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Build the linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train_scaled, y_train)

# Validate the model
y_val_pred = model.predict(X_val_scaled)
val_mse = mean_squared_error(y_val, y_val_pred)
print(f'Validation MSE: {val_mse}')

# Test the model
y_test_pred = model.predict(X_test_scaled)
test_mse = mean_squared_error(y_test, y_test_pred)
print(f'Test MSE: {test_mse}')

# Print out the predicted values, ground truths, and differences for the test set
predicted_vs_actual = pd.DataFrame({
    'Predicted': y_test_pred.flatten(),
    'Ground Truth': y_test.values,
    'Difference': y_test.values - y_test_pred.flatten()
})

print(predicted_vs_actual.head())

# Save the predicted vs actual values to a CSV file
predicted_vs_actual.to_csv(r'C:\Users\cn2802\Downloads\predicted_vs_actual_linear_regression.csv', index=False)

print("Predicted vs actual values saved to: /mnt/data/predicted_vs_actual_linear_regression.csv")
