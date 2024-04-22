# Using an official Python:3.8 runtime 
FROM python:3.8-slim-buster

# Setting the working directory in the container to /app
WORKDIR /app

# Adding the current directory contents into the container at /app
ADD . /app

# Installing any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Making port 8501 available to the world outside this container using streamlit default port
EXPOSE 8501

# Running app_test.py when the container launches
CMD streamlit run app_test.py