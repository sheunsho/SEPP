import sqlite3

def initialize_database():
    """
    Initialize the database by executing schema.sql.
    """
    conn = sqlite3.connect("inventory.db")  # Create or connect to the database
    cursor = conn.cursor()

    # Read and execute the schema.sql file
    with open("schema.sql", "r") as file:
        sql_script = file.read()
        cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
