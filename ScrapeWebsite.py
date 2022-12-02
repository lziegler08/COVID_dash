# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:55:53 2022

@author: Elliott
"""
# Used this:
#https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import date
import os
import time

class ScrapeWebsite:
    def __init__(self, countries, URL, siteName, savePath, attr, attr_val, nameIDX, popIDX, deathIDX, casesIDX):
        self.URL = URL
        self.countries = countries
        self.siteName = siteName
        self.savePath = savePath
        self.attr = attr
        self.attr_val = attr_val
        self.tableRows = self.reqURL()
        self.nameIDX = nameIDX
        self.popIDX = popIDX
        self.deathIDX = deathIDX
        self.casesIDX = casesIDX
    
    def reqURL(self):
        req = requests.get(self.URL)
        soup = BeautifulSoup(req.content, 'html.parser')
        table = soup.find('table', attrs={self.attr:self.attr_val})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        print(len(rows))
        return rows
    
    def getDate(self):
        return str(date.today())
    
    def scrape_country(self):
        countryProfiles = {'name': [],
                           'population': [],
                           'total cases': [],
                           'total deaths':[],
                           'date collected': []}
        today = self.getDate()
        self.jsonPath = self.savePath + self.siteName + '_' +  today + ".json"
        with open(self.jsonPath, "w") as womJ:
            for r in self.tableRows:
                cols = r.find_all('td')
                
                dList = [i.text.strip() for i in cols]
                for c in self.countries:
                    if c.lower() == dList[self.nameIDX].lower():
                        countryProfiles['name'].append(dList[self.nameIDX])
                        countryProfiles['population'].append(int(dList[self.popIDX].replace(',', '')))
                        countryProfiles['total cases'].append(int(dList[self.casesIDX].replace(',', '')))
                        countryProfiles['total deaths'].append(int(dList[self.deathIDX].replace(',', '')))
                        countryProfiles['date collected'].append(today)
                        break
            json.dump(countryProfiles, womJ)
        return self.buildDF()
        
    def buildDF(self):
        self.df = pd.read_json(self.jsonPath)
        return self.df


countries = ['brazil', 'usa', 'france', 'austria', 'Monaco', 'greece']

wom_url = 'https://www.worldometers.info/coronavirus/#countries'
wom_siteName = 'world-o-meter'
wom_savePath = 'C:/Users/Elliott/Documents/PE_final/'
wom_attr = 'id'
wom_attr_val = 'main_table_countries_today'
wom = ScrapeWebsite(countries, wom_url, wom_siteName, wom_savePath,\
                  wom_attr, wom_attr_val, 1, 14, 2, 4)
wom_data = wom.scrape_country()
print(wom_data)