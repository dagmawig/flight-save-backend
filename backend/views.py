from django.http import JsonResponse
from django.shortcuts import render
from pymongo import MongoClient
from dotenv import load_dotenv
import requests, json, os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .dataModel import insertUser, findUser, saveSearchData, searchFlight, checkP
from .flight import Flight
import asyncio

load_dotenv()

connection_string = os.getenv('CONNECTION_STRING')

client = MongoClient(connection_string)
dbname = client['DATABASES']

collection_name = dbname['collection1']

priceline_api = {
    "url": "https://priceline-com-provider.p.rapidapi.com/v1/flights/search",
    "querystring": {"date_departure":"2022-06-17","class_type":"ECO","itinerary_type":"ONE_WAY","location_arrival":"NYC","location_departure":"STL","sort_order":"PRICE","duration_max":"2051","price_min":"100","number_of_passengers":"1","price_max":"20000","number_of_stops":"1"}, 
    "headers": {
	"X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com",
	"X-RapidAPI-Key": "53ccb0e66bmsh883175eecd2c429p13df65jsna6c7198d36a1"
}
}

# priceline_api2 = {
#     "url": "https://priceline-com-provider.p.rapidapi.com/v1/flights/search",
#     "querystring": {"date_departure":"2022-06-17","class_type":"ECO","itinerary_type":"ROUND_TRIP","location_arrival":"NYC","location_departure":"LAS","sort_order":"PRICE","date_departure_return":"2022-06-21","duration_max":"2051","number_of_passengers":"1","price_max":"330","number_of_stops":"1"}, 
#     "headers": {
# 	"X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com",
# 	"X-RapidAPI-Key": "53ccb0e66bmsh883175eecd2c429p13df65jsna6c7198d36a1"
# }
# }

f = open('data.json')
data = json.load(f)
# print(data)


@api_view(['GET'])
def search(request):
    if(request.method == "GET"):
        print("gets here", request.body)
        body = request.body.decode('utf-8')
        bodyData = json.loads(body)
        if(bodyData['searchFilter']['type'] == "ONE_WAY"):
            response = searchFlight(bodyData['searchFilter']['dep'])
            if(response['success']):
                flightData = Flight(response['data']['searchResult'])
                res = {"success": True, "data": {"dep":  flightData.output(), "ret": None}}
                return Response(json.loads(json.dumps(res, default=str)))
        else:
            resDep = searchFlight(bodyData['searchFilter']['dep'])
            resRet = searchFlight(bodyData['searchFilter']['ret'])
            flightDataDep = Flight(resDep['data']['searchResult'])
            flightDataRet = Flight(resRet['data']['searchResult'])
            res = {"success": True, "data": {"dep":  flightDataDep.output(), "ret": flightDataRet.output()}}
            return Response(json.loads(json.dumps(res, default=str)))

@api_view(['POST'])
def loadData(request):
    if(request.method == 'POST'):
        body = request.body.decode('utf-8')
        bodyData = json.loads(body)
        # print(bodyData["userID"])
        response = findUser(bodyData)
        if(response["success"]):
            return Response(json.loads(json.dumps(response, default=str)))
        else:
            inserted = asyncio.run(insertUser(bodyData))
            if(inserted["success"]):
                return Response(json.loads(json.dumps(findUser(bodyData), default=str)))
            else:
                return Response(json.loads(json.dumps(inserted, default=str)))
        
@api_view(['POST'])
def saveSearch(request):
    if(request.method == 'POST'):
        body = request.body.decode('utf-8')
        bodyData = json.loads(body)
        response = saveSearchData(bodyData)
        return Response(json.loads(json.dumps(response, default=str)))

@api_view(['POST'])
def checkPrice(request):
    if(request.method == 'POST'):
        body = request.body.decode('utf-8')
        bodyData = json.loads(body)
        checkP()
        return Response({"place holder": "place holder"})