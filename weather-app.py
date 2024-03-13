from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = 'f0a146930b4d4d689e195332241303'
WEATHER_API_URL = 'https://api.weatherapi.com/v1/current.json'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/weather')
def get_weather():
    # Make a request to the weather API
    params = {'key': API_KEY, 'q': 'London'}  # Example location, you can change it
    response = requests.get(WEATHER_API_URL, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

if __name__ == '__main__':
    # Running Flask on 0.0.0.0 to bind to all network interfaces
    app.run(debug=False, host='0.0.0.0', port=80)
