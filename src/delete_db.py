import os
import time
import mariadb
from dotenv import load_dotenv

def delete_database():
    # Load environment variables
    load_dotenv()

    print("WARNING: This script uses root credentials. This is generally not recommended for security reasons.")
    print("Consider granting necessary privileges to regular users for production environments.")

    # Connection parameters for root user
    config = {
        'host': os.getenv('MARIADB_HOST'),
        'port': int(os.getenv('MARIADB_PORT')),
        'user': 'root',
        'password': os.getenv('MARIADB_ROOT_PASSWORD')
    }

    max_retries = 10
    retry_delay = 3  # seconds

    for attempt in range(max_retries):
        try:
            # Connect to MariaDB as root
            print(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})...")
            connection = mariadb.connect(**config)
            cursor = connection.cursor()

            # If we get here, connection was successful
            print("Successfully connected to MariaDB!")

            # Check if database exists
            database_name = os.getenv('MARIADB_DATABASE')
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]

            if database_name in databases:
                print(f"Database '{database_name}' exists. Proceeding with deletion...")
                cursor.execute(f"DROP DATABASE {database_name}")
                connection.commit()
                print(f"Database '{database_name}' has been deleted successfully!")
            else:
                print(f"Database '{database_name}' does not exist. No deletion needed.")

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
    delete_database()
