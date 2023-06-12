from flask import Flask

from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
CORS(app)

connection_string = os.getenv("MONGODB_URI")
client = MongoClient(connection_string)

db = client['ohayo-mizuumi-db']
messages = db.messages
intent_coll = db.intents
users = db.users

from app import login_routes
from app import intent_routes
from app import message_routes
