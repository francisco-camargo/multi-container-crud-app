import os
import time
import mariadb
from dotenv import load_dotenv
from tabulate import tabulate

def show_table_data():
    # Load environment variables
    load_dotenv()

    # Connection parameters
    config = {
        'host': os.getenv('MARIADB_HOST'),
        'port': int(os.getenv('MARIADB_PORT')),
        'user': os.getenv('MARIADB_USER'),
        'password': os.getenv('MARIADB_PASSWORD'),
        'database': os.getenv('MARIADB_DATABASE')
    }

    max_retries = 10
    retry_delay = 3  # seconds

    for attempt in range(max_retries):
        try:
            # Connect to MariaDB
            print(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})...")
            connection = mariadb.connect(**config)
            cursor = connection.cursor()

            # Get all tables in the database
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
            """, (config['database'],))

            tables = [table[0] for table in cursor.fetchall()]

            if not tables:
                print("No tables found in the database.")
                return

            # For each table, show first 3 rows
            for table in tables:
                print(f"\n=== First 3 rows from {table} ===")

                # Get column names
                cursor.execute(f"DESCRIBE {table}")
                headers = [col[0] for col in cursor.fetchall()]

                # Get first 3 rows
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                rows = cursor.fetchall()

                if rows:
                    print(tabulate(rows, headers=headers, tablefmt='grid'))
                else:
                    print("(No data in table)")

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
    show_table_data()
