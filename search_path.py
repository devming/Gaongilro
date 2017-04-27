# -*- coding: utf-8 -*-

import requests as req
import json

jsonData = {}

def readData(_startStation, _endStation) :

    SEARCH_BASE ="http://swopenapi.seoul.go.kr/api/subway/"

    f = open('./apikey','r')
    apikey = str(f.read())[:-1]
    f.close()
    textformat = "json"
    apiname = "shortestRoute"
    startpage = '0'
    endpage = '1'
    startstation = _startStation    # Set this value to specific station each device.
    endstation = _endStation        # Microphone destination input

    url = SEARCH_BASE + apikey + '/' + textformat + '/' + apiname + '/' + startpage
    url = url + '/' + endpage + '/' + startstation + '/' + endstation
    r = req.get(url)
    js = json.loads(r.text)
    return js

def main() :
    
    startStation = raw_input('Enter the start station - ')      # Set this value to specific station each device.
    endStation = raw_input('Enter the end station - ')     # Microphone destination input
    
    global jsonData
    jsonData = readData(startStation, endStation)

    
#    stationIdList = jsonData['shortestRouteList'][0]['shtStatnId'] 
    stationNameList = jsonData['shortestRouteList'][0]['shtStatnNm'].split(',')
    travelMsg = jsonData['shortestRouteList'][0]['minTravelMsg']

#    print ("Station Id List : " + stationIdList)
#    print ("Path : " + stationNameList)
    print ("Current Station : " + stationNameList[0])
    print ("Next Station : " + stationNameList[1])
    print ("Travel Msg : " + travelMsg)



if __name__ == "__main__":
    main()


