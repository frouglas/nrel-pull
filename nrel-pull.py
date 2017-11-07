#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 23:25:36 2017

@author: frouglas
"""



nrel_api = "gfXQDIuItFQxpf5xs6LEE9KmZ6btbom1DIHfg785"

import data_structure as ds
import numpy as np
import pandas as pd
import math
import os
import pickle
import importlib as il
import matplotlib.pyplot as plt
from datetime import datetime


def readData():
    if os.path.exists("wtk_site_metadata.csv"):
        rawData = pd.read_csv("wtk_site_metadata.csv")
    else:
        print("no information file found")

    


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
