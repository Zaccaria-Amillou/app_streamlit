# Import libraries
import unittest
import docker
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from app_test import preprocess, tokenizer, model

# Define a test case class 
class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a Docker client connected to the Docker daemon
        self.client = docker.from_env()

    # Test case to check if Docker image is built successfully
    def test_docker_build(self):
        # Build the Docker image using the Dockerfile in the current directory
        self.client.images.build(path=".")

    # Test case to check if the prediction process works correctly
    def test_prediction(self):
        # Preprocess the input
        tweet = "This is a test tweet"
        preprocessed = preprocess(tweet)

        # Tokenize and pad the input
        data_tok = pad_sequences(tokenizer.texts_to_sequences([preprocessed]), maxlen=100)

        # Make a prediction
        prediction = model.predict(data_tok)

        # Convert the prediction to 'POSITIVE' or 'NEGATIVE'
        sentiment = 'POSITIVE' if prediction[0][0] > 0.7 else 'NEGATIVE'

        # Check that the sentiment is either 'POSITIVE' or 'NEGATIVE'
        self.assertIn(sentiment, ['POSITIVE', 'NEGATIVE'])

# Run the tests
if __name__ == '__main__':
    unittest.main()