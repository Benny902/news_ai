from flask import request, jsonify
from bson.objectid import ObjectId
import requests
from auth import generate_token
import utils
from utils import db

def setup_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Invalid input'}), 400
        if db.users.find_one({'username': data['username']}):
            return jsonify({'error': 'User already exists'}), 400
        additional_fields = {key: value for key, value in data.items() if key not in ['username', 'password']}
        user_id = db.users.insert_one({'username': data['username'], 'password': data['password'], **additional_fields}).inserted_id
        return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201

    # login endpoint
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = db.users.find_one({'username': data['username'], 'password': data['password']})
        if user:
            token = generate_token(user['_id'])
            return jsonify({'token': token}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    

    # profile endpoint
    @app.route('/profile', methods=['GET', 'PUT'])
    def profile():
        user, status_code, user_id = utils.get_user_data()
        if status_code != 200:
            return jsonify(user), status_code

        if request.method == 'PUT':
            data = request.get_json()
            db.users.update_one({'_id': ObjectId(user_id)}, {'$set': data})
            
        return jsonify({
            'username': user['username'],
            'email': user.get('email', ''),
            'preferences': user.get('preferences', ''),
            'category_preferences': user.get('category_preferences', '')
        }), 200
    

    @app.route('/news', methods=['GET'])
    def fetch_news_route():
        user, status_code, user_id = utils.get_user_data()
        if status_code != 200:
            return jsonify(user), status_code
        try:
            articles = utils.fetch_news(user)

            result = []
            for article in articles:
                header = article.get('title')
                link = article.get('link')
                result.append({
                    'header': header,
                    'link': link,
                })
            return jsonify({'articles': result}), 200
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Failed to fetch news: {str(e)}'}), 500


    @app.route('/summary', methods=['GET'])
    def summarize_route():
        user, status_code, user_id = utils.get_user_data()
        if status_code != 200:
            return jsonify(user), status_code

        try:
            articles = utils.fetch_news(user)

            summaries = []
            for article in articles:
                header = article.get("title")
                link = article.get("link")

                try:
                    summary = utils.summarize_article(link)
                    summaries.append({"header": header, "link": link, "summary": summary})
                except requests.exceptions.RequestException as e:
                    summaries.append({"header": header, "link": link, "summary": f"Error summarizing article: {e}"})

            return jsonify({"articles": summaries}), 200

        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Error fetching news articles or summarizing: {e}"}), 500


    @app.route('/email', methods=['GET'])
    def email_summary_route():
        user, status_code, user_id = utils.get_user_data()
        if status_code != 200:
            return jsonify(user), status_code

        email = user.get('email', '') 
        username = user.get('username', '') 
        import re # email validation using regular expression
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            return jsonify({"error": "Invalid email address format"}), 400  
        try:
            articles = utils.fetch_news(user)

            summaries = []
            for article in articles:
                header = article.get("title")
                link = article.get("link")

                try:
                    summary = utils.summarize_article(link)
                    summaries.append({"header": header, "link": link, "summary": summary})
                except requests.exceptions.RequestException as e:
                    summaries.append({"header": header, "link": link, "summary": f"Error summarizing article: {e}"})

            summary_json = {"articles": summaries}

            # prepare the HTML content with summaries for nice visual mail instead of json mail
            articles_html = ""
            for article in summary_json['articles']:
                articles_html += f"<h4>{article['header']}</h4>"
                articles_html += f"<p>{article['summary']}</p>"
                articles_html += f"<a href='{article['link']}'>Read more</a><br><br>"

            # call the email service to send the ready email
            email_service_url = 'http://email_service:5002/send'
            email_data = {
                "recipient_email": email,
                "recipient_username": username,
                "subject": "Your Summary",
                "text_part": "Here is your summary.",
                "html_part": f"<h3>Your Summary</h3><pre>{articles_html}</pre>"
            }
            response = requests.post(email_service_url, json=email_data)
            if response.status_code != 200:
                return jsonify({"error": "Failed to send email"}), 500

            adjusted_summary_json = {
                "message": "email sent with the summarized news",
                "articles": summary_json["articles"]
            }
            return jsonify(adjusted_summary_json)

        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Error fetching news articles or summarizing: {e}"}), 500