import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env file
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 15432

# Directory containing SQL files
SQL_DIRECTORY = "sql"

def read_sql_file(file_path):
    """Read an SQL file and return its content."""
    with open(file_path, 'r') as file:
        return file.read()

def execute_sql_file(connection, sql_file_path):
    """Execute an SQL file on the database."""
    try:
        with connection.cursor() as cursor:
            sql_content = read_sql_file(sql_file_path)
            cursor.execute(sql_content)
            connection.commit()
            print(f"Executed {sql_file_path} successfully.")
    except Exception as e:
        print(f"Error executing {sql_file_path}: {e}")
        connection.rollback()

def connect_to_server():
    """Connect to the PostgreSQL server (not specific to a database)."""
    try:
        connection = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        print("Connected to the PostgreSQL server successfully.")
        return connection
    except Exception as e:
        print("Error connecting to the PostgreSQL server:", e)
        return None

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

def execute_remaining_scripts(connection):
    """Execute remaining SQL scripts in order."""
    try:
        scripts = ["system.sql", "planets.sql", "incomplete_planets.sql"]
        for script in scripts:
            script_path = os.path.join(SQL_DIRECTORY, script)
            execute_sql_file(connection, script_path)
    except Exception as e:
        print(f"Error executing scripts: {e}")

def main():
    db_connection = connect_to_database()
    if db_connection:
        execute_remaining_scripts(db_connection)
        db_connection.close()
        print("Database setup and script execution completed.")

if __name__ == "__main__":
    main()
