# -*- coding: utf-8 -*-
import mic_streaming as ms
import requests as req
import json
import threading

jsonDataPath = {}

LEFT = 1
RIGHT = 2

def readShortestData(apikey, textFormat, apiName, startPage, endPage, startStation, endStation):
    SEARCH_BASE ="http://swopenapi.seoul.go.kr/api/subway/"

    url = SEARCH_BASE + apikey + '/' + textFormat + '/' + apiName + '/' + startPage
    url = url + '/' + endPage + '/' + startStation + '/' + endStation
    r = req.get(url)
    jsonData = json.loads(r.text)
    print("\njsonData:"+r.text)
    return jsonData
'''
apikey: api key 값
textFormat : json, xml 과 같은 데이터 포맷
apiName: openAPI 이름

'''
def readPrefNextStationData(apikey, textFormat, apiName, startPage, endPage, stationName, startLineNumber):
    SEARCH_BASE = 'http://swopenapi.seoul.go.kr/api/subway/'
    url = SEARCH_BASE + apikey + '/' + textFormat + '/' + apiName + '/' + startPage + '/' + endPage + '/' + stationName
    r = req.get(url)
    jsonData = json.loads(r.text)

    previd = ''
    nextid = ''
#    previd = jsonData["realtimeArrivalList"][0]["statnFid"]
#    nextid = jsonData["realtimeArrivalList"][0]["statnTid"]

    lines = jsonData["realtimeArrivalList"][0]["subwayList"].split(',')   
    lines_size = len(lines)

    i = 0
    while i < lines_size*4 :
        subway_line_ids = jsonData["realtimeArrivalList"][int(i/4)]["subwayList"].split(',')[int(i/4)][:4]
        if subway_line_ids == startLineNumber:
            previd = jsonData["realtimeArrivalList"][i]["statnFid"][6:]
            nextid = jsonData["realtimeArrivalList"][i]["statnTid"][6:]
#            if int(startLineNumber) >= 500:
#                previd = '2'+str(int(previd))
#                nextid = '2'+str(int(nextid))
            break
        i+=4

    prevStationName = ''
    nextStationName = ''
    try:
        SEARCH_BASE = 'http://openapi.seoul.go.kr:8088/'
        apiName = 'SearchSTNInfoByIDService'
        url = SEARCH_BASE + apikey + '/' + textFormat + '/' + apiName + '/' + startPage + '/' + endPage + '/' + previd
        r = req.get(url)
        prevStationName = json.loads(r.text)["SearchSTNInfoByIDService"]["row"][0]["STATION_NM"]

        url = SEARCH_BASE + apikey + '/' + textFormat + '/' + apiName + '/' + startPage + '/' + endPage + '/' + nextid
        r = req.get(url)
        nextStationName = json.loads(r.text)["SearchSTNInfoByIDService"]["row"][0]["STATION_NM"]
    except KeyError:
        print("Key Error is occured.")
        prevStationName = 'empty'
        nextStationName = 'empty'
    return prevStationName + '/' + nextStationName

#class MicThread(threading.Thread):
#    destinationT = ''
#    def get_destination():
#        return destinationT
#    def run(self):
#        destinationT = ms.start_method()

#def main():
#    startStation = input('Enter the start station - ')      # Set this value to specific station each device.
#    endStation = input('Enter the end station - ')     # Microphone destination input
def speak_destination(startStation, line, direction):
    print('목적지를 말하세요.')#TODO: sound로 대체
    endStation = ms.start_method()
#     speak = MicThread()
#    speak.start()
    
    print('-----------------############################-----------------------------------------------------------'+endStation)  
    # Load API Key 
    f = open('./.apikey', 'r')
    apikey = str(f.read())[:-1]
    f.close()

    global jsonDataPath
    jsonDataPath = readShortestData(apikey, 'json', 'shortestRoute', '0', '1', startStation, endStation)
    
    stationNameList = jsonDataPath['shortestRouteList'][0]['shtStatnNm'].split(',')
    travelMsg = jsonDataPath['shortestRouteList'][0]['minTravelMsg']

    # startLineNumber example => 1002, 1004, 1007 ... 100line number
    startLineNumber = jsonDataPath['shortestRouteList'][0]['shtStatnId'].split(',')[0][:4]
    print ("\nCurrent Station : " + stationNameList[0])
    print ("Next Station : " + stationNameList[1])
    print ("Travel Msg : " + travelMsg)

    print("start - " + str(startLineNumber))
    # Read previous station name & next station name
    data = readPrefNextStationData(apikey, 'json', 'realtimeStationArrival', '0', '12', startStation, startLineNumber).split('/')
    prevStationName = data[0]
    nextStationName = data[1]
    
    print ("Left Station : " + prevStationName)
    print ("Right Station : " + nextStationName)
#TODO 1: previd, nexitd 입력!
#TODO 2: prevStationName, nextStationName이 항상 종각, 종로5가로 나옴
    if nextStationName == stationNameList[1]:
        return RIGHT
    else:
        return LEFT

#speak_destination('성균관대', 1, 2)
#if __name__ == "__main__":
#    main()
