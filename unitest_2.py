import unittest
import docker
from tensorflow.keras.preprocessing.sequence import pad_sequences
from app_test import preprocess, tokenizer, model

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = docker.from_env()

    def test_docker_build(self):
        # Build the Docker image
        self.client.images.build(path=".")

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

if __name__ == '__main__':
    unittest.main()