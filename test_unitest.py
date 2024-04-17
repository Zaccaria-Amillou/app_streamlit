# Import libraries
import unittest
from app_test import preprocess, predict_sentiment  # Import predict_sentiment

# Define a test case class 
class TestApp(unittest.TestCase):
    # Test case to check if the preprocess function works correctly
    def test_preprocess(self):
        # Define a test input and expected output
        test_input = "This is a test tweet with a link: https://example.com and a user: @user"
        expected_output = "test tweet link user"

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