import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, Reshape, Masking, GlobalAveragePooling1D, Dense, Dropout

# Load environment variables from .env file
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 15432

# Establish the connection to the PostgreSQL database
try:
    connection = psycopg2.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB
    )
    print(f"Connected to the database '{POSTGRES_DB}' successfully.")
except Exception as e:
    print(f"Error connecting to the database '{POSTGRES_DB}':", e)

# Define the SQL query to fetch data from the 'planet' table
query = """
    SELECT * FROM planet;
"""

# Use pandas to load the data into a DataFrame
try:
    df = pd.read_sql(query, connection)
    print("Data successfully loaded into DataFrame.")
except Exception as e:
    print("Error loading data into DataFrame:", e)

# Optionally, you can close the connection after you're done
connection.close()

# Show the first few rows of the DataFrame
print(df.head())

columns = ['pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_bmasse', 'pl_eqt', 'pl_dens', 'pl_esi']

# Drop rows where all features are missing
df_cleaned = df[columns].dropna(subset=columns[:-1])

# Separate features (X) and target (y)
X = df_cleaned[['pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_bmasse', 'pl_eqt', 'pl_dens']].values
y = df_cleaned['pl_esi'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the model architecture
model = Sequential([
    Input(shape=(X_train.shape[1],)),  # Input layer, shape = number of features
    Reshape((X_train.shape[1], 1)),  # Reshape input to 3D for masking
    Masking(mask_value=np.nan),  # Ignore NaN values
    GlobalAveragePooling1D(),  # Global average pooling layer to reduce dimensions
    Dense(256, activation='relu'),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),# Dense layer with ReLU activation
    Dropout(0.1),  # Dropout to avoid overfitting
    Dense(1)  # Output layer, no activation as it's a regression task
])

# Compile the model
model.compile(optimizer='adam',
              loss='mean_squared_error',  # Using MSE for regression tasks
              metrics=['mae'])  # Mean Absolute Error for evaluation

# Train the model
model.fit(X_train, y_train, epochs=128, batch_size=32, validation_split=0.3)

# Evaluate the model on the test set
test_loss, test_mae = model.evaluate(X_test, y_test)

print(f"Test Loss: {test_loss}")
print(f"Test MAE: {test_mae}")

models_dir = 'models'
model_path = os.path.join(models_dir, 'model.keras')

os.makedirs(models_dir, exist_ok=True)

model.save(model_path)
