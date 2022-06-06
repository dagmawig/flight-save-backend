from django.http import JsonResponse
from django.shortcuts import render
from pymongo import MongoClient
from dotenv import load_dotenv
import requests, json, os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .dataModel import delSearch, insertUser, findUser, saveSearchData, searchFlight, checkP, delSearch, upSearch
from .flight import Flight
import asyncio

load_dotenv()

connection_string = os.getenv('CONNECTION_STRING')

client = MongoClient(connection_string)
dbname = client['DATABASES']

collection_name = dbname['collection1']


# API endpioints
@api_view(['POST'])
def search(request):
    if(request.method == "POST"):
        body = request.body.decode('utf-8')
        bodyData = json.loads(body)
        response = searchFlight(bodyData['searchFilter'])
        if(response['success']):
            flightData = Flight(response['data']['searchResult'])
            res = {"success": True, "data":  flightData.output()}
            return Response(json.loads(json.dumps(res, default=str)))
        else:
            return Response(json.loads(json.dumps(response, default=str)))

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
        response = checkP()
        return Response(json.loads(json.dumps(response, default=str)))

@api_view(['POST'])
def deleteSearch(request):
    if(request.method == 'POST'):
        body = request.body.decode('utf-8')
        bodyData = json.loads(body)
        response = delSearch(bodyData)
        return Response(json.loads(json.dumps(response, default=str)))

@api_view(['POST'])
def updateSearch(request):
    if(request.method == 'POST'):
        body = request.body.decode('utf-8')
        bodyData = json.loads(body)
        response = upSearch(bodyData)
        return Response(json.loads(json.dumps(response, default=str)))