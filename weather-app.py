from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Assuming SQL_PASS is an environment variable containing the password
SQL_PASS = os.getenv('SQL_PASS')

# Properly format the connection string
SQL_CONNECTION_STRING = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:assignment-app-sql-server.database.windows.net,1433;Database=assignment-app-db;Uid=sqluser;Pwd={Password1234!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

API_KEY = 'f0a146930b4d4d689e195332241303'
WEATHER_API_URL = 'https://api.weatherapi.com/v1/current.json'

@app.route('/')
def instructions():
    return f"SQL Connection String: {SQL_CONNECTION_STRING}\n {SQL_PASS}"

@app.route('/weather/<city>')
def get_weather(city):
    # Replace dashes with spaces in the city name
    city = city.replace('-', ' ')
    
    # Make a request to the weather API
    params = {'key': API_KEY, 'q': city}
    response = requests.get(WEATHER_API_URL, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        formatted_weather = format_weather_data(weather_data)
        return formatted_weather
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

def format_weather_data(weather_data):
    current = weather_data.get('current', {})
    location = weather_data.get('location', {})
    
    # Format weather information nicely
    formatted_weather = f"<h2>Weather Information for {location.get('name', '')}</h2>"
    formatted_weather += "<table border='1'>"
    formatted_weather += f"<tr><td>Temperature (C)</td><td>{current.get('temp_c', '')}</td></tr>"
    formatted_weather += f"<tr><td>Condition</td><td>{current.get('condition', {}).get('text', '')}</td></tr>"
    formatted_weather += f"<tr><td>Humidity</td><td>{current.get('humidity', '')}</td></tr>"
    formatted_weather += f"<tr><td>Wind Speed (km/h)</td><td>{current.get('wind_kph', '')}</td></tr>"
    formatted_weather += "</table>"
    
    return formatted_weather

if __name__ == '__main__':
    # Running Flask on 0.0.0.0 to bind to all network interfaces
    app.run(debug=False, host='0.0.0.0', port=80) 
