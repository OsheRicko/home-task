# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY weather-app.py .

# Install Flask and dependencies
RUN pip install --no-cache-dir flask requests

# Expose port 5000 for Flask app
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "weather-app.py"]
