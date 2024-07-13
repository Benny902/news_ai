from flask import Flask
from routes import setup_routes
import logging


app = Flask(__name__)

# setup routes with the app
setup_routes(app)

# configure logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
