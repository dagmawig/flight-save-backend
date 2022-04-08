from wsgiref.validate import validator
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
connection_string = os.getenv('CONNECTION_STRING')

client = MongoClient(connection_string)
db = client['DATABASES']


async def insertUser(userData):
    try:
        type(userData['email']) == str
        type(userData["userID"])  == str
    except Exception as e:
        return {"success": False, "error": f"type error: {e}"}
    try:
        userData["date_created"] = datetime.utcnow()
        resp = db['users'].insert_one(userData)
        return {"success": True, "message": "User Added!", "resp": resp}
    except Exception as e:
        return {"success": False, "error": e}

def findUser(userData):
    try:
        type(userData['email']) == str
        type(userData["userID"])  == str
    except Exception as e:
        return {"success": False, "error": f"type error: {e}"}
    try:
        user = db['users'].find_one({"userID": userData["userID"]})
        if(user==None):
            return {"success": False, "message": "no such user!"}
        else:
            return {"success": True, "data": {"user":user}}
    except Exception as e:
        return {"success": False, "error": e}
