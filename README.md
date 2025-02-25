Multi-Container CRUD Application
================================

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
- `docker-compose.yml` (to manage services like MariaDB).
- `.env` (to store environment variables). Use `.env-template` as a reference. Don't use quotes or spaces.
  🔹 This ensures **MariaDB runs in a container** and is easy to start/stop.
  🔹 **Data persistence** is achieved using a named Docker volume (`mariadb_data_volume`).

---

## **5. Connect Python to MariaDB**

📌 **Milestone:** Write a Python script to connect to the database, run queries, and retrieve data.
📄 **File:** `db_connect.py`
🔹 This script will use a MariaDB library (`mysql-connector-python` or `SQLAlchemy`) to interact with the database.

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
