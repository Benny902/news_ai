from flask import Flask, request, jsonify
from mailjet_rest import Client
import os

app = Flask(__name__)

# this is a temporary free tier Mailjet API key and secret - therefore i dont mind publish it here. (and also my 2ndary mail).
api_key = 'adb10055ceda5647319bc649041afdd1'
api_secret = '4d9a911f10bb2bdb11908aeba4784c8a'
sender_email = 'Benny902e@gmail.com'

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

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

    result = mailjet.send.create(data=email_data)
    return jsonify({
        'status_code': result.status_code,
        'response': result.json()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)