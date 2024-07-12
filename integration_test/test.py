import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture
def user():
    return {
        "username": "1234", 
        "password": "1234",
        "email": "benny902@gmail.com",
        "preferences": "Blockchain, Cybersecurity",
        "category_preferences": "Technology"
    }

@pytest.fixture
def token(user):
    # Register the user
    response = requests.post(f"{BASE_URL}/register", json=user)
    if response.status_code == 400 and "User already exists" in response.json().get("error", ""):
        print("User already exists. Proceeding with login.")
    else:
        assert response.status_code == 200
    
    # Login the user to get the token
    login_response = requests.post(f"{BASE_URL}/login", json={
        "username": user["username"], 
        "password": user["password"]
    })
    assert login_response.status_code == 200
    
    token = login_response.json().get("token")
    print(f"Token obtained: {token}")
    return token

def test_register(user):
    response = requests.post(f"{BASE_URL}/register", json=user)
    if response.status_code == 400 and "User already exists" in response.json().get("error", ""):
        print("User already exists. Test passed.")
    else:
        assert response.status_code == 200

def test_login(user):
    response = requests.post(f"{BASE_URL}/login", json={
        "username": user["username"], 
        "password": user["password"]
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_profile_get(token):
    headers = {"Authorization": token}
    print(f"Headers for profile GET: {headers}")
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200

def test_profile_put(token):
    headers = {"Authorization": token}
    new_preferences = {
        "preferences": "Blockchain, Cybersecurity, AI"
    }
    print(f"Headers for profile PUT: {headers}")
    response = requests.put(f"{BASE_URL}/profile", headers=headers, json=new_preferences)
    assert response.status_code == 200

def test_news(token):
    headers = {"Authorization": token}
    print(f"Headers for news: {headers}")
    response = requests.get(f"{BASE_URL}/news", headers=headers)
    assert response.status_code == 200

def test_summary(token):
    headers = {"Authorization": token}
    print(f"Headers for summary: {headers}")
    response = requests.get(f"{BASE_URL}/summary", headers=headers)
    assert response.status_code == 200

def test_email(token):
    headers = {"Authorization": token}
    print(f"Headers for email: {headers}")
    response = requests.get(f"{BASE_URL}/email", headers=headers)
    assert response.status_code == 200
    assert response.json().get("message") == "processing summary, email with the summarized news will be sent soon"

if __name__ == "__main__":
    pytest.main()
