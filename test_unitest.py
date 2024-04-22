# Import libraries
import unittest
import subprocess
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from app_test import preprocess, predict_sentiment  # Import predict_sentiment

# Defining a test case class 
class TestApp(unittest.TestCase):


    def test_docker_build(self):
        # Running the Docker build command
        result = subprocess.run(['docker', 'build', '-t', 'my-image', '.'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Checking that the Docker build command was successful
        self.assertEqual(result.returncode, 0, f"Docker build failed with error: {result.stderr.decode('utf-8')}")

    def test_preprocess(self):
        # Defining a test input and expected output
        test_input = "This is a simple test tweet without a URL: http://test.com"
        expected_output = "simple test tweet without"

        # Calling the preprocess function
        actual_output = preprocess(test_input)

        # Checking that the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)

    # Testing case to check if the predict_sentiment function works correctly
    def test_predict_sentiment(self):
        # Defining a test input
        test_input = "This is a test tweet"

        # Calling the predict_sentiment function
        sentiment = predict_sentiment(test_input)

        # Checking that the sentiment is either 'POSITIVE' or 'NEGATIVE'
        self.assertIn(sentiment, ['POSITIVE', 'NEGATIVE'])

# Running the tests
if __name__ == '__main__':
    unittest.main()