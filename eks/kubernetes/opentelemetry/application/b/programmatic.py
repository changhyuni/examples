import os
import time
import requests
from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)  # Enabled Programmatic Automatic 

C_HOST = os.environ.get('C_HOST', 'C')
C_PORT = os.environ.get('C_PORT', '7002')

@app.route('/')
def call_app_c():
    time.sleep(5)

    url = f'http://{C_HOST}:{C_PORT}/'
    message = "This is B Application"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        message += " " + resp.text
    except Exception as e:
        print(f"[C] Error calling C: {e}")
        message += " (Error calling C)"
    return message

if __name__ == '__main__':
    PORT = os.environ.get('PORT', '7001')
    app.run(host='0.0.0.0', port=int(PORT))
