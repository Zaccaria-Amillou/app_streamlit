# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make port 5000 available to the world outside this container for Flask app
# Make port 8501 available to the world outside this container for Streamlit app
EXPOSE 5000 8501

# Run supervisord when the container launches
CMD ["/usr/bin/supervisord"]