from django.http import JsonResponse
from django.shortcuts import render
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view


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

@api_view(['GET'])
def get(request):
    if(request.method == "GET"):
        print("gets here", request.body)
        response = requests.request("GET", priceline_api['url'], headers=priceline_api['headers'], params=priceline_api['querystring'])
        # response = requests.get("https://anapioficeandfire.com/api/houses/1")
        print(response.text)
        return Response(response.text)