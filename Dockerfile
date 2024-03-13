# Stage 1: Build the application
FROM python:3.9-slim AS builder

# Set the working directory in the builder stage
WORKDIR /app

# Copy only the Flask application code into the builder stage
COPY weather-app.py .

# Stage 2: Create the final lightweight image
FROM python:3.9-slim

# Set the working directory in the final stage
WORKDIR /app

# Copy only the built application from the builder stage
COPY --from=builder /app/weather-app.py .

# Install Flask and requests in the final stage
RUN pip install --no-cache-dir flask requests

# Expose port 5000 for Flask app
EXPOSE 5000

# Command to run the Flask application in the final stage
CMD ["python", "weather-app.py"]
