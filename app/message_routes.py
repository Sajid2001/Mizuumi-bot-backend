from flask import request, jsonify
from app import app, messages
from _datetime import datetime
from chat import get_response
from bson.json_util import dumps
from auth import require_auth

@app.route("/respond",methods=["POST"])
@require_auth
def respond():

    #send message to bot and store in database
    text = request.get_json().get("text")
    sender = request.get_json().get("sender")
    user_id = request.user_id

    if not text:
        return jsonify({'error': 'You must enter a message'}), 400

    user_message = {
        "text":text,
        "timestamp": datetime.now(),
        "sender": sender,
        "user_id":user_id
    }
    messages.insert_one(user_message)

    #create response and send to the database
    response = get_response(text)
    mizuumi_message = {
        "text":response,
        "timestamp": datetime.now(),
        "sender":"Mizuumi",
        "user_id":user_id
    }

    messages.insert_one(mizuumi_message)
    mizuumi_message = dumps(mizuumi_message)
    return (mizuumi_message)


@app.route("/messages", methods=["GET"])
@require_auth
def get_messages():
    user_id = request.user_id
    data = list(messages.find({"user_id":user_id}).sort("_id", -1).limit(8))
    documents = dumps(data)
    return documents