from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import sqlite3
from src.cloud.database import get_recipes

# Add the root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from src.cloud.database import fetch_inventory, add_to_inventory  # Import database functions
from src.camera.simulation import detect_items_from_images  # Import simulation functions
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

app = Flask(__name__)
CORS(app)

# Initialize model and data generator once (to reuse across requests)
model = MobileNetV2(weights="imagenet")
datagen = ImageDataGenerator(horizontal_flip=True, brightness_range=[0.8, 1.2])

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    inventory = fetch_inventory()
    return jsonify(inventory)

@app.route('/api/inventory', methods=['POST'])
def add_item():
    data = request.json
    item_name = data.get('item_name')
    quantity = data.get('quantity', 1)
    add_to_inventory(item_name, quantity)
    return jsonify({"item_name": item_name, "quantity": quantity})

import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
from src.cloud.database import fetch_inventory, add_to_inventory

app = Flask(__name__)
CORS(app)

# Add project root to sys.path so src module can be found
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

# Initialize the MobileNetV2 model once (to reuse across requests)
model = MobileNetV2(weights="imagenet")

import os
from PIL import Image

def is_valid_image(image_path):
    """
    Check if the image is valid using Pillow's verify() method.
    """
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify the image
        return True
    except (IOError, SyntaxError) as e:
        print(f"Invalid image file: {image_path}, Error: {e}")
        return False

def detect_items_from_images(image_folder):
    """
    Detect food items from images using MobileNetV2 pretrained model.
    Returns a list of detected item names.
    """
    detected_items = []

    # Ensure the folder exists
    if not os.path.exists(image_folder):
        print(f"Image folder not found: {image_folder}")
        return []

    # Supported image file extensions
    valid_extensions = ['.jpg', '.jpeg', '.png']

    for root, dirs, files in os.walk(image_folder):
        for image_file in files:
            image_path = os.path.join(root, image_file)

            # Skip non-image files (e.g., Python files, directories, or system files)
            if not any(image_path.lower().endswith(ext) for ext in valid_extensions):
                print(f"Skipping non-image file: {image_file}")
                continue  # Skip non-image files

            print(f"Processing image: {image_path}")

            # Check if the image is valid before processing it
            if not is_valid_image(image_path):
                continue  # Skip invalid image files

            try:
                img = load_img(image_path, target_size=(224, 224))  # Resize image
                img_array = img_to_array(img)
                img_array = preprocess_input(img_array)
                img_array = tf.expand_dims(img_array, axis=0)

                predictions = model.predict(img_array)
                decoded = decode_predictions(predictions, top=1)[0]
                item_name = decoded[0][1]
                detected_items.append(item_name)

            except Exception as e:
                print(f"Error processing image {image_file}: {e}")

    return detected_items

def get_recipes():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT recipe_name, ingredients FROM recipes")
            recipes = cursor.fetchall()
        return [{"recipe_name": row[0], "ingredients": row[1].split(',')} for row in recipes]
    except Exception as e:
        print(f"Error fetching recipes: {e}")
        return []


@app.route('/api/simulate', methods=['POST'])
def simulate_detection():
    # Get the image folder from the request body
    image_folder = request.json.get('image_folder', 'src/camera')  # Default to 'src/camera'

    print(f"Image folder received: {image_folder}")

    try:
        detected_items = detect_items_from_images(image_folder)

        # Add detected items to inventory
        for item in detected_items:
            add_to_inventory(item, quantity=1)

        return jsonify({"detected_items": detected_items})

    except Exception as e:
        print(f"Error during simulation: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    inventory = fetch_inventory()
    return jsonify(inventory)

@app.route('/api/inventory', methods=['POST'])
def add_item():
    data = request.json
    item_name = data.get('item_name')
    quantity = data.get('quantity', 1)
    add_to_inventory(item_name, quantity)
    return jsonify({"item_name": item_name, "quantity": quantity})

@app.route('/api/recipes', methods=['GET'])
def get_recipe_suggestions():
    try:
        inventory = fetch_inventory()  # Get inventory from the database
        inventory_ingredients = set(item['item_name'] for item in inventory)
        
        recipes = get_recipes()  # Get all recipes
        suggested_recipes = []

        for recipe in recipes:
            recipe_name = recipe['recipe_name']
            recipe_ingredients = set(recipe['ingredients'].split(','))

            if recipe_ingredients.issubset(inventory_ingredients):
                suggested_recipes.append(recipe_name)

        return jsonify({"suggested_recipes": suggested_recipes})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error fetching recipes"}), 500


if __name__ == "__main__":
    app.run(debug=True)



if __name__ == "__main__":
    app.run(debug=True)
