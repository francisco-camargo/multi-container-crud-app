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
        Insert a new record into the specified table using SQL template file.

        Args:
            table: Name of the table (e.g., 'users')
            data: Dictionary of column names and values (e.g., {"name": "Alice", "email": "alice@example.com"})

        Returns:
            ID of the inserted record
        """
        try:
            connection, cursor = self._get_connection()

            # Read SQL template using the correct path
            sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'insert_record.sql')
            with open(sql_path, 'r') as f:
                sql_template = f.read()

            # Format the SQL template
            columns = ', '.join(data.keys())
            values_placeholders = ', '.join(['%s' for _ in data])
            sql = sql_template.format(
                table=table,
                columns=columns,
                values=values_placeholders,
            )

            # Execute the SQL with values
            cursor.execute(sql, list(data.values()))
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

            # Read SQL template
            sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'select_records.sql')
            with open(sql_path, 'r') as f:
                sql_template = f.read()

            # Build where clause if conditions exist
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + ' AND '.join([f"{k} = ?" for k in conditions.keys()])

            # Format the SQL template
            sql = sql_template.format(
                table=table,
                where_clause=where_clause
            )

            # Execute query with or without conditions
            if conditions:
                cursor.execute(sql, list(conditions.values()))
            else:
                cursor.execute(sql)

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

            # Read SQL template
            sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'update_record.sql')
            with open(sql_path, 'r') as f:
                sql_template = f.read()

            # Format the SQL template
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            sql = sql_template.format(
                table=table,
                set_clause=set_clause
            )

            # Execute with values including the condition_id
            values = list(data.values()) + [condition_id]
            cursor.execute(sql, values)
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

            # Read SQL template
            sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'delete_record.sql')
            with open(sql_path, 'r') as f:
                sql_template = f.read()

            # Format and execute the SQL
            sql = sql_template.format(table=table)
            cursor.execute(sql, (record_id,))
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
