import os
import time
import mariadb
from dotenv import load_dotenv

def execute_sql_file(cursor, filepath):
    print('Running initialize_db.py')
    print(f"Attempting to execute SQL file: {filepath}")
    try:
        with open(filepath, 'r') as file:
            sql_commands = file.read().split(';')
            for command in sql_commands:
                if command.strip():
                    print(f"Executing command: {command.strip()}")
                    cursor.execute(command)
    except FileNotFoundError:
        print(f"ERROR: SQL file not found at {filepath}")
        raise

def initialize_database():
    load_dotenv()

    # Regular user connection parameters
    config = {
        'host': 'mariadb',  # Use the service name from docker-compose
        'port': int(os.getenv('MARIADB_PORT')),
        'user': os.getenv('MARIADB_USER'),
        'password': os.getenv('MARIADB_PASSWORD'),
        'database': os.getenv('MARIADB_DATABASE'),
        'connect_timeout': 20
    }

    max_retries = 30  # Increase retries
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect as user (attempt {attempt + 1}/{max_retries})...")
            connection = mariadb.connect(**config)
            cursor = connection.cursor()

            # Explicitly select database
            database = config['database']
            cursor.execute(f"USE {database}")

            # Update SQL directory path to be relative to the current file
            sql_directory = '/app/sql'
            print(f"Looking for SQL files in: {sql_directory}")

            # Create sql directory if it doesn't exist
            os.makedirs(sql_directory, exist_ok=True)

            # Execute schema
            schema_path = os.path.join(sql_directory, 'schema.sql')
            if os.path.exists(schema_path):
                print("Creating tables...")
                execute_sql_file(cursor, schema_path)
            else:
                print(f"ERROR: schema.sql not found at {schema_path}")
                return

            # Execute seed data
            seed_path = os.path.join(sql_directory, 'seed.sql')
            if os.path.exists(seed_path):
                print("Inserting seed data...")
                execute_sql_file(cursor, seed_path)
            else:
                print(f"WARNING: seed.sql not found at {seed_path}")

            connection.commit()

            # Verify tables were created
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Created tables: {[table[0] for table in tables]}")

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
