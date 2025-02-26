import os
import time
import mariadb
from dotenv import load_dotenv

def execute_sql_file(cursor, filepath):
    with open(filepath, 'r') as file:
        sql_commands = file.read().split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)

def setup_database():
    # Load environment variables
    load_dotenv()

    # Connection parameters
    config = {
        'host': os.getenv('MARIADB_HOST'),
        'port': int(os.getenv('MARIADB_PORT')),
        'user': os.getenv('MARIADB_USER'),
        'password': os.getenv('MARIADB_PASSWORD')
    }

    max_retries = 5
    retry_delay = 2  # seconds

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
                cursor.execute(f"USE {database_name}")

                # Execute SQL files in order
                sql_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql')

                # Execute schema first
                schema_path = os.path.join(sql_directory, 'schema.sql')
                if os.path.exists(schema_path):
                    execute_sql_file(cursor, schema_path)

                # Then execute seed data
                seed_path = os.path.join(sql_directory, 'seed.sql')
                if os.path.exists(seed_path):
                    execute_sql_file(cursor, seed_path)

                connection.commit()
                print("Database setup completed successfully!")

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
