import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Load the dataset from an Excel file
data = pd.read_excel(r'C:\Users\nidhi\Downloads\onlinefraud.xlsx')  # Ensure the path is correct

# Check the first few rows to ensure the data is loaded properly
print(data.head())

# Assuming 'type' is categorical and needs to be converted to numeric
data['type'] = data['type'].map({"CASH_OUT": 1, "PAYMENT": 2, "CASH_IN": 3, "TRANSFER": 4, "DEBIT": 5})

# Ensure there are no missing values in the dataset
print(data.isnull().sum())  # This will print the count of missing values for each column

# Define features (X) and target labels (y)
X_train = data[['type', 'amount', 'oldbalanceOrg', 'newbalanceOrig']].values  # Features
y_train = data['fraud'].values  # Target (fraud or not)

# Check if X_train and y_train are defined correctly
print(X_train.shape)  # Should show (number of samples, number of features)
print(y_train.shape)  # Should show (number of samples,)

# Define the model
model = Sequential([
    Dense(64, activation='relu', input_dim=X_train.shape[1]),  # input_dim should match number of features
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # For binary classification (fraud or not)
])

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Save the trained model to 'static/model.h5'
model.save("static/model.h5")
print("Model saved as 'static/model.h5'")
