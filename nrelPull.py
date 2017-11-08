#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 23:25:36 2017

@author: frouglas
"""



nrel_api = "gfXQDIuItFQxpf5xs6LEE9KmZ6btbom1DIHfg785"

import numpy as np
import pandas as pd
import math
import os
import pickle
import importlib as il
import matplotlib.pyplot as plt
from datetime import datetime
import data_structure as ds
import sys
import requests
from shapely.geometry import Point
import csv



def readData(refresh=0):
    if sys.version_info[0] < 2:
        print("     requires python 2 or above")
    elif sys.version_info[0] == 2:
        picklePath = "nrel_2.wind"
    else:
        picklePath = "nrel.wind"
    
    
    if (os.path.exists(picklePath) and refresh != 1):
        dataPackage = pickle.load(open(picklePath, "rb" ))
    else:
        if ((sys.version_info == 3) and (refresh!=1) and (os.path.exists("nrel_2.wind"))):
            picklePath = "nrel_2.wind"
            dataPackage = pickle.load(open(picklePath, "rb" ))
        rawData = pd.DataFrame()
        
        if os.path.exists("wtk_site_metadata.csv"):
            rawData = pd.read_csv("wtk_site_metadata.csv")
        else:
            print("no information file found")
    
        states = list(rawData["State"])
        states = [states[i].upper() for i in range(len(states))]
        rawData.loc[:,"State"] = states
        
        counties = list(rawData["County"])
        counties = [counties[i].upper() for i in range(len(counties))]
        rawData.loc[:,"County"] = counties
        
        rawData = rawData.set_index("site_id")
        
        stateList = np.sort(rawData.State.unique())
        stateList = [stateList[i].upper() for i in range(len(stateList))]
        
    
        # compile databases of state and county level information (turbines)
        
        stateDB = {}
        countyDB = {}
        thisCountyDB = {}
        
        
        for state in stateList:
            stateData = rawData[rawData["State"] == state]
            turbines = stateData.index.values
            maxLat = stateData.latitude.max()
            minLat = stateData.latitude.min()
            maxLong = stateData.longitude.max()
            minLong = stateData.longitude.min()
            centroid = [stateData.latitude.mean(), stateData.longitude.mean()]
            countyList = np.sort(stateData.County.unique())
            countyList = [countyList[i].upper() for i in range(len(countyList))]
            for county in countyList:
                countyData = stateData[stateData["County"] == county]
                c_turbines = countyData.index.values
                c_maxLat = countyData.latitude.max()
                c_minLat = countyData.latitude.min()
                c_maxLong = countyData.longitude.max()
                c_minLong = countyData.longitude.min()
                c_centroid = [countyData.latitude.mean(), countyData.longitude.mean()]
                thisCounty = ds.county({'name':county, 'state':state,'turbines':c_turbines, 
                                  'maxLat':c_maxLat,'minLat':c_minLat,'maxLong':c_maxLong,'minLong':c_minLong,
                                  'centroid':c_centroid})
                thisCountyDB[county] = thisCounty
            thisState = ds.state({'name':state,'countyList':countyList, 'turbines':turbines, 
                                  'maxLat':maxLat,'minLat':minLat,'maxLong':maxLong,'minLong':minLong,
                                  'centroid':centroid,'counties':thisCountyDB})
            stateDB[state] = thisState 
        dataPackage = [1,rawData,stateDB]
        pickle.dump(dataPackage, open(picklePath, "wb" ),protocol=sys.version_info[0])
        print(    "database updated")
        breakPt = 1
        
    return dataPackage   

# method for downloading a single year of data from a single turbine

def csvDownload(turbine, tYear = 0, query = 0):
    debugOn = 1
    outputFile = ""
    
    pointID = turbine.name
        
    if debugOn == 1:
        startTime = datetime.utcnow()
        resName = "nrel_results_tester.csv"
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        resName = "nrel_results_" + timestamp + ".csv"
    
    outputFile = str(pointID)
    thisGrab = ds.defaultParams()
    siteCap = turbine.loc["capacity"]
    lat = turbine.loc["latitude"]
    longitude = turbine.loc["longitude"]
    pointLoc = Point(longitude,lat).wkt
    
    parDict = {}
    
    parDict["api_key"] = thisGrab.apiKey
    parDict["wkt"] = pointLoc
    parDict["atrributes"] = thisGrab.attributes
    if tYear == 0:
        parDict["names"] = thisGrab.names
    else:
        parDict["names"] = [tYear]
    parDict["email"] = thisGrab.email
    
    #siteString = str("https://developer.nrel.gov//wind-toolkit/wind/wtk_download.csv?" 
    #                 + parameterString)
    
    if query == 0 and os.path.exists(resName):
        next
    else:
        r = requests.get(url = "https://developer.nrel.gov/api/wind-toolkit/wind/wtk_download.csv",
                     params = parDict)
        responseText = r.text
        with open(resName,'w') as f:
            f.write(responseText)
            f.close
    
    thisSite = pd.read_csv(resName,header = 3,usecols = ['Year','Month','Day','Hour','Minute', 'power (MW)'])
    thisSite.loc[:,"power (MW)"] = thisSite.loc[:"power (MW)"] / siteCap
    thisSite.rename(columns={'power (MW)':'availability'}, inplace=True)
    
    years = thisSite["Year"].astype(int).values
    months = thisSite["Month"].astype(int).values
    days = thisSite["Day"].astype(int).values
    hours = thisSite["Hour"].astype(int).values
    minutes = thisSite["Minute"].astype(int).values
    
    indexArrays = [years, months, days, hours, minutes]
    indexTuples = list(zip(*indexArrays))
    
    thisIndex = pd.MultiIndex.from_tuples(indexTuples, names=['Year','Month','Day','Hour','Minute'])
    thisSite = thisSite.drop('Year',1)
    thisSite = thisSite.drop('Month',1)
    thisSite = thisSite.drop('Day',1)
    thisSite = thisSite.drop('Hour',1)
    thisSite = thisSite.drop('Minute',1)
    
    thisSite = thisSite.set_index(thisIndex)
    thisSite = thisSite.groupby(level=['Year','Month','Day','Hour']).mean()
    
    theseYears = np.sort(thisSite.index.levels[0].values)
    
    for eachYear in theseYears:
        activeShape = thisSite.loc[(eachYear,slice(None),slice(None),slice(None))]
        activeShape['Year'] = eachYear
        activeShape['hr_num'] = [i + 1 for i in range(len(activeShape))]
        activeShape.set_index('Year',append=True, inplace=True)
        activeShape.set_index('hr_num',append=True, inplace=True)
        activeShape = activeShape.reorder_levels(['hr_num','Year','Month','Day','Hour'])
        outputFile = outputFile + "_" + str(int(eachYear)) + ".csv"
        activeShape.to_csv(outputFile)
    
    if debugOn == 1:
        endTime = datetime.utcnow()
        elapsed = endTime - startTime
        print(elapsed.total_seconds())
    
    return(1)
'''

[sample code from other import]
 
def loadData(statBasis):
    stats = statBasis
    
    playerDB = {}
    
    if os.path.exists("gameLogs.csv"):
        rawData = pd.read_csv("gameLogs.csv")
    else:
        print("no such file found")
        
    if os.path.exists("team_dict.csv"):
        teamDB = pd.read_csv("team_dict.csv")
    else:
        print("no such file found")
    
    teamDB.set_index("City Name", drop=True, inplace=True)
    
    team_dict = teamDB['NBA.com Abbreviation'].to_dict()
    
    gameDB = {}
    
    colNames = list(rawData.columns.values)
    
    i = 0
    
    for i in range(len(colNames)):
        colNames[i] = colNames[i].replace(" ","_")
       
    colNames[6] = 'VENUE'
        
    rawData.columns = colNames
    
    own_vals = [team_dict[x] for x in rawData["OWN_TEAM"]]
    opp_vals = [team_dict[x] for x in rawData["OPP_TEAM"]]
    home = [(x=='H') for x in rawData["VENUE"]]
    date = [datetime.strptime(x,"%m.%d.%y") for x in rawData["DATE"]]
    
    home_tm = []
    away_tm = []
    game_code = []
    
    for i in range(len(own_vals)):
        if home[i]:
            home_tm.append(own_vals[i])
            away_tm.append(opp_vals[i])
        else:
            home_tm.append(opp_vals[i])
            away_tm.append(own_vals[i])
        game_code.append(date[i].strftime("%m.%d.%y") + "#" + home_tm[i] + "#" + away_tm[i])
    
    rawData = rawData.assign(own_team = own_vals)
    rawData = rawData.assign(home_team = home_tm)
    rawData = rawData.assign(away_team = away_tm)
    rawData = rawData.assign(game_id = game_code)
    rawData = rawData.assign(fScore = 0)
    rawData.loc[:,"DATE"] = date
    
    fPoints = np.asarray(list(rawData['fScore']))
    for eachStat in stats.countingStats:
        thisVal = stats.values[eachStat]
        if thisVal == 0:
            continue
        thisStat = np.asarray(rawData[eachStat])
        fPoints = fPoints + thisStat * thisVal
    rawData.loc[:,'fScore'] = fPoints
        
    playerCounter = 1
    totalPlayers = len(rawData['PLAYER_FULL_NAME'].unique())
    
    for eachName in rawData['PLAYER_FULL_NAME'].unique():
        thisData = rawData[rawData.PLAYER_FULL_NAME==eachName]
        pGamesPlayed = thisData['game_id']
        pGamesEligible = thisData[thisData['MIN'] >= 12]['game_id']
        
#        for eachTeam in thisData["OWN_TEAM"].unique():
            
        playerDB[eachName] = ds.player({'name':eachName,'playerID':playerCounter,
                'gamesPlayed':pGamesPlayed, 'gamesEligible':pGamesEligible, 'gameStats':thisData})
        if playerCounter % 20 == 0:
            print("parsed " + str(playerCounter) + " of " + str(totalPlayers) + " players...")
        playerCounter += 1
        
    
    playerDB[rawData["PLAYER_FULL_NAME"][0]].name
    
    checkPt = -1
    i = 0
    entries = len(rawData)
    return 1
    #for eachEntry in rawData.itertuples():
    #    thisPlayer = playerDB[eachEntry.PLAYER_FULL_NAME]
    #    thisGame = eachEntry.game_id
    #    
    #    if thisPlayer.gameStats is None:
    #        thisPlayer.gameStats = {}
    #    thisPlayer.gameStats[thisGame] = [eachEntry[eachEntry._fields.index(cStat)] for cStat in stats.countingStats]
    #    
    #    if thisGame in gameDB:
    #        gameDB[thisGame].gamePlayers.append(thisPlayer)
    #        gameDB[thisGame].gameStats[thisPlayer] = thisPlayer.gameStats
    #    else:
    #        gameDB[thisGame] = ds.game({'game_id': thisGame})
    #        gameDB[thisGame].gamePlayers.append(thisPlayer)
    #        gameDB[thisGame].gameStats[thisPlayer] = thisPlayer.gameStats
    #    
    #    if i == checkPt:
    #        break
    #    else:
    #        i += 1
    #        if i % 100 == 0:
    #            print("     processed game " + str(i) + " of " + str(entries))

def loadScores(scoreDB = "pt_template.csv"):
    stats = ds.stats
    if os.path.exists(scoreDB):
        scoreRubrik = pd.read_csv(scoreDB)
    else:
        print("no such file found")
        return 0
    statList = list(scoreRubrik.columns.values)
    stats.countingStats = statList
    for eachStat in statList:
        statVal = scoreRubrik[eachStat][0]
        if not hasattr(stats,"values"):
            stats.values = {}
        stats.values[eachStat] = statVal
    return stats
    
'''
