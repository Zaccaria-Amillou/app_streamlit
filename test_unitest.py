# Import libraries
import unittest
import subprocess
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from app_test import preprocess, predict_sentiment  # Import predict_sentiment

# Define a test case class 
class TestApp(unittest.TestCase):
    # Test case to check if the preprocess function works correctly

    def test_docker_build(self):
        # Run the Docker build command
        result = subprocess.run(['docker', 'build', '-t', 'my-image', '.'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check that the Docker build command was successful
        self.assertEqual(result.returncode, 0, f"Docker build failed with error: {result.stderr.decode('utf-8')}")

    def test_preprocess(self):
        # Define a test input and expected output
        test_input = "This is a simple test tweet without a URL: http://test.com"
        expected_output = "simple test tweet without"

        # Call the preprocess function
        actual_output = preprocess(test_input)

        # Check that the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)

    # Test case to check if the predict_sentiment function works correctly
    def test_predict_sentiment(self):
        # Define a test input
        test_input = "This is a test tweet"

        # Call the predict_sentiment function
        sentiment = predict_sentiment(test_input)

        # Check that the sentiment is either 'POSITIVE' or 'NEGATIVE'
        self.assertIn(sentiment, ['POSITIVE', 'NEGATIVE'])

# Run the tests
if __name__ == '__main__':
    unittest.main()