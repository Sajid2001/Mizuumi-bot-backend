from app import users, app
from flask import request, jsonify
from bson.json_util import dumps
from bcrypt import gensalt, hashpw, checkpw
import re

@app.route('/register', methods = ["POST"])
def register():
    
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    role = request.get_json().get("role")

    if not role:
        role = "USER"

    #validation + bcrpyt

    if not email or not password:
        return jsonify({'error': 'Fields should not be empty'}), 400
    
    valid_email = re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email)
    if not valid_email:
        return jsonify({'error': 'Invalid email format'}), 400
    
    is_valid_password = re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password)

    if not is_valid_password:
        return jsonify({'error': 'Password is not strong enough'}), 400
    
    exists = users.find_one({"email":email})

    if exists:
        return jsonify({'error': 'User already exists'}), 400
    
    encoded_password = password.encode('utf-8')
    salt = gensalt(10)
    hashed_password = hashpw(encoded_password,salt)

    #validation + bcrypt

    user = {
        "email":email,
        "password":hashed_password,
        "role":role
    }

    users.insert_one(user)
    return dumps(user)


@app.route('/login', methods = ["POST"])
def login():

    email = request.get_json().get("email")
    password = request.get_json().get("password")
    role = request.get_json().get("role")

    if not email or not password:
        return jsonify({'error': 'Fields should not be empty'}), 400

    user = users.find_one({"email":email})

    if not user:
        return jsonify({'error': 'Incorrect Email'}), 400
    
    entered_password = password.encode('utf-8')

    match = checkpw(entered_password,user["password"])
    
    if not match:
        return jsonify({'error': 'Incorrect Password'}), 400
    
    return dumps(user)

