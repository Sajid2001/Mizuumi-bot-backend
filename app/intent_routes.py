from app import app, intent_coll
from flask import request, jsonify
from bson.json_util import dumps
from bson import ObjectId
from urllib.parse import unquote
from train import train_model
from auth import require_auth


@app.route("/train", methods=["POST"])
@require_auth
def train_route():
    train_model()
    response = {'message': 'Training completed'}
    return jsonify(response)


@app.route("/intents", methods=["GET"])
@require_auth
def get_intents():
    data = list(intent_coll.find())
    documents = dumps(data)
    return documents


@app.route("/add-intent", methods=["POST"])
@require_auth
def add_intent():
    tag = request.get_json().get("tag")

    if not tag:
        return jsonify({'error': 'Must input a tag'}), 400

    if intent_coll.count_documents({ 'tag': tag }, limit = 1) != 0:
        return jsonify({'error': 'Tag Already exists'}), 400

    else:
        document = {
        "tag":tag,
        "patterns":[],
        "responses":[]
        }

    intent_coll.insert_one(document)
    document = dumps(document)

    return (document)

@app.route("/delete-intent/<id>", methods = ["DELETE"])
@require_auth
def delete_intent(id):
    document = intent_coll.find_one_and_delete({'_id':ObjectId(id)})
    return dumps(document)
    

@app.route("/add-pattern/<id>", methods = ["PUT"])
@require_auth
def update_pattern(id):
    pattern = request.get_json().get("prompt") 

    exists = intent_coll.find_one({
        'patterns': {'$elemMatch': {'$eq': pattern}}
    })
    
    if exists:
        return jsonify({'error': 'Pattern already exists'}), 400
    
    if pattern and len(pattern) > 10:
        document = intent_coll.find_one_and_update({'_id':ObjectId(id)},{'$push':{'patterns':pattern}}, return_document=True)
    else:
        return jsonify({'error': 'You must submit either a pattern greater than 10 characters'}), 400
    return dumps(document)


@app.route("/add-response/<id>", methods = ["PUT"])
@require_auth
def update_response(id):
    response = request.get_json().get("prompt")

    exists = intent_coll.find_one({
        'responses': {'$elemMatch': {'$eq': response}}
    })

    if exists:
        return jsonify({'error': 'Response already exists'}), 400
    
    if response and len(response) > 10:
        document = intent_coll.find_one_and_update({'_id':ObjectId(id)},{'$push':{'responses': response}}, return_document=True)
    else:
        return jsonify({'error': 'You must submit a response greater than 10 characters'}), 400
    return dumps(document)


@app.route("/delete-pattern/<id>/<prompt>", methods = ["PUT"])
@require_auth
def delete_pattern(id, prompt):
    decoded_prompt = unquote(prompt)
    document = intent_coll.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$pull': {'patterns': decoded_prompt}},
        return_document=True
    )
    return dumps(document)


@app.route("/delete-response/<id>/<prompt>", methods = ["PUT"])
@require_auth
def delete_response(id, prompt):
    decoded_prompt = unquote(prompt)
    document = intent_coll.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$pull': {'responses': decoded_prompt}},
        return_document=True
    )
    return dumps(document)