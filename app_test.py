import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import csv
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging



nltk.download('stopwords')
nltk.download('wordnet')


logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=cc8b2f05-ca7d-4f53-9ffe-8fbf51e3ff78'))

# Preprocessing
def preprocess(text):
    stop_words = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    text_cleaning_re = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+|[-+]?\d*\.\d+|\d+"
    # Remove link,user and special characters
    text = re.sub(text_cleaning_re, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            tokens.append(lemmatizer.lemmatize(token))
    return " ".join(tokens)

# Load the tokenizer
with open('tokenizer/tokenizer_l_glo.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the model
model = load_model('model/model.h5')

st.title("Tweet Sentiment Prediction")

# Input text box for user to enter a tweet
tweet_input = st.text_input("Enter a tweet:")

if st.button("Predict"):
    if tweet_input:
        # Preprocess the input
        data_prepocess = [preprocess(tweet_input)]
        
        # Tokenize and pad the input
        data_tok = pad_sequences(tokenizer.texts_to_sequences(data_prepocess), maxlen=100)
        
        # Make a prediction
        prediction = model.predict(data_tok)
        
        # Convert the prediction to 'POSITIVE' or 'NEGATIVE'
        sentiment = 'POSITIVE' if prediction[0][0] > 0.7 else 'NEGATIVE'
        
        # Display the prediction
        st.write("Prediction:", sentiment)

        # Ask for user feedback
        feedback = None
        st.write("Was the prediction correct?")
        if st.button("Yes, it was correct"):
            feedback = "Yes"
        elif st.button("No, it wasn't correct"):
            feedback = "No"

        # Log the feedback to Application Insights
        if feedback is not None:
            logger.warning('User feedback', extra={'custom_dimensions': {'Tweet': tweet_input, 'Prediction': sentiment, 'Feedback': feedback}})

            if feedback == "Yes":
                st.write("Thank you for your feedback!")
            else:
                st.write("We're sorry to hear that. We'll use your feedback to improve our model.")