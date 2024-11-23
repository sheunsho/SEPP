import sqlite3
import random

def fetch_all_items():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM food_items")  # Fetch only the names
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items

def detectItems():
    allPossibleItems = fetch_all_items()
    detectedItems = random.sample(allPossibleItems, random.randint(3, 7))
    return detectedItems
