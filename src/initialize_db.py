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

def initialize_database():
    load_dotenv()

    # Regular user connection parameters
    config = {
        'host': os.getenv('MARIADB_HOST'),
        'port': int(os.getenv('MARIADB_PORT')),
        'user': os.getenv('MARIADB_USER'),
        'password': os.getenv('MARIADB_PASSWORD'),
        'database': os.getenv('MARIADB_DATABASE')
    }

    max_retries = 10
    retry_delay = 3

    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect as user (attempt {attempt + 1}/{max_retries})...")
            connection = mariadb.connect(**config)
            cursor = connection.cursor()

            # Explicitly select database
            database = config['database']
            cursor.execute(f"USE {database}")

            sql_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql')

            # Execute schema
            schema_path = os.path.join(sql_directory, 'schema.sql')
            if os.path.exists(schema_path):
                print("Creating tables...")
                execute_sql_file(cursor, schema_path)

            # Execute seed data
            seed_path = os.path.join(sql_directory, 'seed.sql')
            if os.path.exists(seed_path):
                print("Inserting seed data...")
                execute_sql_file(cursor, seed_path)

            connection.commit()
            print("Database initialization completed successfully!")
            break

        except mariadb.Error as e:
            print(f"Error: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not initialize database.")
                return

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

if __name__ == "__main__":
    initialize_database()
