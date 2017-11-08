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

import csv
import os


debugOn = 1
sampleT = 8249

if debugOn == 1:
    startTime = datetime.utcnow()
    resName = "nrel_results_tester.csv"
    outputFile = str(sampleT)
else:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    resName = "nrel_results_" + timestamp + ".csv"
    
wtkData = nrel.readData(0)
wtkDF = wtkData[1]
stateDB = wtkData[2]

thisTurbine = wtkDF.loc[sampleT]

success = nrel.csvDownload(thisTurbine, 2010, 1)

breakPt = 1

#
#thisGrab = ds.defaultParams()
#
#
#if defaultID == 0:
#    pointID = 1
#    outputFile = str(pointID)
#else:
#    pointID = defaultID
#siteCap = wtkDF.loc[defaultID, "capacity"]
#lat = wtkDF.loc[defaultID,"latitude"]
#longitude = wtkDF.loc[defaultID,"longitude"]
#pointLoc = Point(longitude,lat).wkt
#
#parDict = {}
#
#parDict["api_key"] = thisGrab.apiKey
#parDict["wkt"] = pointLoc
#parDict["atrributes"] = thisGrab.attributes
#parDict["names"] = thisGrab.names
#parDict["email"] = thisGrab.email
#
##siteString = str("https://developer.nrel.gov//wind-toolkit/wind/wtk_download.csv?" 
##                 + parameterString)
#
#if debugOn == 1 and os.path.exists(resName):
#    next
#else:
#    r = requests.get(url = "https://developer.nrel.gov/api/wind-toolkit/wind/wtk_download.csv",
#                 params = parDict)
#    responseText = r.text
#    f = open(resName,'w')
#    f.write(responseText)
#    f.close
#
#thisSite = pd.read_csv(resName,header = 3,usecols = ['Year','Month','Day','Hour','Minute', 'power (MW)'])
#thisSite.loc[:,"power (MW)"] = thisSite.loc[:"power (MW)"] / siteCap
#thisSite.rename(columns={'power (MW)':'availability'}, inplace=True)
#
#years = thisSite["Year"].astype(int).values
#months = thisSite["Month"].astype(int).values
#days = thisSite["Day"].astype(int).values
#hours = thisSite["Hour"].astype(int).values
#minutes = thisSite["Minute"].astype(int).values
#
#indexArrays = [years, months, days, hours, minutes]
#indexTuples = list(zip(*indexArrays))
#
#thisIndex = pd.MultiIndex.from_tuples(indexTuples, names=['Year','Month','Day','Hour','Minute'])
#thisSite = thisSite.drop('Year',1)
#thisSite = thisSite.drop('Month',1)
#thisSite = thisSite.drop('Day',1)
#thisSite = thisSite.drop('Hour',1)
#thisSite = thisSite.drop('Minute',1)
#
#thisSite = thisSite.set_index(thisIndex)
#thisSite = thisSite.groupby(level=['Year','Month','Day','Hour']).mean()
#mIndex = thisSite.index
#
#theseYears = np.sort(thisSite.index.levels[0].values)
#
#for eachYear in theseYears:
#    activeShape = thisSite.loc[(eachYear,slice(None),slice(None),slice(None))]
#    activeShape['Year'] = eachYear
#    activeShape['hr_num'] = [i + 1 for i in range(len(activeShape))]
#    activeShape.set_index('Year',append=True, inplace=True)
#    activeShape.set_index('hr_num',append=True, inplace=True)
#    activeShape = activeShape.reorder_levels(['hr_num','Year','Month','Day','Hour'])
#    outputFile = outputFile + "_" + str(int(eachYear)) + ".csv"
#    activeShape.to_csv(outputFile)
#
#if debugOn == 1:
#    endTime = datetime.utcnow()
#    elapsed = endTime - startTime
#    print(elapsed.total_seconds())
#    
#
#    
#    
#    
#    
#    
#
#
#
#
#
