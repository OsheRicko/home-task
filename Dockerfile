# Use the official Python image as a base image
FROM python:3.9-slim AS base

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY hello-world.py .

# Install Flask and dependencies
RUN pip install --no-cache-dir flask

# Expose port 5000 for Flask app
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "hello-world.py"]

# Second stage for optimization
FROM base AS release

# No need to do anything here for now
