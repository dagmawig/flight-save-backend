from wsgiref.validate import validator
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
from pymongo.collection import ReturnDocument
from .flight import Flight

load_dotenv()
connection_string = os.getenv('CONNECTION_STRING')
headers = {
    "X-RapidAPI-Host": os.getenv('X-RAPIDAPI-HOST'),
    "X-RapidAPI-Key": os.getenv('X-RAPIDAPI-KEY')
}
url = os.getenv('URL')

priceline_api = {
    "url": url,
    "querystring": {"class_type":"ECO","sort_order":"PRICE","number_of_passengers":"1"}, 
    "headers": {
	"X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com",
	"X-RapidAPI-Key": "53ccb0e66bmsh883175eecd2c429p13df65jsna6c7198d36a1"
} }

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
        userData['searchData'] = []
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

def saveSearchData(userData):
    try:
        type(userData["userID"])  == str
        type(userData['searchData']['type']) == str
        type(userData['searchData']['name']) == str
        type(userData['searchData']['searchResult']) == dict
        type(userData['searchData']['dep']['date_departure']) == str
        type(userData['searchData']['dep']['location_arrival']) == str
        type(userData['searchData']['dep']['location_departure']) == str
        type(userData['searchData']['dep']['number_of_stops']) == str
        if(userData['searchData']['type'] == "round_trip"):
            type(userData['searchData']['arr']['date_departure']) == str
            type(userData['searchData']['arr']['location_arrival']) == str
            type(userData['searchData']['arr']['location_departure']) == str
            type(userData['searchData']['arr']['number_of_stops']) == str
    except Exception as e:
        return {"success": False, "error": f"type error: {e}"}
    try:
        userData['searchData']["date_created"] = datetime.utcnow()
        userData['searchData']["date_updated"] = datetime.utcnow()
        user = db['users'].find_one_and_update({"userID": userData["userID"]},
        {"$push": {"searchData":  userData['searchData']}}, return_document=ReturnDocument.AFTER)
        return {"success": True, "data": {"user": user}}
    except Exception as e:
        return {"success": False, "error": e}
