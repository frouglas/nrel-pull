# -*- coding: utf-8 -*-
"""
Created on Tue Nov 07 17:41:46 2017

@author: doug
"""

import pandas as pd

def getSites(turbine_data):
    
    if turbine_data[0] == 0:
        print "bad data. please try again"
        return 0
    else:
        tDB = turbine_data[1]
        stateDB = turbine_data[2]
    
    print('How would you like to select turbines?')
    print('     1. By state')
    print('     2. By state and county')
    print('     3. By lat/long with radius')
    
    goodSelection = 0
    
    while goodSelection == 0:
        userSelection = input(int("please select an option: "))
        goodSelection = 1
        if userSelection == 1:
            siteInfo = getStateSites(turbine_data)
        elif userSelection == 2:
            siteInfo = getCountySites(turbine_data)
        elif userSelection == 3:
            siteInfo = getGeoSites(turbine_data)
        else:
            print("           invalid selection. please try again.")
            goodSelection = 0
    
    return siteInfo

def getStateSites(turbine_data):
    return 1

def getCountySites(turbine_data):
    return 1

def getGeoSites(turbine_data):
    return 1