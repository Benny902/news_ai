import jwt
from datetime import datetime, timedelta
import logging

import os
from dotenv import load_dotenv
load_dotenv()

def generate_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        logging.error("Invalid token.")
        return None
