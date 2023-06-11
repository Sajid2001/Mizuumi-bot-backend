from flask import request, jsonify
from app import app, messages
from _datetime import datetime
from chat import get_response
from bson.json_util import dumps
from bson import ObjectId

@app.route("/respond",methods=["POST"])
def respond():

    #send message to bot and store in database
    text = request.get_json().get("text")
    sender = request.get_json().get("sender")

    if text == "":
        return jsonify({'error': 'You must enter a message'}), 400

    user_message = {
        "text":text,
        "timestamp": datetime.now(),
        "sender": sender
    }
    messages.insert_one(user_message)

    #create response and send to the database
    response = get_response(text)
    mizuumi_message = {
        "text":response,
        "timestamp": datetime.now(),
        "sender":"Mizuumi"
    }

    messages.insert_one(mizuumi_message)
    mizuumi_message = dumps(mizuumi_message)
    return (mizuumi_message)


@app.route("/messages", methods=["GET"])
def get_messages():
    data = list(messages.find().sort("_id", -1).limit(8))
    documents = dumps(data)
    return documents