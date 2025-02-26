import mariadb
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    try:
        conn = mariadb.connect(
            user=os.getenv("MARIADB_USER"),
            password=os.getenv("MARIADB_PASSWORD"),
            host=os.getenv("MARIADB_HOST"),
            port=int(os.getenv("MARIADB_PORT")),
            database=os.getenv("MARIADB_DATABASE")
        )
        print("Successfully connected to the database")
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

if __name__ == "__main__":
    connect_to_db()
