import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
'''uM1 ds1	uM1 ds2	uM1 ds3	uM1 ds4
'''
def evaluate_model(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    
datafile = 'uMyo_uLabel_Recording_14_20240323_003917-Test-Crop-save.csv'
data = pd.read_csv(f'training_data/{datafile}')

print(f'Training Model from {datafile}')

input_features = ['uM1 ds1','uM1 ds2','uM1 ds3','uM1 ds4','uM1 Timestamp',
                  'uM2 ds1','uM2 ds2','uM2 ds3','uM2 ds4','uM2 Timestamp',
                  'uM3 ds1','uM3 ds2','uM3 ds3','uM3 ds4','uM3 Timestamp',]
X = data[input_features]
input_labels = ['h1','h2','h3','h4','h5','uL Timestamp']
y = data[input_labels]

# Split the data into training and testing sets, and scale the input features
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()


base_model = RandomForestRegressor(n_estimators=100, random_state=42)

model = MultiOutputRegressor(base_model)

model.fit(X_train, y_train)

# Print the evaluation metric(s) to the screen
with open(f'{datafile.split(".")[0]}.pkl', 'wb') as f:
    pickle.dump(model, f)


# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
evaluate_model(y_test, y_pred)

# Create a new DataFrame with the actual and predicted labels
result_df = y_test.copy().reset_index(drop=True)
result_df.columns = ['Actual uLable 0', 'Actual uLable 1', 'Actual uLable 2', 'Actual uLable 3','Actual uLable 4', 'LASK_time']
result_df['Predicted uLable 0'] = y_pred[:, 0]
result_df['Predicted uLable 1'] = y_pred[:, 1]
result_df['Predicted uLable 2'] = y_pred[:, 2]
result_df['Predicted uLable 3'] = y_pred[:, 3]
result_df['Predicted uLable 4'] = y_pred[:, 4]

# Save the DataFrame as a CSV file
result_df.to_csv('predictions_vs_actuals.csv', index=False)
