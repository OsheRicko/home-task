# Stage 1: Build environment
FROM python:3.9-slim AS build

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY weather-app.py .

# Create a directory for templates
RUN mkdir templates

# Copy the HTML file into the templates directory
COPY templates/weather.html templates/

# Install Flask and requests module
RUN pip install --no-cache-dir flask requests

# Stage 2: Production environment
FROM python:3.9-slim AS production

# Set the working directory in the container
WORKDIR /app

# Copy only necessary files from the build stage
COPY --from=build /app .

# Expose port 5000 for Flask app
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "weather-app.py"]
