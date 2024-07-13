import requests
from retrying import retry
from flask import request
from auth import decode_token
from bson.objectid import ObjectId
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()


# MongoDB connection setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

how_many_news_to_get = 5 # can be adjusted
preferredLanguage ="english" # i can edit later the preferences of the user to include language preferences - for now can change manually


def json_serialize(obj):
    """Convert MongoDB document to a JSON-serializable format."""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: json_serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_serialize(i) for i in obj]
    return obj


def get_user_data():
    token = request.headers.get("Authorization")
    if not token:
        return {"error": "Missing Authorization token"}, 401
    user_id = decode_token(token)
    if not user_id:
        return {'error': 'Invalid token'}, 403
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return {'error': 'User not found'}, 404
    return user, 200, user_id


# helper function for both /news and /summary to eliminate duplicate code for fetching newsdata
def fetch_news(user):
    preferences = user.get('preferences', '')
    category_preferences = user.get('category_preferences', '')
    try: # https://newsdata.io/api/1/news?apikey=pub_481851327244a72b345ba689fc6897ca6d2a9&q=Blockchain%20Cyber%20security&category=education,technology 
        response = requests.get(f'https://newsdata.io/api/1/news?&apiKey={NEWS_API_KEY}&q={preferences}&category={category_preferences}')
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get("results", [])
        
        if len(articles) > how_many_news_to_get:
            selected_articles = select_top_articles(articles, preferences)
            return selected_articles
        else:
            return articles
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Error fetching news articles: {e}")
    
# if fetch_news gives more than 5 articles (can be adjust on 'how_many_news_to_get') then get only top 5 bases on user preferences using gemini
def select_top_articles(articles, preferences):
    try: 
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        article_texts = "\n\n".join([article['description'] for article in articles])
        data = { # need to build this data for the text because this is how the gemini api wants to get the data in the POST request
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Based on the user preferences '{preferences}', select and list {how_many_news_to_get} most relevant articles from the following:\n\n{article_texts}"
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            selected_article_descriptions = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
            selected_articles = []
            for description in selected_article_descriptions.split('\n'):
                for article in articles:
                    if description in article['description']:
                        selected_articles.append(article)
                        if len(selected_articles) == how_many_news_to_get:
                            break
                if len(selected_articles) == how_many_news_to_get:
                    break
            return selected_articles
        else:
            raise requests.exceptions.RequestException(
                f"Error selecting top articles: {response.status_code} - {response.text}"
            )
    except Exception as e:
        raise requests.exceptions.RequestException(f"Error selecting top articles: {e}")
    

# summarize with gemini AI - function for both /news and /summary to eliminate duplicate code
@retry(stop_max_attempt_number=3)
def summarize_article(link):
    """Summarizes an article's description using the Gemini API and returns the summary string."""
    try:
        if not link:
            raise ValueError("Missing 'link' in link data")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Summarize the following article in few rows, focusing on the main points and key details, in {preferredLanguage}:\n\n{link}"
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text") # the response invloves a complex json, i just need the "text" from there
        else:
            raise requests.exceptions.RequestException(
                f"Error summarizing article: {response.status_code} - {response.text}"
            )
    except Exception as e:
        raise requests.exceptions.RequestException(f"Error summarizing article: {e}")
