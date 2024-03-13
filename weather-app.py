from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = 'f0a146930b4d4d689e195332241303'
WEATHER_API_URL = 'https://api.weatherapi.com/v1/current.json'

@app.route('/')
def instructions():
    return """
    <h1>Weather Retrieval Instructions</h1>
    <p>To retrieve weather information, push the button next to the desired city below or make a GET request to /weather/city_name, replacing 'city_name' with the name of the city for which you want to fetch weather data.</p>
    <p>Example: /weather/London</p>
    <button onclick="location.href='/weather/London';">Get Weather for London</button>
    <button onclick="location.href='/weather/TelAviv';">Get Weather for Tel Aviv</button>
    <button onclick="location.href='/weather/NewYork';">Get Weather for New York</button>
    """

@app.route('/weather/<city>')
def get_weather(city):
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