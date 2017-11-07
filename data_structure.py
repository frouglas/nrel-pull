#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 00:06:47 2017

@author: frouglas
"""

class county():
    def __init__(self, params):
        self.name = params.get('name')
        self.state = params.get('state')
        self.maxLat = params.get('maxLat')
        self.minLat = params.get('minLat')
        self.maxLong = params.get('maxLong')
        self.minLong = params.get('minLong')
        self.countyCenter = params.get('centroid')
        self.turbines = params.get('turbines')
        
        
class state():
    def __init__(self, params):
        self.name = params.get('name')
        self.maxLat = params.get('maxLat')
        self.minLat = params.get('minLat')
        self.maxLong = params.get('maxLong')
        self.minLong = params.get('minLong')
        self.countyList = params.get('countyList')
        self.counties = params.get('counties')
        self.turbines = params.get('turbines')
        self.stateCenter = params.get('centroid')
        
class defaultParams():
    def __init__(self):
        self.apiKey = "gfXQDIuItFQxpf5xs6LEE9KmZ6btbom1DIHfg785"
        self.names = [2010]
        self.attributes = ['power']
        self.utc = 0
        self.leap_day = 0
        self.email = 'doug@ethree.com'
        self.intervals = 12 * 24 * 365
    
    def size(self, turbines = 1):
        sizeCalc = len(self.names) * len(self.attributes) * self.intervals * turbines
        return sizeCalc

def size_check(site_count = 1, attribute_count = 1, year_count = 1, int_per_year = 1):
    site_count = 0
    attribute_count = 0
    year_count = 0
    int_per_year = 0
    
    request_size = size_count*attribute_count*year_count*int_per_year
    
    return request_size