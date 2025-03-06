from src.initialize_db import initialize_database
from src.show_data import show_table_data


def main():
    initialize_database()
    tables = ['users', 'posts', 'comments']
    for table in tables:
        show_table_data(table)


if __name__ == "__main__":
    main()