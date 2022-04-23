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
        segmentIDArr, totDurationArr, overnightArr, cabinNameArr, flightTimeArr, airArr = [], [], [], [], [], []
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
                temp4 = []
                for segD in self.data["segment"]:
                    if(segD["uniqueSegId"]==segID):
                        temp2.append(segD["departDateTime"])
                        temp2.append(segD["arrivalDateTime"])
                        temp4.append(self.getAirportName(segD["origAirport"]))
                        temp4.append(self.getAirportName(segD["destAirport"]))
                temp3.append(temp4)
            flightTimeArr.append(temp2)  
            airArr.append(temp3) 
        return {"sliceIDArr": sliceIDArr, "segmentIDArr": segmentIDArr, "totDurationArr": totDurationArr, "overnightArr": overnightArr, "cabinNameArr": cabinNameArr, "flightTimeArr": flightTimeArr, "airArr": airArr}
    def output(self):
        return {"airline": self.getAirline(), "totPrice": self.getTotalPrice(), "flightInfo":  self.flightInfo(), "raw_data": self.data}