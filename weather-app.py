from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = 'f0a146930b4d4d689e195332241303'
WEATHER_API_URL = 'https://api.weatherapi.com/v1/current.json'

@app.route('/')
def instructions():
    return """
    <h1>Weather Retrieval Instructions</h1>
    <p>To retrieve weather information, make a GET request to /weather/city_name, replacing 'city_name' with the name of the city for which you want to fetch weather data.</p>
    <p>Example: /weather/London</p>
    """

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
        'City': location.get('name', ''),
        'Country': location.get('country', ''),
        'Temperature (C)': current.get('temp_c', ''),
        'Temperature (F)': current.get('temp_f', ''),
        'Condition': current.get('condition', {}).get('text', ''),
        'Humidity': current.get('humidity', ''),
        'Wind Speed (kph)': current.get('wind_kph', ''),
        'Wind Speed (mph)': current.get('wind_mph', ''),
        'Wind Direction': current.get('wind_dir', ''),
        'Last Updated': current.get('last_updated', ''),
    }
    
    return formatted_weather

if __name__ == '__main__':
    # Running Flask on 0.0.0.0 to bind to all network interfaces
    app.run(debug=False, host='0.0.0.0', port=80)
