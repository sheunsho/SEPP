import unittest
from unittest.mock import patch, MagicMock
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from src.camera.simulation import (
    normalize_string,
    preprocess_image,
    predict_image,
    detect_items_from_images,
    VALID_FOOD_KEYWORDS,
    MANUAL_MAPPINGS,
    CONFIDENCE_THRESHOLD
)

class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.image_folder = "test_images"
        self.valid_food_keywords = VALID_FOOD_KEYWORDS
        self.manual_mappings = MANUAL_MAPPINGS
        self.confidence_threshold = CONFIDENCE_THRESHOLD
        self.datagen = ImageDataGenerator(horizontal_flip=True, brightness_range=[0.8, 1.2])
        self.model = MagicMock()
        self.model.predict.return_value = np.zeros((1, 1000))  # Ensure valid shape for predict

    def test_normalize_string(self):
        self.assertEqual(normalize_string("French_Loaf"), "french loaf")
        self.assertEqual(normalize_string("TurkeyBreast"), "turkeybreast")

    @patch("tensorflow.keras.preprocessing.image.load_img")
    @patch("tensorflow.keras.preprocessing.image.img_to_array")
    def test_preprocess_image(self, mock_img_to_array, mock_load_img):
        mock_load_img.return_value = MagicMock()  # Mock PIL Image object
        mock_img_to_array.return_value = np.zeros((224, 224, 3))  # Mock image array
        image_array = preprocess_image("test_image.jpg", self.datagen)
        self.assertEqual(image_array.shape, (1, 224, 224, 3))


    def test_predict_image_valid(self):
        with patch("tensorflow.keras.applications.mobilenet_v2.decode_predictions") as mock_decode_predictions:
            mock_decode_predictions.return_value = [[
                ("n123", "apple", 0.7),
                ("n456", "carrot", 0.4),
                ("n789", "dough", 0.1)
            ]]
            result = predict_image(
                self.model,
                tf.zeros((1, 224, 224, 3)),
                self.confidence_threshold,
                self.valid_food_keywords,
                self.manual_mappings
            )
            self.assertEqual(result[0], "apple")

    def test_predict_image_manual_mapping(self):
        with patch("tensorflow.keras.applications.mobilenet_v2.decode_predictions") as mock_decode_predictions:
            mock_decode_predictions.return_value = [[
                ("n123", "french loaf", 0.6), # should map to chicken breast fingers crossed
                ("n456", "carrot", 0.3),
                ("n789", "dough", 0.1)
            ]]
            result = predict_image(
                self.model,
                tf.zeros((1, 224, 224, 3)),
                self.confidence_threshold,
                self.valid_food_keywords,
                self.manual_mappings
            )
            self.assertEqual(result[0], "chicken breast")

    @patch("os.listdir")
    @patch("src.camera.simulation.preprocess_image")
    @patch("src.camera.simulation.predict_image")
    def test_detect_items_from_images(self, mock_predict_image, mock_preprocess_image, mock_listdir):
        mock_listdir.return_value = ["image1.jpg", "image2.jpg"]
        mock_preprocess_image.return_value = tf.zeros((1, 224, 224, 3))
        mock_predict_image.side_effect = [("apple", 0.6), ("banana", 0.7)]

        detected_items = detect_items_from_images(
            self.image_folder,
            self.model,
            self.datagen,
            self.confidence_threshold,
            self.valid_food_keywords,
            self.manual_mappings
        )
        self.assertEqual(detected_items, ["apple", "banana"])

if __name__ == "__main__":
    unittest.main()
