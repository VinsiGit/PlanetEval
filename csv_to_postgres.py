import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2

# Load environment variables from .env file
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 15432

def connect_to_database():
    """Connect to the specific database."""
    try:
        connection = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
        )
        print(f"Connected to the database '{POSTGRES_DB}' successfully.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database '{POSTGRES_DB}':", e)
        return None

# Function to execute SQL queries
def execute_sql(connection, sql_query):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
        print("SQL query executed successfully.")
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()

# Load the CSV files into pandas DataFrames
eval_df = pd.read_csv('cleaning/eval.csv')
training_df = pd.read_csv('cleaning/training.csv')

# Ensure the column names match across the files where necessary
missing_planet_columns = ['hostname', 'pl_letter', 'pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_bmasse', 'pl_eqt',
                          'pl_dens', 'pl_esi_estimate']
planet_columns = ['hostname', 'pl_letter', 'pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_bmasse', 'pl_eqt', 'pl_dens', 'pl_esi']

# Missing planet data (from eval.csv)
missing_planet_df = eval_df[missing_planet_columns]

# Planet data (from training.csv)
planet_df = training_df[planet_columns]

# Extract system data from training_df and convert 'cb_flag' to boolean
system_columns = ['hostname', 'cb_flag', 'sy_snum', 'sy_pnum', 'ra', 'dec', 'sy_dist', 'st_lum', 'st_dens', 'st_age', 'st_teff']
system_df = training_df[system_columns].drop_duplicates(subset=['hostname'])

# Convert 'cb_flag' from int to boolean (0 -> False, 1 -> True)
system_df['cb_flag'] = system_df['cb_flag'].astype(bool)

# Generate SQL for `system`
system_sql = "INSERT INTO system (hostname, cb_flag, sy_snum, sy_pnum, ra, dec, sy_dist, st_lum, st_dens, st_age, st_teff) VALUES\n"
system_values = []

for _, row in system_df.iterrows():
    system_values.append(f"('{row['hostname']}', {row['cb_flag']}, {row['sy_snum']}, {row['sy_pnum']}, {row['ra']}, {row['dec']}, {row['sy_dist']}, {row['st_lum']}, {row['st_dens']}, {row['st_age']}, {row['st_teff']})")

system_sql += ",\n".join(system_values) + ";"

# Generate SQL for `missing_planet`
missing_planet_sql = "INSERT INTO missing_planet (hostname, pl_letter, pl_orbper, pl_orbsmax, pl_rade, pl_bmasse, pl_eqt, pl_dens, pl_esi_estimation) VALUES\n"
missing_planet_values = []

for _, row in missing_planet_df.iterrows():
    missing_planet_values.append(f"('{row['hostname']}', '{row['pl_letter']}', {row['pl_orbper']}, {row['pl_orbsmax']}, {row['pl_rade']}, {row['pl_bmasse']}, {row['pl_eqt']}, {row['pl_dens']}, {row['pl_esi_estimate']})")

missing_planet_sql += ",\n".join(missing_planet_values) + ";"

# Generate SQL for `planet`
planet_sql = "INSERT INTO planet (hostname, pl_letter, pl_orbper, pl_orbsmax, pl_rade, pl_bmasse, pl_eqt, pl_dens, pl_esi) VALUES\n"
planet_values = []

for _, row in planet_df.iterrows():
    planet_values.append(f"('{row['hostname']}', '{row['pl_letter']}', {row['pl_orbper']}, {row['pl_orbsmax']}, {row['pl_rade']}, {row['pl_bmasse']}, {row['pl_eqt']}, {row['pl_dens']}, {row['pl_esi']})")

planet_sql += ",\n".join(planet_values) + ";"

# Connect to the database
connection = connect_to_database()

if connection:
    # Step 1: Insert system data first
    execute_sql(connection, system_sql)

    # Step 2: Insert missing_planet data (hostname should already exist in system)
    execute_sql(connection, missing_planet_sql)

    # Step 3: Insert planet data (hostname should already exist in system)
    execute_sql(connection, planet_sql)

    # Close the connection
    connection.close()
