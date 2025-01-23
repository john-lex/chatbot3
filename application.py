

from flask import Flask, request, jsonify
from twilio.rest import Client
import requests


app = Flask(__name__)


TWILIO_ACCOUNT_SID = "AC8e99c083b0c62298468ed0659949930b"
TWILIO_AUTH_TOKEN = "7ce7b6747b504ac137f228650aa34783"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+15186291413"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

rasa_url = "http://localhost:5005/webhooks/rest/webhook"

@app.route("/")
def home():
    return "servidor de flask corriendo"


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")


    response = requests.post(rasa_url, json={"sender": "user" , "message" : user_message })

    bot_response = response.json()
    messages = [message.get("text") for message in bot_response if "text" in message]

    return jsonify({"messages": messages})


@app.route("/whatsapp", methods=["POST"])
def chat_whatsapp():
    
    get_message = request.form.get("body")
    number_send = request.form.get("from")

    response_rasa = requests.post(rasa_url, json={"sender": number_send , "message" : get_message })


    bot_response = response_rasa.json()

    for response in bot_response:
        client.messages.create(
            from_ = TWILIO_WHATSAPP_NUMBER,
            to= number_send,
            body=response.get("text")
        )

    
    return jsonify({ "status" : "success"}), 200



if __name__ == "__main__":
      app.run(port=5000, debug=True)

