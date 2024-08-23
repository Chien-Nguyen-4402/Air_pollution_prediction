import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the merged data
file_path = r"C:\Users\cn2802\Downloads\ML Project\lag_30_70km_3_var_no_subtract\2023_lag30min_70km_3_var_no_subtract.csv"
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

# Define the parameter grid for hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_features': ['sqrt', 'log2', None],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Perform grid search with cross-validation
rf = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')
grid_search.fit(X_train_scaled, y_train)

# Get the best parameters from the grid search
best_params = grid_search.best_params_
print("Best parameters found: ", best_params)

# Train the Random Forest Regressor with the best parameters
best_rf = grid_search.best_estimator_

# Validate the model
y_val_pred = best_rf.predict(X_val_scaled)
val_mse = mean_squared_error(y_val, y_val_pred)
print(f'Validation MSE: {val_mse}')

# Test the model
y_test_pred = best_rf.predict(X_test_scaled)
test_mse = mean_squared_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)
print(f'Test MSE: {test_mse}')
print(f'Test R²: {test_r2}')

# Print out the predicted values, ground truths, and differences for the test set
predicted_vs_actual = pd.DataFrame({
    'Predicted': y_test_pred,
    'Ground Truth': y_test.values,
    'Difference': y_test.values - y_test_pred
})

print(predicted_vs_actual.head())

# Visualize feature importance
feature_importances = best_rf.feature_importances_
feature_names = X.columns

# Create a DataFrame for better visualization
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
})

# Sort the DataFrame by importance
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Plot feature importances
plt.figure(figsize=(12, 8))
plt.barh(importance_df['Feature'], importance_df['Importance'], color='skyblue')
plt.xlabel('Importance')
plt.ylabel('Features')
plt.title('Feature Importances in Random Forest Model')
plt.gca().invert_yaxis()  # Invert y-axis to display the most important feature at the top
plt.show()

# Save the predicted vs actual values to a CSV file
# predicted_vs_actual.to_csv(r'C:\Users\cn2802\Downloads\predicted_vs_actual.csv', index=False)

# print("Predicted vs actual values saved to: /mnt/data/predicted_vs_actual.csv")
