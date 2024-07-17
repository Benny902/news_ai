# news_ai

## Personalized News Update Aggregator

### Overview and Idea

Dockerized microservice-based application, written mostly with Python Flask, that fetches most interesting news (by newsdata.io API) using user preferences and generates concise summaries using AI (Gemini API) and sends it to users via email, also utilizing Dapr and RabbitMQ.  


## How to run

```
docker-compose up --build
```

now the app with all its microservices should be running.

## How to test

- ## using integration test
to run the integration test: (cd integration_test)  
```
pytest -v test.py 
```

- ## using frontend
the app includes a frontend for easier testing and using at  ``` http://localhost:4000/ ``` (Click image to enlarge)
<img src="./images/frontend.png" alt="Click image to enlarge" width="300"  height="600">

- ## using only backend API  
#### example usage in postman / swagger / bash (curl) / etc:
(i've also included "postman_collection.json" for convenience)

use METHOD on http://localhost:5000/ with the following endpoints:  
>POST /register: to create a user  
POST /login: to login with user  
GET /profile: to show user profile  
PUT /profile: to edit preferences of the user  
GET /news: to show news based on user preferences  
GET /summary: to show summarized news based on user preferences  
GET /email: to email summarized news based on user preferences to users email  
GET /queue: to get an email from queue and process it.  
- (if /queue is not called, the emails will be processed from the queue automatically after 60 seconds.)

- for "POST /register" or "POST /login" you need to include json input.  
for example POST /login  
```
{  
    "username": "1234",  
    "password": "1234"  
}  
```
a successful login will return a token as response, we need that token for the other routes:  
for /profile, /news, /summary and /mail we need to put the token into Headers for example:  
```
curl -X PUT http://localhost:5000/profile \
     -H "Content-Type: application/json" \
     -H "Authorization: <your_token_here>" \
     -d '{
            "preferences": "Blockchain, Cybersecurity",
            "category_preferences": "Technology"
         }'
```
## Scheme

![!\[alt text\](scheme.png)  ](./images/scheme.png)
