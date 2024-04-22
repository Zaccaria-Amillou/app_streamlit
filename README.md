# Sentiment Analysis Streamlit App

This repository contains a Streamlit application for sentiment analysis. The application uses a pre-trained TensorFlow model to predict the sentiment of a given text.

## Notebook
The notebook folder contains the EDA, the first modelisation and a test with a BERT model.

If you want to test the modelisation part you'll have to download the glove.6b.300d.txt
```bash
wget http://nlp.stanford.edu/data/glove.6B.zip
```
Then you can unzip the file into the input folder
```bash
unzip glove.6B.zip glove.6B.300d.txt -d input
```

## Application Structure

- `app_test.py`: This is the main application file. It contains the Streamlit application and the code for preprocessing the input and making predictions with the model.

- `tokenizer/tokenizer_l_glo.pkl`: This file contains the pre-trained tokenizer used to tokenize the input text.

- `model/model.h5`: This file contains the pre-trained TensorFlow model used to make predictions.

## Preprocessing

The application preprocesses the input text by removing links, usernames, special characters, and stop words, and by lemmatizing the words. The preprocessing function is defined in `app_test.py`.

## Model

The application uses a pre-trained TensorFlow model to make predictions. The model is loaded from `model/model.h5` in `app_test.py`.

## Running the Application

To run the application, you need to have Streamlit and TensorFlow installed. You can install them with pip:

```bash
pip install streamlit tensorflow
```
Then, you can run the application with the following command:
```bash
streamlit run app_test.py
```

The application will be accessible in your web browser at localhost:8501.

## Docker

A Dockerfile is included for building a Docker image of the application. You can build the image with the following command:
```bash
docker build -t streamlit_app .
```

And run a container from the image with this command:
```bash
docker run -p 8501:8501 streamlit_app
```

The application will be accessible in your web browser at localhost:8501.