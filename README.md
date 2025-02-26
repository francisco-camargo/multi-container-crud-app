Multi-Container CRUD Application
================================

# Purpose

This project is designed for educational purposes. It aims to help you learn how to:

- Set up and configure Docker containers.
- Create and manage a MariaDB database.
- Connect a Python application to a MariaDB database.
- Perform CRUD (Create, Read, Update, Delete) operations using SQL and Python.

# Citation Instructions

If you use this repository in your work, please cite it as follows:

**GitHub Repository**: [multi-container-crud-app](https://github.com/francisco-camargo/multi-container-crud-app)

**Suggested Citation**:

* Author: Francisco Camargo
* Title: Multi-Container CRUD Application
* Source: https://github.com/francisco-camargo/multi-container-crud-app
* Date Accessed:

Please ensure proper attribution when using or modifying this work.

# Roadmap

## **1. Define the Database Schema**

📌 **Milestone:** Create a SQL script to define the database structure (tables, relationships, constraints).

📄 **File:** `schema.sql`

🔹 This file will contain `CREATE TABLE` statements for your **three tables**.

---

## **2. Set Up Sample Data**

📌 **Milestone:** Create a SQL script to insert test data into the tables.

📄 **File:** `seed.sql`

🔹 This file will contain `INSERT INTO` statements with **dummy data** to test queries.

---

## **3. Create Initialization Script**

📌 **Milestone:** Create a SQL script to control the order of running other SQL scripts.

📄 **File:** `init.sql`

🔹 This file will source `schema.sql` and `seed.sql` in the desired order.

---

## **4. Configure Docker for MariaDB**

📌 **Milestone:** Create a Docker environment to run MariaDB.

📄 **Files:**

- `Dockerfile` (to define the MariaDB container setup).
- `docker-compose.yaml` (to manage services like MariaDB).
- `.env` (to store environment variables). Use `.env-template` as a reference. Don't use quotes or spaces.

🔹 This ensures **MariaDB runs in a container** and is easy to start/stop.

🔹 **Data persistence** is achieved using a named Docker volume (`mariadb_data_volume`).

See section "How to Instantiate the MariaDB Container" to run the project at this stage.

---

## **5. Connect Python to MariaDB**

📌 **Milestone:** Write a Python script to run on the host machine to connect to the database, run queries, and retrieve data.

📄 **File:** `src/db_connect.py`

🔹 This script will use a MariaDB library (`mariadb`) to interact with the database. I chose `mariadb` over `sqlalchemy` because I will use SQL scripts instead of using ORM functionality so `mariadb` will suffice.

🔹 **Running the Script:**

1. **Install Dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

   **Run the Script**:
   Ensure that the MariaDB container is running before executing the script.

   ```sh
   python src/db_connect.py
   ```

This will connect to the MariaDB instance running in the Docker container and print a success message if the connection is established.

---

## **6. Run Migrations & Seed Data**

📌 **Milestone:** Automate database setup with Python.

📄 **File:** `setup_db.py`

🔹 This script will:

✅ Create the database (if it doesn’t exist).

✅ Run `init.sql` to create tables and insert test data.

---

## **7. Test Queries & CRUD Operations**

📌 **Milestone:** Write Python scripts to test `SELECT`, `INSERT`, `UPDATE`, and `DELETE` queries.

📄 **Files:**

- `query_tests.py` (test queries).
- `crud_operations.py` (Python functions for Create, Read, Update, Delete).

---

## **8. Containerize the Python App (Optional)**

📌 **Milestone:** Run your Python scripts inside a Docker container.

📄 **File:** `Dockerfile` (for Python container).

🔹 This allows your **Python app** to run in a container alongside MariaDB.

---

## **Next Steps**

Once these files and milestones are in place, you’ll be able to:

✅ Start and stop your database with **Docker**.

✅ Run Python scripts to **insert, update, and query data**.

✅ Easily deploy or share your setup.

# How to Instantiate the MariaDB Container

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/francisco-camargo/multi-container-crud-app.git
    cd multi-container-crud-app
    ```

2. **Create the `.env` File**:
    Copy the `.env-template` file to `.env` and fill in the required environment variables.
    ```sh
    cp .env-template .env
    ```

3. **Build and Start the MariaDB Container**:
    Use Docker Compose to build and start the MariaDB container.
    ```sh
    docker compose up --build -d
    ```

4. **Stop the MariaDB Container**:
    To stop the MariaDB container, use the following command:
    ```sh
    docker compose down
    ```

5. **Access the MariaDB Container**:
    To access the MariaDB container, use the following command:
    ```sh
    docker exec -it mariadb_container bash
    ```

    To enter MariaDB run
    ```sh
    mariadb -u user -puserpassword
    ```

    Or, alternatively, run
    ```sh
    docker exec -it mariadb_container mariadb -u user -puserpassword
    ```

    Either way, once you are in the MariaDB program, you can verify that the database is up by running
    ```sh
    SHOW DATABASES;

    >>>
    +--------------------+
    | Database           |
    +--------------------+
    | crud_db            |
    | information_schema |
    +--------------------+
    ```

* `information_schema`: A system database that contains metadata about the database server and its objects. It is automatically created and managed by MariaDB.
* `crud_db`: A user-defined database created for your application to store your application's data. The name is defined in `.env`