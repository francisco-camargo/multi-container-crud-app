import os
from typing import List, Dict, Any, Optional
import mariadb
from dotenv import load_dotenv

class DatabaseCRUD:
    def __init__(self):
        """Initialize database connection parameters."""
        load_dotenv()
        self.config = {
            'host': os.getenv('MARIADB_HOST'),
            'port': int(os.getenv('MARIADB_PORT')),
            'user': os.getenv('MARIADB_USER'),
            'password': os.getenv('MARIADB_PASSWORD'),
            'database': os.getenv('MARIADB_DATABASE')
        }

    def _get_connection(self) -> tuple[mariadb.Connection, mariadb.Cursor]:
        """Create and return a database connection and cursor."""
        connection = mariadb.connect(**self.config)
        cursor = connection.cursor(dictionary=True)  # Return results as dictionaries
        cursor.execute(f"USE {self.config['database']}")
        return connection, cursor

    def create_record(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert a new record into the specified table.

        Args:
            table: Name of the table
            data: Dictionary of column names and values

        Returns:
            ID of the inserted record
        """
        try:
            connection, cursor = self._get_connection()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            cursor.execute(query, list(data.values()))
            connection.commit()
            return cursor.lastrowid

        finally:
            cursor.close()
            connection.close()

    def read_records(self, table: str, conditions: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve records from the specified table.

        Args:
            table: Name of the table
            conditions: Optional dictionary of WHERE conditions

        Returns:
            List of records as dictionaries
        """
        try:
            connection, cursor = self._get_connection()
            query = f"SELECT * FROM {table}"

            if conditions:
                where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
                query += f" WHERE {where_clause}"
                cursor.execute(query, list(conditions.values()))
            else:
                cursor.execute(query)

            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def update_record(self, table: str, data: Dict[str, Any], condition_id: int) -> bool:
        """
        Update a record in the specified table.

        Args:
            table: Name of the table
            data: Dictionary of columns to update
            condition_id: ID of the record to update

        Returns:
            True if update was successful
        """
        try:
            connection, cursor = self._get_connection()
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE id = ?"

            values = list(data.values()) + [condition_id]
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount > 0

        finally:
            cursor.close()
            connection.close()

    def delete_record(self, table: str, record_id: int) -> bool:
        """
        Delete a record from the specified table.

        Args:
            table: Name of the table
            record_id: ID of the record to delete

        Returns:
            True if deletion was successful
        """
        try:
            connection, cursor = self._get_connection()
            query = f"DELETE FROM {table} WHERE id = ?"

            cursor.execute(query, (record_id,))
            connection.commit()
            return cursor.rowcount > 0

        finally:
            cursor.close()
            connection.close()

# Example usage
if __name__ == "__main__":
    db = DatabaseCRUD()

    # Create
    new_record = {"username": "Test User", "email": "test@example.com"}
    record_id = db.create_record("users", new_record)
    print(f"Created record with ID: {record_id}")

    # Read
    records = db.read_records("users", {"id": record_id})
    print(f"Retrieved record: {records[0]}")

    # Update
    updated_data = {"email": "updated@example.com"}
    success = db.update_record("users", updated_data, record_id)
    print(f"Update successful: {success}")

    # Delete
    success = db.delete_record("users", record_id)
    print(f"Delete successful: {success}")
