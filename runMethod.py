#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 23:27:27 2017

@author: frouglas
"""



import nrelPull as nrel
import data_structure as ds
import numpy as np
import pandas as pd
import geopy as gp
from datetime import datetime
from shapely.geometry import Point
import requests

debugOn = 1
defaultID = 8249

if debugOn == 1:
    startTime = datetime.utcnow()

wtkData = nrel.readData(0)
wtkDF = wtkData[1]
stateDB = wtkData[2]

thisGrab = ds.defaultParams()


if defaultID == 0:
    pointLoc = 1
else:
    lat = wtkDF.loc[defaultID,"latitude"]
    long = wtkDF.loc[defaultID,"longitude"]
    pointLoc = Point(long,lat).wkt
#    pointLoc = pointLoc.replace(" ","",1)
#    pointLoc = pointLoc.replace(" ","%2C",1)

attributeStr = ""

for thisAttribute in thisGrab.attributes:
    if attributeStr != "":
        attributeStr = attributeStr + ","
    attributeStr = "" + thisAttribute

namesStr = ""

for thisName in thisGrab.names:
    if namesStr != "":
        namesStr = namesStr + ","
    namesStr = "" + str(thisName)

parDict = {}

parDict["api_key"] = thisGrab.apiKey
parDict["wkt"] = pointLoc
parDict["atrributes"] = thisGrab.attributes
parDict["names"] = thisGrab.names
parDict["email"] = thisGrab.email

#siteString = str("https://developer.nrel.gov//wind-toolkit/wind/wtk_download.csv?" 
#                 + parameterString)

r = requests.get(url = "https://developer.nrel.gov/api/wind-toolkit/wind/wtk_download.csv",
                 params = parDict)

breakPt = 1

if debugOn == 1:
    endTime = datetime.utcnow()
    elapsed = endTime - startTime
    print(elapsed.total_seconds())
    

    
    
    
    
    





