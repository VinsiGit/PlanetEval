import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import numpy as np
from tensorflow.keras.models import load_model

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

# Load the pre-trained model from the specified file
model = load_model('models/model.keras')
print("Model loaded successfully.")

# Define the SQL query to fetch data from the 'missing_planet' table
query = """
    SELECT *
    FROM missing_planet
"""

# Use pandas to load the data into a DataFrame
try:
    df_missing_planet = pd.read_sql(query, connection)
    print("Missing planet data successfully loaded into DataFrame.")
except Exception as e:
    print("Error loading missing planet data into DataFrame:", e)

# Clean the data (drop rows with missing features)
columns = ['pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_bmasse', 'pl_eqt', 'pl_dens']
df_missing_planet_cleaned = df_missing_planet.dropna(subset=columns)

# Separate features (X) for prediction
X_missing = df_missing_planet_cleaned[columns].values

# Make predictions using the loaded model
predictions = model.predict(X_missing)

# Add the predictions to the DataFrame
df_missing_planet_cleaned['pl_esi_estimation'] = predictions

# Update the `missing_planet` table with the predicted values
try:
    cursor = connection.cursor()
    for index, row in df_missing_planet_cleaned.iterrows():
        update_query = """
            UPDATE missing_planet
            SET pl_esi_estimation = %s
            WHERE hostname = %s AND pl_letter = %s;
        """
        cursor.execute(update_query, (row['pl_esi_estimation'], row['hostname'], row['pl_letter']))
    connection.commit()
    print("Database updated with predicted values.")
except Exception as e:
    print("Error updating the database:", e)

# Close the connection
connection.close()
