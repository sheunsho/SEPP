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
#ABDOULAHI SECTION


def add_item_to_inventory(item_name):
    try:
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (item_name) VALUES (?)", (item_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Item ' {item_name}' already exists in inventory")
    finally:
        conn.close()

def get_inventory():

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT item_name FROM inventory")
    items = cursor.fetchall()
    conn.close()
    return [item[0] for item in items]

def add_recipe(recipe_name, ingredients):

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (recipe_name, ingredients) VALUES (?, ?)",
        (recipe_name, ','.join(ingredients))
    )
    conn.commit()
    conn.close() 

def get_recipes():

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_name, ingredients FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    return[{"recipe_name": row[0], "ingredients": row[1].split(',')} for row in recipes]

#TESTS
#if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # Test CRUD operations
    print("Adding items to inventory...")
    add_item_to_inventory("apple")
    add_item_to_inventory("milk")
    add_item_to_inventory("bread")

    print("Fetching inventory...")
    print(get_inventory())

    print("Adding recipes...")
    add_recipe("Apple Pie", ["apple", "flour", "sugar"])
    add_recipe("Milkshake", ["milk", "banana", "ice cream"])

    print("Fetching recipes...")
    print(get_recipes())


