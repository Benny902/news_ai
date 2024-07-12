import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'benny_secret_key')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://db:27017/')
    DB_NAME = os.environ.get('DB_NAME', 'user_db')

    NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'pub_481851327244a72b345ba689fc6897ca6d2a9')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyCcAup4i8Kt6hXKSF0DH5mtpVs6LLZxoCU')