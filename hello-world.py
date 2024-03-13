from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Running Flask on 0.0.0.0 to bind to all network interfaces
    app.run(debug=False, host='0.0.0.0', port=80)
