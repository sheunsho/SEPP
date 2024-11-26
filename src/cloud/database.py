import os
import sqlite3

# Get the path to the database file
db_path = os.path.join(os.path.dirname(__file__), "inventory.db")

def initialize_database():
    """
    Initialize the database by executing schema.sql.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read and execute the schema.sql file
    schema_path = os.path.join(os.path.dirname(__file__), "../../schema.sql")
    with open(schema_path, "r") as file:
        sql_script = file.read()
        cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

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
