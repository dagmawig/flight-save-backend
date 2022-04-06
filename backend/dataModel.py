from wsgiref.validate import validator
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
connection_string = os.getenv('CONNECTION_STRING')

client = MongoClient(connection_string)
db = client['DATABASES']


def insertUser(userData):
    try:
        type(userData['email']) == str
        type(userData["userID"])  == str
    except Exception as e:
        return {"success": False, "error": f"type error: {e}"}
    try:
        userData["date_creaetd"] = datetime.utcnow()
        db['users'].insert_one(userData)
        return {"success": True, "message": "User Added!"}
    except Exception as e:
        return {"success": False, "error": e}

