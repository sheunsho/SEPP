#CREATED SPRINT 1, LAST EDITED SPRINT 2 
#CONTROLS THE DATABSE OF RECIPES AND INGREDIENTS

import os
import sqlite3
from typing import List, Dict
import random

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

            # Combine duplicate entries
            cursor.execute("SELECT SUM(quantity) FROM inventory WHERE item_name = ?", (item_name,))
            total_quantity = cursor.fetchone()[0]

            if total_quantity:
                # Update the existing entry
                cursor.execute(
                    "UPDATE inventory SET quantity = ? WHERE item_name = ?",
                    (total_quantity + quantity, item_name)
                )
                print(f"Updated {item_name} total quantity to {total_quantity + quantity}.")
            else:
                # Insert new entry
                cursor.execute(
                    "INSERT INTO inventory (item_name, quantity) VALUES (?, ?)",
                    (item_name, quantity)
                )
                print(f"Added {item_name} to inventory.")
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

def get_matching_recipe() -> Dict[str, List[str]]:
    """
    Return a random recipe that can be made using ingredients in the inventory.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Fetch inventory items and their quantities
            cursor.execute("SELECT item_name, quantity FROM inventory")
            inventory = {row[0]: row[1] for row in cursor.fetchall()}

            # Fetch all recipes
            cursor.execute("SELECT recipe_name, ingredients FROM recipes")
            recipes = cursor.fetchall()

            # Find recipes that can be made with available inventory
            matching_recipes = []
            for recipe_name, ingredients in recipes:
                ingredient_list = ingredients.split(',')
                can_make = True
                for ingredient in ingredient_list:
                    if ingredient not in inventory or inventory[ingredient] <= 0:
                        can_make = False
                        break
                if can_make:
                    matching_recipes.append({"recipe_name": recipe_name, "ingredients": ingredient_list})

            # Return a random matching recipe, if any
            if matching_recipes:
                return random.choice(matching_recipes)
            else:
                return {"error": "No recipes can be made with the available ingredients."}

    except Exception as e:
        print(f"Error fetching matching recipe: {e}")
        return {"error": str(e)}
    
def populate_sample_recipes():
    """Add sample recipes to the database."""
    recipes = [
        ("Pasta", ["pasta", "tomato sauce", "cheese"]),
        ("Sandwich", ["bread", "lettuce", "tomato", "cheese"]),
        ("Salad", ["lettuce", "tomato", "cucumber", "olive oil"]),
        ("Omelette", ["egg", "milk", "cheese"]),
        ("Grilled Cheese", ["bread", "cheese", "butter"]),
    ]

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for recipe_name, ingredients in recipes:
                cursor.execute(
                    "INSERT OR IGNORE INTO recipes (recipe_name, ingredients) VALUES (?, ?)",
                    (recipe_name, ','.join(ingredients))
                )
            print("Sample recipes added successfully.")
    except Exception as e:
        print(f"Error populating sample recipes: {e}")
    

if __name__ == "__main__":
    import argparse

    # Initialize the database
    initialize_database()

    # Command-line argument parser
    parser = argparse.ArgumentParser(description="Recipe Finder CLI")
    parser.add_argument("--get-recipe", action="store_true", help="Find a recipe based on available inventory")
    parser.add_argument("--populate-recipes", action="store_true", help="Populate the database with sample recipes")
    args = parser.parse_args()

    if args.populate_recipes:
        populate_sample_recipes()
    elif args.get_recipe:
        recipe = get_matching_recipe()
        if "error" not in recipe:
            print(f"\nRecipe: {recipe['recipe_name']}")
            print(f"Ingredients: {', '.join(recipe['ingredients'])}\n")
        else:
            print(f"\n{recipe['error']}\n")


