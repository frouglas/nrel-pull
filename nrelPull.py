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


def readData(refresh=0):
    
    if (os.path.exists("nrel.wind") and refresh != 1):
        dataPackage = pickle.load(open( 'nrel.wind', "rb" ))
    else:
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
        
        states = np.sort(rawData.State.unique())
        states = [states[i].upper() for i in range(len(states))]
        
    
        # compile databases of state and county level information (turbines)
        
        stateDB = {}
        countyDB = {}
        thisCountyDB = {}
        
        
        for state in states:
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
        pickle.dump(dataPackage, open( 'nrel.wind', "wb" ))
        print(    "database updated")
        breakPt = 1
        
    return dataPackage   

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
