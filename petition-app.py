from flask import Flask, jsonify, request, render_template, redirect, url_for
import os
import pyodbc

app = Flask(__name__)

# Retrieve SQL connection string from environment variable
SQL_CONNECTION_STRING = os.getenv('SQL_CONNECTION_STRING')

# Function to create a table if it doesn't exist
def create_table():
    try:
        # Establish connection
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Execute SQL command to create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        # Print database error if any
        print("Database error:", e)
        return False

# Call the create_table function when the application starts
create_table()

# Welcome route
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Function to execute SQL query
def execute_query(query, params=None):
    try:
        # Establish connection
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Execute SQL query with optional parameters
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        # Print database error if any
        print("Database error:", e)
        return False

# Route to display form to add a name
@app.route('/add-name', methods=['GET'])
def add_name_form():
    return render_template('add_name.html')

# Route to retrieve names from the database
@app.route('/get-names', methods=['GET'])
def get_names():
    try:
        # Establish connection
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Execute SQL query to select names
        cursor.execute("SELECT name FROM data")
        rows = cursor.fetchall()
        conn.close()
        
        # Extract names from rows
        names = [row[0] for row in rows]
        return render_template('signed_names.html', names=names)
    except Exception as e:
        # Print database error if any
        print("Database error:", e)
        return jsonify({'error': 'Failed to retrieve names from the database'}), 500

# Route to add a name to the database
@app.route('/names', methods=['POST'])
def add_name():
    try:
        # Retrieve name from JSON request
        data = request.get_json()
        name = data.get('name')

        # Return error if name is not provided
        if not name:
            return jsonify({'error': 'Name is required'}), 400

        # Execute SQL query to insert name into the database
        query = "INSERT INTO data (name) VALUES (?)"
        params = (name,)
        if execute_query(query, params):
            return redirect(url_for('thanks'))  # Redirect to thanks.html on success
        else:
            return jsonify({'error': 'Failed to insert name into the database'}), 500
    except Exception as e:
        # Print error if any
        print("Error:", e)
        return jsonify({'error': 'Internal server error'}), 500

# Route to display a thank you message
@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

if __name__ == '__main__':
    # Create table if it doesn't exist and run the Flask app
    create_table()
    app.run(host='0.0.0.0', port=80, debug=False)
