import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "This is C Application"

if __name__ == '__main__':
    PORT = os.environ.get('PORT', '7002')
    app.run(host='0.0.0.0', port=int(PORT))
