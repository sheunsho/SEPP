from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# Add the root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from src.cloud.database import fetch_inventory, add_to_inventory, get_matching_recipe, remove_from_inventory  # Import database functions
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

@app.route('/api/simulate', methods=['POST'])
def simulate_detection():
    try:
        # Ensure the request contains a JSON payload
        if not request.json:
            return jsonify({"error": "No JSON payload provided"}), 400

        # Extract image_folder from the payload, with a default value
        image_folder = request.json.get('image_folder', 'src/camera/')
        print(f"Image folder received: {image_folder}")  # Debugging log

        # Verify the image folder exists
        if not os.path.exists(image_folder):
            return jsonify({"error": f"Image folder not found: {image_folder}"}), 400

        # Proceed with simulation
        detected_items = detect_items_from_images(
            image_folder,
            model,
            datagen,
            confidence_threshold={
                0: 0.5,
                1: 0.4,
                2: 0.3
            },
            valid_food_keywords=[
                "apple", "orange", "banana", "carrot", "chicken", "beef", "milk",
                "bread", "cheese", "tomato", "potato", "lettuce", "grape", "onion",
                "pomegranate", "loaf", "bottle", "packaging", "meat"
            ],
            manual_mappings={
                "french loaf": "chicken breast",
                "roast": "chicken breast",
                "turkey breast": "chicken breast",
                "lotion": "milk",
                "pomegranate": "apple",
                "dough": "chicken breast"
            }
        )

        # Add detected items to inventory
        for item in detected_items:
            add_to_inventory(item, quantity=1)

        return jsonify({"detected_items": detected_items})
    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging log
        return jsonify({"error": str(e)}), 500


@app.route('/api/recipe', methods=['GET'])
def get_random_recipe():
    """
    API endpoint to fetch a random recipe based on available inventory.
    """
    try:
        recipe = get_matching_recipe()
        if "error" in recipe:
            return jsonify({"error": recipe["error"]}), 404
        return jsonify(recipe)
    except Exception as e:
        print(f"Error fetching recipe: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/inventory/<item_name>', methods=['DELETE'])
def remove_item(item_name):
    """
    API endpoint to remove an item or reduce its quantity from the inventory.
    """
    try:
        # Extract optional quantity from query parameters
        quantity = int(request.args.get('quantity', 1))  # Default to 1 if not provided
        remove_from_inventory(item_name, quantity)
        return jsonify({"message": f"{item_name} removed successfully."}), 200
    except Exception as e:
        print(f"Error removing item from inventory: {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
