from wsgiref.validate import validator
from pymongo import MongoClient
import os, requests, json, copy
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
    "querystring": {"class_type":"ECO","sort_order":"PRICE","number_of_passengers":"1", "itinerary_type": "ONE_WAY"}, 
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
        type(userData['searchData']['name']) == str
        type(userData['searchData']['classType']) == str
        type(userData['searchData']['alertPrice']) == str
        type(userData['searchData']['date_departure']) == str
        type(userData['searchData']['location_departure']) == str
        type(userData['searchData']['location_arrival']) == str
        type(userData['searchData']['number_of_stops']) == str
        type(userData['searchData']['searchResult']) == dict
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

def searchFlight(searchData):
    try:
        type(searchData['date_departure']) == str
        type(searchData['location_departure']) == str
        type(searchData['location_arrival']) == str
        type(searchData['number_of_stops']) == str
        type(searchData['classType']) == str
    except Exception as e:
        return {"success": False, "error": f"type error: {e}"}
    try:
        priceline_api['querystring']['date_departure'] = searchData['date_departure']
        priceline_api['querystring']['location_arrival'] = searchData['location_arrival']
        priceline_api['querystring']['location_departure'] = searchData['location_departure']
        priceline_api['querystring']['number_of_stops'] = searchData['number_of_stops']
        priceline_api['querystring']['class_type'] = searchData['classType']

        response = requests.request("GET", priceline_api['url'], headers=priceline_api['headers'], params=priceline_api['querystring'])
        respJson = json.loads(response.text)
        if "pricedItinerary" in respJson:
            if respJson['pricedItinerary'] != None:
                return {"success": True, "data": {"searchResult": json.loads(response.text)}}
            else:
                return {"success": False, "message": "No Result"}
        else:
            return {"success": False, "message": "No Result"}
        
    except Exception as e:
        return {"success": False, "error": e}

def checkP():
    try:
        usersCursor = db['users'].find({})
        userArr = list(usersCursor)
    except Exception as e:
        return {"success": False, "error": e}
    userMessageArr = []
    for user in userArr:
        searchData = user['searchData']
        newSearchData = []
        for search in searchData:
            dateNow = datetime.utcnow().strftime("%Y-%m-%d")
            if(dateNow<search['dep']['date_departure'] and search["alertP"] != None):
                resDep = searchFlight(search['dep'])
                if(resDep['success']):
                    flightDep = Flight(resDep['data']['searchResult']).output()
                else:
                    flightDep = search['searchResult']['dep']
                if(search['type'] == "ROUND_TRIP"):
                    resRet = searchFlight(search['ret'])
                    if(resRet['success']):
                        flightRet = Flight(resRet['data']['searchResult']).output()
                    else:
                        flightRet = search['searchResult']['ret']
                else:
                    flightRet = None
                newSearch = copy.deepcopy(search)
                newSearch["date_updated"] = datetime.utcnow()
                newSearch["searchResult"] = {"dep": flightDep, "ret": flightRet}
                newSearchData.append(newSearch)
            else:
                newSearchData.append(search)
        userMessage = {user["userID"]: {"data update": None, "email": None}}
        try:
            db['users'].find_one_and_update({"userID": user["userID"]},
            {"$set": {"searchData": newSearchData}}, return_document=ReturnDocument.AFTER)
            try:
                emailPriceAlert(newSearchData)
                userMessage[user["userID"]]['email'] = "success"
            except Exception as e:
                userMessage[user["userID"]]['email'] = e
            userMessage[user["userID"]]['data update'] = "success"
        except Exception as e:
            userMessage[user["userID"]]['data update'] = e
            print({"success": False, "error": e})

        userMessageArr.append(userMessage)

    return userMessageArr

def delSearch(userData):
    try:
        type(userData['userID']) == str
        type(userData['dateCreated']) == str   
    except Exception as e:
        return {"success": False, "error": f"type error: {e}"}
    try:
        user = db['users'].find_one({"userID": userData["userID"]})
        date = datetime.utcnow()
        print(userData['dateCreated'], user['searchData'][0]['date_created'])
        newSearchData = updateSearchData(user['searchData'], userData['dateCreated'])
        updatedUser = db['users'].find_one_and_update({"userID": userData["userID"]},
        {"$set": {"searchData":  newSearchData}}, return_document=ReturnDocument.AFTER)
        return {"success": True, "data": {"user": updatedUser}}
    except Exception as e:
        return {"success": False, "error": e}


def emailPriceAlert(fetchedSearchedData):
    return "to be worked on later"

def updateSearchData(arr, date):
    newArr = []
    for search in arr:
        if(search['date_created'].timestamp() != datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').timestamp()):
            newArr.append(search)
    return newArr