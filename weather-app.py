from flask import Flask, jsonify
import pyodbc
import os

app = Flask(__name__)

# Get SQL connection string from environment variable
SQL_CONNECTION_STRING = os.getenv('SQL_CONNECTION_STRING')

def test_db_connection():
    try:
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        conn.close()
        return True
    except Exception as e:
        print("Connection error:", e)
        return False

@app.route('/')
def check_db_connection():
    if test_db_connection():
        return "good"
    else:
        return "bad"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
