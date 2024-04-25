import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=cc8b2f05-ca7d-4f53-9ffe-8fbf51e3ff78'))
st.title("Tweet Sentiment Prediction")

# Input text box for user to enter a tweet
tweet_input = st.text_input("Enter a tweet:")

@st.cache_data
def get_sentiment(tweet):
    # Send a POST request to the Flask app with the tweet text
    response = requests.post('http://20.76.117.141:5000', data={'tweet': tweet})

    # Parse the JSON response
    response_json = json.loads(response.text)

    # Get the sentiment prediction from the response
    sentiment = response_json.get('sentiment', '')
    return sentiment

if st.button("Predict"):
    if tweet_input:
        sentiment = get_sentiment(tweet_input)
        st.write(f"Sentiment: {sentiment}")

# Ask for user feedback
st.write("Can you give us your feedback?")

# Feedback buttons
if st.button("Yes, it was correct"):
    feedback = "Yes"
    # Log the feedback to Application Insights
    logger.warning('User feedback', extra={'custom_dimensions': {'Tweet': tweet_input, 'Prediction': sentiment, 'Feedback': feedback}})
    st.write("Thank you for your feedback!")
    # Rerun the app
    st.experimental_rerun()
elif st.button("No, it wasn't correct"):
    feedback = "No"
    # Log the feedback to Application Insights
    logger.warning('User feedback', extra={'custom_dimensions': {'Tweet': tweet_input, 'Prediction': sentiment, 'Feedback': feedback}})
    st.write("We're sorry to hear that. We'll use your feedback to improve our model.")
    # Rerun the app
    st.experimental_rerun()