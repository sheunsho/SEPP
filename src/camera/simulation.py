import os
import sys
import tensorflow as tf  # type: ignore
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions  # type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array  # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from src.cloud.database import fetch_inventory, add_to_inventory

# Configuration constants
VALID_FOOD_KEYWORDS = [
    "apple", "orange", "banana", "carrot", "chicken", "beef", "milk",
    "bread", "cheese", "tomato", "potato", "lettuce", "grape", "onion",
    "pomegranate", "loaf", "bottle", "packaging", "meat"
]
MANUAL_MAPPINGS = {
    "french loaf": "chicken breast",
    "roast": "chicken breast",
    "turkey breast": "chicken breast",
    "lotion": "milk",
    "pomegranate": "apple",
    "dough": "chicken breast"
}
CONFIDENCE_THRESHOLD = {0: 0.5, 1: 0.4, 2: 0.3}  # Dynamic confidence thresholds

def normalize_string(input_string):
    """
    Normalize the input string by converting to lowercase and replacing underscores with spaces.
    """
    return input_string.lower().replace("_", " ")

def preprocess_image(image_path, datagen):
    """
    Preprocess and augment the image.
    """
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    augmented = datagen.random_transform(img_array)
    return tf.expand_dims(augmented, axis=0)

def predict_image(model, image_array, confidence_threshold, valid_food_keywords, manual_mappings):
    """
    Predict the content of the image using the model and map predictions to valid food items.
    """
    predictions = model.predict(image_array)
    decoded = decode_predictions(predictions, top=5)

    top_predictions = []
    for i, (_, label, confidence) in enumerate(decoded[0]):
        normalized_label = normalize_string(label)
        if confidence > confidence_threshold.get(i, 0.2):
            if normalized_label in manual_mappings:
                top_predictions.append((manual_mappings[normalized_label], confidence))
            elif normalized_label in valid_food_keywords:
                top_predictions.append((normalized_label, confidence))

    return max(top_predictions, key=lambda x: x[1]) if top_predictions else None

def detect_items_from_images(image_folder, model, datagen, confidence_threshold, valid_food_keywords, manual_mappings):
    """
    Detect food items from images in the specified folder.
    """
    detected_items = []
    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        try:
            image_array = preprocess_image(image_path, datagen)
            best_prediction = predict_image(
                model, image_array, confidence_threshold, valid_food_keywords, manual_mappings
            )
            if best_prediction:
                detected_items.append(best_prediction[0])
                print(f"Image: {image_file}, Detected: {best_prediction[0]} ({best_prediction[1]:.2f})")
            else:
                print(f"Image: {image_file}, Could not identify any food item.")
        except Exception as e:
            print(f"Error processing image {image_file}: {e}")
    return detected_items

def main():
    # Fetch current inventory
    items = fetch_inventory()
    print("Current Inventory:", items)

    # Detect items from images
    image_folder = os.path.join(os.path.dirname(__file__), "images")
    if not os.path.exists(image_folder):
        print(f"Image folder not found: {image_folder}")
        return

    datagen = ImageDataGenerator(
        horizontal_flip=True,
        brightness_range=[0.8, 1.2]
    )
    model = MobileNetV2(weights="imagenet")

    detected_items = detect_items_from_images(
        image_folder,
        model,
        datagen,
        CONFIDENCE_THRESHOLD,
        VALID_FOOD_KEYWORDS,
        MANUAL_MAPPINGS
    )

    if detected_items:
        print("Detected Items from Images:", detected_items)

        # Add detected items to the inventory
        for item in detected_items:
            add_to_inventory(item, quantity=1)

if __name__ == "__main__":
    main()
