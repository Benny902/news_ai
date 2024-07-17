from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import threading
import requests


app = Flask(__name__)

# enable CORS for the frontend to work locally 
CORS(app)

# set up logs
if not os.path.exists('/app/logs'):
    os.makedirs('/app/logs')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    handlers=[
                        logging.FileHandler("/app/logs/app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# URLs of the current additional services
SERVICE_URLS = {
    'B': 'news_service',
    'C': 'email_service'
}

# function to forward requests to a service (updated to do it via Dapr url)
def forward_to_service(service, endpoint, method='GET', json_data=None, headers=None):
    service = SERVICE_URLS.get(service)
    dapr_url = f'http://localhost:3500/v1.0/invoke/{service}/method{endpoint}'
    try:
        logger.info(f"Forwarding request to {dapr_url} with method {method} and data {json_data}")
        response = requests.request(method=method, url=dapr_url, json=json_data, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        response.raise_for_status()
        response_data = response.json()
        logger.info(f"Received response data: {response_data}")
        return response_data, response.status_code
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        try:
            error_response = response.json()
            logger.error(f"Error response data: {error_response}")
            return error_response, response.status_code
        except ValueError:
            return {"error": str(http_err)}, response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        return {"error": str(req_err)}, 500

@app.route('/register', methods=['POST'])
def register():
    logger.info("Register endpoint called")
    data, status_code = forward_to_service('B', '/register', method='POST', json_data=request.get_json())
    return jsonify(data), status_code

@app.route('/login', methods=['POST'])
def login():
    logger.info("Login endpoint called")
    data, status_code = forward_to_service('B', '/login', method='POST', json_data=request.get_json())
    return jsonify(data), status_code

@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    logger.info(f"Profile endpoint called with method {request.method}")
    headers = {'Authorization': request.headers.get('Authorization')}
    if request.method == 'GET':
        data, status_code = forward_to_service('B', '/profile', method='GET', headers=headers)
    elif request.method == 'PUT':
        data, status_code = forward_to_service('B', '/profile', method='PUT', headers=headers, json_data=request.get_json())
    return jsonify(data), status_code

@app.route('/news', methods=['GET'])
def news():
    logger.info("News endpoint called")
    headers = {'Authorization': request.headers.get('Authorization')}
    data, status_code = forward_to_service('B', '/news', method='GET', headers=headers)
    return jsonify(data), status_code

@app.route('/summary', methods=['GET'])
def summary():
    logger.info("Summary endpoint called")
    headers = {'Authorization': request.headers.get('Authorization')}
    data, status_code = forward_to_service('B', '/summary', method='GET', headers=headers)
    return jsonify(data), status_code

@app.route('/email', methods=['GET'])
def email():
    logger.info("Email endpoint called")
    headers = {'Authorization': request.headers.get('Authorization')}
    thread = threading.Thread(target=process_and_send_email, args=(headers,))
    thread.start()
    return jsonify({"message": "processing summary, email with the summarized news will be sent soon"})

def process_and_send_email(headers):
    with app.app_context():
        result_summary = process_email(headers)
        logger.info(f"Processed summary result: {result_summary}")

def process_email(headers):
    data, status_code = forward_to_service('B', '/email', method='GET', headers=headers)
    return data

@app.route('/queue', methods=['GET'])
def queue():
    logger.info("Queue endpoint called")
    data, status_code = forward_to_service('C', '/queue', method='GET')
    return jsonify(data), status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
