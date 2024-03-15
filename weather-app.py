from flask import Flask, jsonify
import pyodbc
import os

app = Flask(__name__)

# Get SQL connection string from environment variable
SQL_CONNECTION_STRING = os.getenv('SQL_CONNECTION_STRING')

# Establish a connection to the Azure SQL Database
def get_sql_connection():
    try:
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        return conn
    except Exception as e:
        print(f"Error connecting to SQL Database: {str(e)}")
        return None

# Endpoint to retrieve data from a table in the database
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        conn = get_sql_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM YourTableName")
            data = cursor.fetchall()
            conn.close()
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
