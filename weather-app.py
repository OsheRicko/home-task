from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = 'f0a146930b4d4d689e195332241303'
WEATHER_API_URL = 'https://api.weatherapi.com/v1/current.json'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/weather/<city>')
def get_weather(city):
    # Make a request to the weather API
    params = {'key': API_KEY, 'q': city}
    response = requests.get(WEATHER_API_URL, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        formatted_weather = format_weather_data(weather_data)
        return jsonify(formatted_weather)
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

def format_weather_data(weather_data):
    current = weather_data.get('current', {})
    location = weather_data.get('location', {})
    
    formatted_weather = {
        'city': location.get('name', ''),
        'country': location.get('country', ''),
        'temperature_c': current.get('temp_c', ''),
        'temperature_f': current.get('temp_f', ''),
        'condition': current.get('condition', {}).get('text', ''),
        'humidity': current.get('humidity', ''),
        'wind_speed_kph': current.get('wind_kph', ''),
        'wind_speed_mph': current.get('wind_mph', ''),
        'wind_direction': current.get('wind_dir', ''),
        'last_updated': current.get('last_updated', ''),
    }
    
    return formatted_weather

if __name__ == '__main__':
    # Running Flask on 0.0.0.0 to bind to all network interfaces
    app.run(debug=False, host='0.0.0.0', port=80)
