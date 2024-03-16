# Use a smaller base image
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY petition-app.py .
COPY templates /app/templates
COPY static /app/static

# Install required packages for connecting to SQL Server, Flask, and requests
RUN apk update && \
    apk add --no-cache unixodbc unixodbc-dev curl python3-dev build-base && \
    rm -rf /var/cache/apk/* && \
    pip install --no-cache-dir pyodbc flask requests

# Install msodbcsql18 driver package
RUN apk add --no-cache gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import - && \
    curl https://packages.microsoft.com/config/alpine/3.14/prod.list > /etc/apk/repositories && \
    apk update && \
    apk add --no-cache msodbcsql18

# Expose port 5000 for Flask app
EXPOSE 5000

# Create a non-root user to use least privilege
RUN adduser -D myuser

# Switch to the non-root user
USER myuser

# Define ARG for SQL connection string
ARG SQL_CONNECTION_STRING

# Set environment variable for SQL connection string
ENV SQL_CONNECTION_STRING=$SQL_CONNECTION_STRING

# Command to run the Flask application
CMD ["python", "petition-app.py"]
