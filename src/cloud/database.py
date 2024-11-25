import sqlite3

def initialize_database():
    """
    Initialise the database by executing schema.sql.
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
    
def fetch_all_items(table_name):
    """
    Fetch all items from the specified table.
    """
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}"  # Query for the specified table
    cursor.execute(query)
    items = cursor.fetchall()
    conn.close()
    return items

if __name__ == "__main__":
    initialize_database()  # Initialise the database

    # Ask the user which table they want to fetch data from
    table_name = input("Enter the table name to fetch data from: ").strip()

    try:
        items = fetch_all_items(table_name)  # Fetch data from the specified table
        print(f"Data from '{table_name}':", items)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}. Check if the table '{table_name}' exists.")
