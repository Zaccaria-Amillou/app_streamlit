
from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.stem import WordNetLemmatizer
import pickle
import string
import re
import csv


import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

app = Flask(__name__)

abbreviations = {}
with open('input/abbreviations.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(':')
        abbreviations[key.strip()] = value.strip()

def preprocess(text):
    # Convert the tweet to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    # Remove HTML tags
    text = re.sub(r'<.*?>', ' ', text)
    # Remove punctuation
    text = "".join([x for x in text if x not in string.punctuation])
    # Tokenization
    tweet = text.split()
    # Lemmatization
    tweet = [lemmatizer.lemmatize(x) for x in tweet if x not in stop_words]
    # Remove the word "lol"
    tweet = [word for word in tweet if word != 'lol']
    # Remove the word "amp"
    tweet = [word for word in tweet if word != 'amp']
    # Remove the word "quot"
    tweet = [word for word in tweet if word != 'quot']
    # Remove the word URL
    tweet = [word for word in tweet if word != 'url']
    # Convertit les abréviations en anglais standard
    tweet = [abbreviations[word] if word in abbreviations else word for word in tweet]
    # Reconstruct the tweet
    tweet = " ".join(tweet)
    return tweet

# Load the tokenizer
with open('tokenizer/tokenizer_l_glo.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the model
model = load_model('model/model.h5')

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment = ''
    if request.method == 'POST':
        tweet_input = request.form.get('tweet')
        if tweet_input:
            # Preprocess the input
            data_prepocess = [preprocess(tweet_input)]
            
            # Tokenize and pad the input
            data_tok = pad_sequences(tokenizer.texts_to_sequences(data_prepocess), maxlen=100)
            
            # Make a prediction
            prediction = model.predict(data_tok)
            
            # Convert the prediction to 'POSITIVE' or 'NEGATIVE'
            sentiment = 'POSITIVE' if prediction[0][0] > 0.7 else 'NEGATIVE'
            
            # Return the sentiment as a JSON response
            return jsonify({'sentiment': sentiment})

    # If the request method is not POST, return an empty JSON response
    return jsonify({})

if __name__ == '__main__':
    app.run()

    