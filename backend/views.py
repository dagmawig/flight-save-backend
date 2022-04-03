import json
from django.http import JsonResponse
from django.shortcuts import render
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import requests, json
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

f = open('data.json')
data = json.load(f)
# print(data)

class Flight:
    def __init__(self, data):
        self.data = data
    def getAirline(self):
        airlineArr = []
        for  iten in self.data["pricedItinerary"]:
            airlineArr.append(self.getAirlineName(iten["pricingInfo"]["ticketingAirline"]))
        return airlineArr
    def getAirlineName(self, code):
        for airline in self.data["airline"]:
            if(airline["code"]==code):
                return airline["name"]
    def getAirportName(self, code):
        for airport in self.data["airport"]:
            if(airport["code"]==code):
                return airport["name"]
    def getTotalPrice(self):
        totPriceArr = []
        for iten in self.data["pricedItinerary"]:
            totPriceArr.append(iten["pricingInfo"]["totalFare"])
        return totPriceArr
    def flightInfo(self):
        sliceIDArr = []
        for iten in self.data["pricedItinerary"]:
            sliceIDArr.append(iten["slice"][0]["uniqueSliceId"])
        segmentIDArr, totDurationArr, overnightArr, cabinNameArr, flightTimeArr, destAirArr = [], [], [], [], [], []
        for sliceID in sliceIDArr:
            for sliceD in self.data["slice"]:
                if(sliceD["uniqueSliceId"]==sliceID):
                    temp = []
                    for segment in sliceD["segment"]:
                        temp.append(segment["uniqueSegId"])
                    segmentIDArr.append(temp)
                    totDurationArr.append(sliceD["duration"])
                    overnightArr.append(sliceD["overnightLayover"])
                    cabinNameArr.append(sliceD["segment"][0]["cabinName"])
        for segArr in segmentIDArr:
            temp2, temp3 = [], []
            for segID in segArr:
                for segD in self.data["segment"]:
                    if(segD["uniqueSegId"]==segID):
                        temp2.append(segD["departDateTime"])
                        temp2.append(segD["arrivalDateTime"])
                        temp3.append(self.getAirportName(segD["destAirport"]))
            flightTimeArr.append(temp2)  
            destAirArr.append(temp3) 
        return {"sliceIDArr": sliceIDArr, "segmentIDArr": segmentIDArr, "totDurationArr": totDurationArr, "overnightArr": overnightArr, "cabinNameArr": cabinNameArr, "flightTimeArr": flightTimeArr, "destAirArr": destAirArr}
    def output(self):
        return {"airline": self.getAirline(), "totPrice": self.getTotalPrice(), "flightInfo":  self.flightInfo()}

flightData = Flight(data)

@api_view(['GET'])
def get(request):
    if(request.method == "GET"):
        print("gets here", request.body)
        # response = requests.request("GET", priceline_api['url'], headers=priceline_api['headers'], params=priceline_api['querystring'])
        # response = requests.get("https://anapioficeandfire.com/api/houses/1")
        # print(response.text)
        return Response(flightData.output())