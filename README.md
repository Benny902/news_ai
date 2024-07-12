# news_ai

## Personalized News Update Aggregator

### Overview and Idea

The project aims to develop a microservice-based application that aggregates news
and technology updates based on user preferences. The system will fetch the latest
news, pick up most interesting news using AI based on user preferences (optionally
generate concise summaries using AI), and send this information to users via email,
Telegram, or other communication channels.


## How to run

```
docker-compose up --build
```

now the app with all its microservices should be running.

## How to test

- using integration test
to run the integration test: (cd integration_test)  
```
pytest -v test.py 
```

- using frontend
the app includes a frontend for easier testing and using at  ``` http://localhost:4000/ ```  

- using only backend API  
#### example usage in postman / swagger / etc:
i've also included "postman_collection.json" that you can use to test each route individually with the different order numbers as you wish.  

METHOD on http://localhost:5000/ with the following endpoints:  
>POST /register: to create a user  
POST /login: to login with user  
GET /profile: to show user profile  
PUT /profile: to edit preferences of the user  
GET /news: to show news based on user preferences  
GET /summary: to show summarized news based on user preferences  
GET /email: to email summarized news based on user preferences to users email  

for "POST /register" or "POST /login" you need to include json input.  
for example POST /login  
>{  
    "username": "1234",  
    "password": "1234"  
}  

a successful login will return a token as response, we need that token for the other routes:  
for /profile, /news, /summary and /mail we need to put the token into Headers for example:  
>curl -X PUT http://localhost:5000/profile \\  
     -H "Content-Type: application/json" \\  
     -d '{  
            "preferences": "Blockchain, Cybersecurity",  
            "category_preferences": "Technology"  
         }'  

## Scheme

![!\[alt text\](scheme.png)  ](./images/scheme.png)
