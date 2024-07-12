from flask import Flask
from routes import setup_routes
from config import Config
import logging
from utils import db

app = Flask(__name__)
app.config.from_object(Config)

# setup routes with the app and database instance
setup_routes(app)

# configure logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
