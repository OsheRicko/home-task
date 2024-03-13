# Stage 1: Build the application
FROM python:3.9-slim AS builder

# Set the working directory in the builder stage
WORKDIR /app

# Copy the Flask application code into the builder stage
COPY weather-app.py .

# Install Flask and dependencies in the builder stage
RUN pip install --no-cache-dir flask requests

# Stage 2: Create the final lightweight image
FROM python:3.9-slim

# Copy the built application from the builder stage
COPY --from=builder /app /app

# Set the working directory in the final stage
WORKDIR /app

# Expose port 5000 for Flask app
EXPOSE 5000

# Command to run the Flask application in the final stage
CMD ["python", "weather-app.py"]
