import os
import time
import mariadb
from dotenv import load_dotenv

def setup_database():
    # Load environment variables
    load_dotenv()

    # Regular user connection parameters
    config = {
        'host': os.getenv('MARIADB_HOST'),
        'port': int(os.getenv('MARIADB_PORT')),
        'user': os.getenv('MARIADB_USER'),
        'password': os.getenv('MARIADB_PASSWORD')
    }

    max_retries = 10
    retry_delay = 3  # seconds

    for attempt in range(max_retries):
        try:
            # Connect to MariaDB
            print(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})...")
            connection = mariadb.connect(**config)
            cursor = connection.cursor()

            # If we get here, connection was successful
            print("Successfully connected to MariaDB!")

            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor]
            database_name = os.getenv('MARIADB_DATABASE')

            if database_name in databases:
                print(f"Database '{database_name}' already exists. Skipping setup.")
            else:
                print(f"Database '{database_name}' does not exist. Creating now...")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
                print("Database created.")

            break  # Exit the retry loop if successful

        except mariadb.Error as e:
            print(f"Error: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to database.")
                return

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

if __name__ == "__main__":
    setup_database()
