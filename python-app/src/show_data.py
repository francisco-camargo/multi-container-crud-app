import os
import time
import mariadb
from dotenv import load_dotenv
from tabulate import tabulate

host = os.getenv('MARIADB_HOST')

def show_table_data(
    table_name,
    host=host,
    ):
    print('Running show_data.py')
    load_dotenv()

    config = {
        'host': host,  # Use container service name
        'port': int(os.getenv('MARIADB_PORT')),
        'user': os.getenv('MARIADB_USER'),
        'password': os.getenv('MARIADB_PASSWORD'),
        'database': os.getenv('MARIADB_DATABASE'),
        'connect_timeout': 20
    }

    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            connection = mariadb.connect(**config)
            cursor = connection.cursor()

            # Get column names
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]

            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            if rows:
                print(f"\nContents of {table_name}:")
                print(tabulate(rows, headers=columns, tablefmt='grid'))
            else:
                print(f"\nNo data found in {table_name}")

            break

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
    tables = ['users', 'posts', 'comments']
    for table in tables:
        show_table_data(table, host='localhost')
