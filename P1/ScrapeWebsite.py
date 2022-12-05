#%% -*- coding: utf-8 -*-
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
        if self.siteName == 'ny_times':
            table_body = table.find('tbody', attrs={self.attr:'children'})
        else:
            table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        return rows
    
    def getDate(self):
        return str(date.today())



    def scrape_wom(self):
        countryProfiles = {'name': [],
                           'population': [],
                           'total cases': [],
                           'total deaths':[],
                           'date collected': []}
        today = self.getDate()
        for r in self.tableRows:
            cols = r.find_all('td')
            
            dList = [i.text.strip() for i in cols]
            for c in self.countries:
                if c.lower() == dList[self.nameIDX].lower():
                    countryProfiles['name'].append(dList[self.nameIDX])
                    countryProfiles['population'].append(float(dList[self.popIDX].replace(',', '')))
                    countryProfiles['total cases'].append(float(dList[self.casesIDX].replace(',', '')))
                    countryProfiles['total deaths'].append(float(dList[self.deathIDX].replace(',', '')))
                    countryProfiles['date collected'].append(today)
                    break
        return countryProfiles 

    def scrape_nyt(self):
        countryProfiles = {'name': [],
                           'daily deaths avg': [],
                           'per 100k': [],
                           'date collected': []}
        today = self.getDate()
        for r in self.tableRows:
            cols = r.find_all('td')
            dList = [i.text.strip() for i in cols]
            try:
                dList[0] = dList[0].split('\xa0')[0]
            except:
                pass
            
            countryProfiles['name'].append(dList[0])
            countryProfiles['daily deaths avg'].append(float(dList[4].replace(',', '')))
            try:
                countryProfiles['per 100k'].append(float(dList[5].replace(',', '')))
            except ValueError:
                countryProfiles['per 100k'].append(0.0)
            countryProfiles['date collected'].append(today)
            
        return countryProfiles


    def scrape_JH(self):
        countryProfiles = {'name': [],
                           'population': [],
                           'total cases': [],
                           'total deaths':[],
                           'date collected': []}


    def scrape_country(self):
        today = self.getDate()
        self.jsonPath = self.savePath + self.siteName + '_' +  today + ".json"
        with open(self.jsonPath, "w") as womJ:
            if self.siteName == 'ny_times':
                cProf = self.scrape_nyt()
            if self.siteName == 'world-o-meter':
                cProf = self.scrape_wom()
            json.dump(cProf, womJ)
        return self.buildDF()
        
    def buildDF(self):
        self.df = pd.read_json(self.jsonPath)
        return self.df


countries = ['brazil', 'usa', 'france', 'austria', 'Monaco', 'greece', 'brunei', 'hong kong', 'paraguay', 'south korea', 'New Zealand', 'japan', 'Palau', 'Andorra']

wom_url = 'https://www.worldometers.info/coronavirus/#countries'
wom_siteName = 'world-o-meter'
wom_savePath = '/Users/lauraziegler/Documents/GitHub/COVID_dash/' #'/Users/lauraziegler/Documents/Python/COVID_dash/P1/'#
wom_attr = 'id'
wom_attr_val = 'main_table_countries_today'
wom = ScrapeWebsite(countries, wom_url, wom_siteName, wom_savePath,\
                  wom_attr, wom_attr_val, 1, 14, 2, 4)
wom_data = wom.scrape_country()
print(wom_data)


nyt_url = 'https://www.nytimes.com/interactive/2021/world/covid-cases.html'
nyt_siteName = 'ny_times'
nyt_savePath = '/Users/lauraziegler/Documents/GitHub/COVID_dash/' # '/Users/lauraziegler/Documents/Python/COVID_dash/P1/' #
nyt_attr = 'class'
nyt_attr_val = 'g-table super-table withchildren'
nyt =  ScrapeWebsite(countries, nyt_url, nyt_siteName, nyt_savePath,\
                  nyt_attr, nyt_attr_val, 0, 4, 4, 1)
nyt_data = nyt.scrape_country()

print(nyt_data)

"""
jh_url = 'https://coronavirus.jhu.edu/data/mortality'
jh_siteName = 'jh'
jh_savePath = '/Users/lauraziegler/Documents/GitHub/COVID_dash/'
jh_attr = 'class'
jh_attr_val = 'g-table super-table withchildren'
jh =  ScrapeWebsite(countries, jh_url, jh_siteName, jh_savePath,\
                  jh_attr, jh_attr_val, 0, 4, 4, 1)
jh_data = jh.scrape_country()

print(jh_data)
"""
#%%