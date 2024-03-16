# Use a smaller base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY petition-app.py .
COPY templates /app/templates
COPY static /app/static

# Install required packages for connecting to SQL Server, Flask, and requests
RUN apt-get update && \
    apt-get install -y --no-install-recommends unixodbc unixodbc-dev curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir pyodbc flask requests

# Install msodbcsql18 driver package
RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Expose port 5000 for Flask app
EXPOSE 5000

# Define ARG for SQL connection string
ARG SQL_CONNECTION_STRING

# Set environment variable for SQL connection string
ENV SQL_CONNECTION_STRING=$SQL_CONNECTION_STRING

# Command to run the Flask application
CMD ["python", "petition-app.py"]

 
