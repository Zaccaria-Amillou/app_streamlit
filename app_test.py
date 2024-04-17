import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
import csv
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging


nltk.download('wordnet')
nltk.download('stopwords')

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=cc8b2f05-ca7d-4f53-9ffe-8fbf51e3ff78'))

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
    # Reconstruct the tweet
    tweet = " ".join(tweet)
    return tweet

# # Preprocessing
# def preprocess(text):
#     stop_words = stopwords.words("english")
#     lemmatizer = WordNetLemmatizer()
#     text_cleaning_re = r"@\\S+|.*https?:\\S*.*|.*www\\.\\S*.*|[^A-Za-z0-9]+|[-+]?\\d*\\.\\d+|\\d+"
#     # Remove link,user and special characters
#     text = re.sub(text_cleaning_re, ' ', str(text).lower()).strip()
#     tokens = []
#     for token in text.split():
#         if token not in stop_words:
#             tokens.append(lemmatizer.lemmatize(token))
#     return " ".join(tokens)

def predict_sentiment(tweet):
    # Preprocess the input
    data_prepocess = [preprocess(tweet)]
    
    # Tokenize and pad the input
    data_tok = pad_sequences(tokenizer.texts_to_sequences(data_prepocess), maxlen=100)
    
    # Make a prediction
    prediction = model.predict(data_tok)
    
    # Convert the prediction to 'POSITIVE' or 'NEGATIVE'
    sentiment = 'POSITIVE' if prediction[0][0] > 0.7 else 'NEGATIVE'
    
    return sentiment

# Load the tokenizer
with open('tokenizer/tokenizer_l_glo.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the model
model = load_model('model/model.h5')

st.title("Tweet Sentiment Prediction")

# Input text box for user to enter a tweet
tweet_input = st.text_input("Enter a tweet:")

if 'feedback' not in st.session_state:
    st.session_state.feedback = None

if 'sentiment' not in st.session_state:
    st.session_state.sentiment = None

if st.button("Predict"):
    if tweet_input:
        # Call the predict_sentiment function
        st.session_state.sentiment = predict_sentiment(tweet_input)
        
        # Display the prediction
        st.write("Prediction:", st.session_state.sentiment)

# Ask for user feedback
st.write("Can you give us your feedback?")

if st.button("Yes, it was correct"):
    st.session_state.feedback = "Yes"
    # Log the feedback to Application Insights
    logger.warning('User feedback', extra={'custom_dimensions': {'Tweet': tweet_input, 'Prediction': st.session_state.sentiment, 'Feedback': st.session_state.feedback}})
    st.write("Thank you for your feedback!")
    # Rerun the app
    st.experimental_rerun()
elif st.button("No, it wasn't correct"):
    st.session_state.feedback = "No"
    # Log the feedback to Application Insights
    logger.warning('User feedback', extra={'custom_dimensions': {'Tweet': tweet_input, 'Prediction': st.session_state.sentiment, 'Feedback': st.session_state.feedback}})
    st.write("We're sorry to hear that. We'll use your feedback to improve our model.")
    # Rerun the app
    st.experimental_rerun()