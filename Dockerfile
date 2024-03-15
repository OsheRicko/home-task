# Use a smaller base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY weather-app.py .

# Install required packages for connecting to SQL Server, Flask, and requests
RUN apt-get update && \
    apt-get install -y --no-install-recommends unixodbc unixodbc-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir pyodbc flask requests

# Expose port 5000 for Flask app
EXPOSE 5000

# Define ARG for SQL connection string
ARG SQL_CONNECTION_STRING

# Set environment variable for SQL connection string
ENV SQL_CONNECTION_STRING=$SQL_CONNECTION_STRING

# Command to run the Flask application
CMD ["python", "weather-app.py"]
