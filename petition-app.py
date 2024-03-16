from flask import Flask, jsonify, request, render_template, redirect, url_for
import os
import pyodbc

app = Flask(__name__)

# Get SQL connection string from environment variable
SQL_CONNECTION_STRING = os.getenv('SQL_CONNECTION_STRING')

def create_table():
    try:
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        cursor = conn.cursor()
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
        print("Database error:", e)
        return False

# Call the create_table function when the application starts
create_table()

@app.route('/')
def welcome():
    return render_template('welcome.html')

def execute_query(query, params=None):
    try:
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Database error:", e)
        return False

@app.route('/add-name', methods=['GET'])
def add_name_form():
    return render_template('add_name.html')

@app.route('/get-names', methods=['GET'])
def get_names():
    try:
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM data")
        rows = cursor.fetchall()
        conn.close()
        names = [row[0] for row in rows]
        return render_template('signed_names.html', names=names)
    except Exception as e:
        print("Database error:", e)
        return jsonify({'error': 'Failed to retrieve names from the database'}), 500

@app.route('/names', methods=['POST'])
def add_name():
    try:
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({'error': 'Name is required'}), 400

        query = "INSERT INTO data (name) VALUES (?)"
        params = (name,)
        if execute_query(query, params):
            return redirect(url_for('thanks'))  # Redirect to thanks.html
        else:
            return jsonify({'error': 'Failed to insert name into the database'}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=80, debug=False)
