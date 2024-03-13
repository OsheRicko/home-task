from flask import Flask

app = Flask(__name__)

@app.route('/')
def instructions():
    return """
    <h1>Weather Retrieval Instructions</h1>
    <p>To retrieve weather information, push the button next to the desired city below.</p>

    <button onclick="location.href='/weather/London';">Get Weather for London</button>
    <button onclick="location.href='/weather/TelAviv';">Get Weather for Tel Aviv</button>
    <button onclick="location.href='/weather/NewYork';">Get Weather for New York</button>
    """

@app.route('/weather/<city>')
def get_weather(city):
    # Your weather retrieval logic goes here
    # This route will handle requests for weather information for any specified city
    return f"Weather data for {city}"

if __name__ == '__main__':
    # Running Flask on 0.0.0.0 to bind to all network interfaces
    app.run(debug=False, host='0.0.0.0', port=80)
