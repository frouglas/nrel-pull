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
import sortMethod as sm
import csv
import os


debugOn = 1
turbineMethod = 1

if debugOn == 1:
    startTime = datetime.utcnow()
    resName = "nrel_results_tester.csv"
else:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    resName = "nrel_results_" + timestamp + ".csv"
 
wtkData = nrel.readData(0)

if wtkData[0]==0:
    print("there was an error loading the NREL metadata")
else:
    wtkDF = wtkData[1]
    stateDB = wtkData[2]

if turbineMethod == 0:
    turbines = sm.getSites(wtkData)
else:
    thisTurbine = wtkDF.loc[8260]

success = nrel.csvDownload(thisTurbine, 2010, 1)

breakPt = 1
