from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import logging
import os
import threading
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
    'B': 'http://news_service:5001',
    'C': 'http://email_service:5002'
}

# function to forward requests to a service
def forward_to_service(service, endpoint, method='GET', json_data=None, headers=None):
    url = SERVICE_URLS.get(service) + endpoint
    try:
        logger.info(f"Forwarding request to {url} with method {method}")
        response = requests.request(method=method, url=url, json=json_data, headers=headers)
        response.raise_for_status()
        logger.info(f"Received response from {url} with status code {response.status_code}")
        return response.json(), response.status_code
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        try:
            error_response = response.json()
            return jsonify(error_response), response.status_code
        except ValueError:
            return jsonify({"error": str(http_err)}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        return jsonify({"error": str(req_err)}), 500

@app.route('/register', methods=['POST'])
def register():
    logger.info("Register endpoint called")
    return forward_to_service('B', '/register', method='POST', json_data=request.get_json())

@app.route('/login', methods=['POST'])
def login():
    logger.info("Login endpoint called")
    return forward_to_service('B', '/login', method='POST', json_data=request.get_json())

@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    logger.info(f"Profile endpoint called with method {request.method}")
    headers = {'Authorization': request.headers.get('Authorization')}
    if request.method == 'GET':
        return forward_to_service('B', '/profile', method='GET', headers=headers)
    elif request.method == 'PUT':
        return forward_to_service('B', '/profile', method='PUT', headers=headers, json_data=request.get_json())

@app.route('/news', methods=['GET'])
def news():
    logger.info("News endpoint called")
    headers = {'Authorization': request.headers.get('Authorization')}
    return forward_to_service('B', '/news', method='GET', headers=headers)

@app.route('/summary', methods=['GET'])
def summary():
    logger.info("Summary endpoint called")
    headers = {'Authorization': request.headers.get('Authorization')}
    return forward_to_service('B', '/summary', method='GET', headers=headers)

@app.route('/email', methods=['GET'])
def email():
    logger.info("Email endpoint called")
    headers = {'Authorization': request.headers.get('Authorization')}
    thread = threading.Thread(target=process_and_send_email, args=(headers,))
    thread.start()
    return jsonify({"message": "processing summary, email with the summarized news will be sent soon"})

def process_and_send_email(headers):
    result_summary = process_summary(headers)
    logger.info(f"Processed summary result: {result_summary}")
    return result_summary

def process_summary(headers):
    return forward_to_service('B', '/email', method='GET', headers=headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
