import os
import sqlite3

# Get the path to the database file
db_path = os.path.join(os.path.dirname(__file__), "inventory.db")

def initialize_database():
    """
    Initialize the database by executing schema.sql.
    """
    print("initialize_database function started")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Read and execute the schema.sql file
        schema_path = os.path.join(os.path.dirname(__file__), "../../schema.sql")
        if not os.path.exists(schema_path):
            print(f"Schema file not found at: {schema_path}")
            return

        print(f"Schema file found at: {schema_path}")
        with open(schema_path, "r") as file:
            sql_script = file.read()
            print("Executing SQL script:")
            print(sql_script)
            cursor.executescript(sql_script)

        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def fetch_inventory():
    """
    Fetch all items from the inventory table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM inventory"
    cursor.execute(query)
    items = cursor.fetchall()
    conn.close()
    return items

def add_to_inventory(item_name, quantity=1):
    """
    Add an item to the inventory or update its quantity if it already exists.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the item already exists in the inventory
    cursor.execute("SELECT quantity FROM inventory WHERE item_name = ?", (item_name,))
    result = cursor.fetchone()

    if result:
        # If the item exists, update the quantity
        new_quantity = result[0] + quantity
        cursor.execute(
            "UPDATE inventory SET quantity = ? WHERE item_name = ?", (new_quantity, item_name)
        )
        print(f"Updated {item_name} quantity to {new_quantity}.")
    else:
        # If the item doesn't exist, insert it
        cursor.execute(
            "INSERT INTO inventory (item_name, quantity) VALUES (?, ?)", (item_name, quantity)
        )
        print(f"Added {item_name} to the inventory.")

    conn.commit()
    conn.close()

# Add this at the end of the file
if __name__ == "__main__":
    initialize_database()
