#CREATED SPRINT 1, LAST EDITED SPRINT 2 
#CONTROLS THE DATABSE OF RECIPES AND INGREDIENTS

import os
import sqlite3
from typing import List, Dict

# Get the path to the database file
db_path = os.path.join(os.path.dirname(__file__), "inventory.db")
schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

def initialize_database():
    """Initialize database by executing the schema.sql script."""
    try:
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, "r") as file:
                sql_script = file.read()
                conn.executescript(sql_script)
            print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

def fetch_inventory() -> List[Dict[str, int]]:
    """Fetch items from the inventory table."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT item_name, quantity FROM inventory")
            items = cursor.fetchall()
        return [{"item_name": item[0], "quantity": item[1]} for item in items]
    except Exception as e:
        print(f"Error fetching inventory: {e}")
        return []

def add_to_inventory(item_name: str, quantity: int = 1):
    """Add item to the inventory or update its quantity if it already exists."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Check if the item already exists in the inventory
            cursor.execute("SELECT quantity FROM inventory WHERE item_name = ?", (item_name,))
            result = cursor.fetchone()

            if result:
                new_quantity = result[0] + quantity
                cursor.execute(
                    "UPDATE inventory SET quantity = ? WHERE item_name = ?",
                    (new_quantity, item_name)
                )
                print(f"Updated {item_name} quantity to {new_quantity}.")
            else:
                cursor.execute(
                    "INSERT INTO inventory (item_name, quantity) VALUES (?, ?)",
                    (item_name, quantity)
                )
                print(f"Added {item_name} to inventory")
    except Exception as e:
        print(f"Error adding to inventory: {e}")
    
def remove_from_inventory(item_name: str, quantity: int = 1):
    """" Remove an item from the inventory or reduce quantity """

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT quantity FROM inventory WHERE item_name = ?", (item_name,))
            result = cursor.fetchone()

            if result:
                current_quantity = result[0]
                if current_quantity > quantity:
                    new_quantity = current_quantity - quantity
                    cursor.execute(
                        "UPDATE inventory SET quantity = ? WHERE item_name = ?",
                        (new_quantity, item_name)
                    )
                    print(f"Reduced {item_name} quantity to {new_quantity}")
                else:
                    cursor.execute(
                        "DELETE FROM inventory WHERE item_name = ?",
                        (item_name,)
                    )
                    print(f"Removed {item_name} from inventory")
            else:
                print(f"Removed {item_name} from inventory")
    except Exception as e:
        print(f"Error removing from inventory: {e}")


def add_recipe(recipe_name: str, ingredients: List[str]):
    """Add recipe to the recipe table."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Check if the recipe already exists
            cursor.execute("SELECT recipe_name FROM recipes WHERE recipe_name = ?", (recipe_name,))
            result = cursor.fetchone()

            if result:
                print(f"Recipe '{recipe_name}' already exists.")
            else:
                cursor.execute(
                    "INSERT INTO recipes (recipe_name, ingredients) VALUES (?, ?)",
                    (recipe_name, ','.join(ingredients))
                )
                print(f"Added recipe: {recipe_name}")
    except Exception as e:
        print(f"Error adding recipe: {e}")

def remove_recipe(recipe_name: str):
    """Remove a recipe from the recipes table."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT recipe_name FROM recipes WHERE recipe_name = ?", (recipe_name,))
            result = cursor.fetchone()

            if result:
                cursor.execute("DELETE FROM recipes WHERE recipe_name = ?", (recipe_name,))
                print(f"Removed recipe: {recipe_name}")
            else:
                print(f"Recipe '{recipe_name}' not found.")
    except Exception as e:
        print(f"Error removing recipe: {e}")


def get_recipes() -> List[Dict[str, List[str]]]:
    """Fetch all the recipes from the database."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT recipe_name, ingredients FROM recipes")
            recipes = cursor.fetchall()
        return [{"recipe_name": row[0], "ingredients": row[1].split(',')} for row in recipes]
    except Exception as e:
        print(f"Error fetching recipes: {e}")
        return []

def fetch_food_items() -> List[str]:
    """Fetch all food items from food_items."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT item_name FROM food_items")
            items = cursor.fetchall()
        return [item[0] for item in items]
    except Exception as e:
        print(f"Error fetching food items: {e}")
        return []

# TESTS
if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # Test CRUD operations
    print("Fetching food items...")
    print(fetch_food_items())

    print("Adding items to inventory...")
    add_to_inventory("apple", 3)  # Add or update inventory
    add_to_inventory("milk", 2)   # Add or update inventory
    add_to_inventory("bread", 1)  # Add to inventory

    print("Fetching inventory...")
    print(fetch_inventory())

    print("Adding recipes...")
    add_recipe("Grilled Cheese Sandwich", ["bread", "cheese", "butter"])
    add_recipe("Omelette", ["eggs", "milk", "butter"])

    print("Fetching recipes...")
    print(get_recipes())

    print("Removing items from inventory...")
    remove_from_inventory("apple", 2)  # Reduce quantity
    remove_from_inventory("milk")      # Remove item completely
    remove_from_inventory("butter")    # Item not in inventory

    print("Removing recipes...")
    remove_recipe("Grilled Cheese Sandwich")  # Remove existing recipe
    remove_recipe("Nonexistent Recipe")      # Recipe not in database
