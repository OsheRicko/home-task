import requests
from flask import Flask, render_template

app = Flask(__name__)

# Define the API key for weatherapi.com
API_KEY = 'f0a146930b4d4d689e195332241303'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/weather/<city>')
def get_weather(city):
    # Make a request to weatherapi.com to get weather data for the specified city
    url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Extract the weather data from the response
        data = response.json()
        weather = {
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'humidity': data['current']['humidity']
        }
        return render_template('weather.html', **weather)
    else:
        return 'Error fetching weather data'

if __name__ == '__main__':
    # Running Flask on 0.0.0.0 to bind to all network interfaces
    app.run(debug=False, host='0.0.0.0', port=80)
