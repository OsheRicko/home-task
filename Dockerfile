# Use a smaller base image
FROM python:3.9-alpine

# Create a non-root user
RUN adduser -D myuser
USER myuser

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
