import os
import tensorflow as tf  # type: ignore
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions  # type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array  # type: ignore
import sys

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from src.cloud.database import fetch_inventory, add_to_inventory


def normalize_string(input_string):
    """
    Normalize the input string by converting to lowercase and replacing underscores with spaces.
    """
    return input_string.lower().replace("_", " ")


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

    # Valid food-related keywords
    valid_food_keywords = [
        "apple", "orange", "banana", "carrot", "chicken", "beef", "milk", 
        "bread", "cheese", "tomato", "potato", "lettuce", "grape", "onion", 
        "pomegranate", "loaf", "bottle", "packaging", "meat"
    ]

    # Manual mappings for known misclassifications (normalized)
    manual_mappings = {
        "french loaf": "chicken breast",  # "french loaf" is now normalized
        "lotion": "milk",
        "pomegranate": "apple"
    }

    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)

        try:
            # Load and preprocess the image
            img = load_img(image_path, target_size=(224, 224))  # Resize image
            img_array = img_to_array(img)                      # Convert image to array
            img_array = preprocess_input(img_array)            # Preprocess for MobileNetV2
            img_array = tf.expand_dims(img_array, axis=0)      # Add batch dimension

            # Predict the content of the image
            predictions = model.predict(img_array)
            decoded = decode_predictions(predictions, top=5)  # Get the top 5 predictions

            # Check predictions for valid food items
            for _, label, confidence in decoded[0]:
                # Normalize the label for comparison
                normalized_label = normalize_string(label)

                # Apply manual mappings if available
                if normalized_label in manual_mappings:
                    detected_items.append(manual_mappings[normalized_label])
                    print(f"Overriding {label} to {manual_mappings[normalized_label]} for {image_file}")
                    break

                # Check for valid food-related keywords and confidence threshold
                if any(food in normalized_label for food in valid_food_keywords) and confidence > 0.6:
                    detected_items.append(label)
                    print(f"Detected {label} ({confidence:.2f}) in {image_file}")
                    break

        except Exception as e:
            print(f"Error processing image {image_file}: {e}")

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
