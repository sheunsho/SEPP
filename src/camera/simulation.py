import os
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array

import sys
import os

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from src.cloud.database import fetch_inventory, add_to_inventory

def detect_items_from_images():
    """
    Detect food items from images using MobileNetV2 pretrained model.
    Returns a list of detected item names.
    """
    # Get the absolute path to the images folder
    image_folder = os.path.join(os.path.dirname(__file__), "images")

    # Ensure the folder exists
    if not os.path.exists(image_folder):
        print(f"Image folder not found: {image_folder}")
        return []

    # Load the pretrained MobileNetV2 model
    model = MobileNetV2(weights="imagenet")
    detected_items = []

    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)

        # Load and preprocess the image
        img = load_img(image_path, target_size=(224, 224))  # Resize image
        img_array = img_to_array(img)                      # Convert image to array
        img_array = preprocess_input(img_array)            # Preprocess for MobileNetV2
        img_array = tf.expand_dims(img_array, axis=0)      # Add batch dimension

        # Predict the content of the image
        predictions = model.predict(img_array)
        decoded = decode_predictions(predictions, top=1)[0]  # Get the top prediction
        item_name = decoded[0][1]                            # Extract the label (name)
        detected_items.append(item_name)

    return detected_items

if __name__ == "__main__":
    # Fetch current inventory
    items = fetch_inventory()
    print("Current Inventory:", items)

    # Detect items from images
    detected_items = detect_items_from_images()
    if detected_items:
        print("Detected Items from Images:", detected_items)

        # Add detected items to the inventory
        for item in detected_items:
            add_to_inventory(item, quantity=1)
