from app import app, intent_coll
from flask import request, jsonify
from bson.json_util import dumps
from bson import ObjectId
from urllib.parse import unquote


@app.route("/intents", methods=["GET"])
def get_intents():
    data = list(intent_coll.find())
    documents = dumps(data)
    return documents


@app.route("/add-intent", methods=["POST"])
def add_intent():
    tag = request.get_json().get("tag")

    if intent_coll.count_documents({ 'tag': tag }, limit = 1) != 0:
        return jsonify({'error': 'Tag Already exists'}), 400

    else:
        document = {
        "tag":tag,
        "patterns":[],
        "responses":[]
        }

    intent_coll.insert_one(document)
    import train
    document = dumps(document)

    return (document)

@app.route("/delete-intent/<id>", methods = ["DELETE"])
def delete_intent(id):
    document = intent_coll.find_one_and_delete({'_id':ObjectId(id)})
    import train
    return dumps(document)
    

@app.route("/add-pattern/<id>", methods = ["PUT"])
def update_pattern(id):
    pattern = request.get_json().get("pattern")

    if pattern and len(pattern) > 10:
        document = intent_coll.find_one_and_update({'_id':ObjectId(id)},{'$push':{'patterns':pattern}}, return_document=True)
    else:
        return jsonify({'error': 'You must submit either a pattern greater than 10 characters'}), 400
    import train
    return dumps(document)


@app.route("/add-response/<id>", methods = ["PUT"])
def update_response(id):
    response = request.get_json().get("response")
    if response and len(response) > 10:
        document = intent_coll.find_one_and_update({'_id':ObjectId(id)},{'$push':{'responses': response}}, return_document=True)
    else:
        return jsonify({'error': 'You must submit a response greater than 10 characters'}), 400
    import train
    return dumps(document)


@app.route("/delete-pattern/<id>/<prompt>", methods = ["PUT"])
def delete_pattern(id, prompt):
    decoded_prompt = unquote(prompt)
    document = intent_coll.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$pull': {'patterns': decoded_prompt}},
        return_document=True
    )
    import train
    return dumps(document)


@app.route("/delete-response/<id>/<prompt>", methods = ["PUT"])
def delete_response(id, prompt):
    decoded_prompt = unquote(prompt)
    document = intent_coll.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$pull': {'response': decoded_prompt}},
        return_document=True
    )
    import train
    return dumps(document)