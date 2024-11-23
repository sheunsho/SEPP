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
    
def fetch_all_items():
    """
    Fetch all items from the food_items table.
    Returns a list of tuples where each tuple represents a row.
    """
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items")  # Query all food items
    items = cursor.fetchall()  # Get all rows
    conn.close()
    return items

if __name__ == "__main__":
    initialize_database()
    items = fetch_all_items()
    print("Food Items:", items)