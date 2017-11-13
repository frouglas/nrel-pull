# -*- coding: utf-8 -*-
"""
Created on Tue Nov 07 13:20:14 2017

@author: doug
"""

import urllib.request
import json

googleAPI = "AIzaSyA3cIh3Qqzhm3PUvxTis7CPpFnED9x9jcE"
endURL = "}&key=" + googleAPI
baseURL = "https://maps.googleapis.com/maps/api/geocode/json?address={"

def getCoords(addString):
    thisReq = baseURL + addString + endURL
    thisReq = URLConvert(thisReq)
    geoRequest = urllib.request.urlopen(thisReq)
    geoRequest = json.load(geoRequest)
    geoRequest = geoRequest['results']
    gName = geoRequest[0]['formatted_address']
    geoRequest = geoRequest[0]['geometry']
    geoRequest = [geoRequest['location']['lat'],geoRequest['location']['lng']]
    geoRequest = [gName, geoRequest]
    return geoRequest

def URLConvert(reqStr):
    retStr = reqStr.replace(" ","%20")
    retStr = retStr.replace(",","%2C")
    return retStr

thisPlace = getCoords("Madison, WI")
    