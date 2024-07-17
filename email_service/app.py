from flask import Flask, request, jsonify
from mailjet_rest import Client
import os, pika, json, requests
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

# this is a temporary free tier Mailjet API key and secret - therefore i dont mind publish it here. (and also my 2ndary mail).
api_key = os.getenv("MAILJET_API_KEY")
api_secret = os.getenv("MAILJET_API_SECRET")
sender_email = os.getenv("SENDER_EMAIL")

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# RabbitMQ
rabbitmq_host = 'rabbitmq'
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue', durable=True)
    return channel


@app.route('/send', methods=['POST'])
def send_email():
    data = request.json
    recipient_email = data.get('recipient_email')
    username = data.get('recipient_username')
    subject = data.get('subject', 'Your email subject')
    text_part = data.get('text_part', 'Greetings from Mailjet!')
    html_part = data.get('html_part', '<h3>Dear recipient, welcome to Mailjet!</h3><br />May the delivery force be with you!')

    email_data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Benny_News_AI"
                },
                "To": [
                    {
                        "Email": recipient_email,
                        "Name": username
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    # put email data into RabbitMQ queue instead of directly sending it ( mailjet.send.create(data=email_data) )
    channel = get_rabbitmq_channel()
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(email_data))
    print("Email queued:", email_data)
    return jsonify({'status': 'email queued', 'email_data': email_data})


# route to manually process emails from the queue (1 by 1 by their order)
@app.route('/queue', methods=['GET'])
def process_email_queue():
    channel = get_rabbitmq_channel()

    # get the number of messages in the queue
    method_frame, properties, body = channel.basic_get('email_queue', auto_ack=True)

    if method_frame:
        email_data = json.loads(body) # get email data from the queue
        result = mailjet.send.create(data=email_data) # send the email using Mailjet
        print("Email sent:", result.status_code, result.json())
        return jsonify({'status': 'email processed', 'email_data': email_data})
    else:
        return jsonify({'status': 'queue empty'})

# background scheduler to call /queue every 60 seconds (releasing a queue every 60 seconds)
scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: requests.get('http://localhost:5002/queue'), trigger='interval', seconds=60)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)