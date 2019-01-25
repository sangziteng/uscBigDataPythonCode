#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 20:11:24 2019

@author: xiaojuezhang
"""
import os
import pandas as pd

from bs4 import BeautifulSoup #for webscraping
import time
import numpy as np
from urllib.request import urlopen



########################################################################

### url = "http://www.rugbydata.com/italy/ireland/gamesplayed/"


Countries = ['england', 'ireland', 'france']
for C in Countries:
    url = "http://www.rugbydata.com/italy/" + C + "/gamesplayed/"
    ### print(url)

    response = urlopen(url)
    
    html = response.read()
    
    ########################################################################
    
    soup = BeautifulSoup(html, "html.parser")
    
    AwayTeam = soup.find_all('td', attrs = {'class':'away-team'})
    # AwayTeam[0].text
    AwayTeamClean = []
    for x in AwayTeam:
        print(x.text)
        AwayTeamClean.append(x.text)
    AwayTeamClean
    # len(AwayTeamClean)
        
    
    ## j = 0
    ## for i in range(0,10,1):
    ##    j = i + 1
    ##    print(i)
    
    HomeTeam = soup.find_all('td', attrs = {'class':'home-team'})
    HomeTeamClean = []
    for x in HomeTeam:
        print(x.text)
        HomeTeamClean.append(x.text)
    HomeTeamClean
    
    
    Scores = soup.find_all('a', attrs = {'class':'match-score'})
    ScoresClean = []
    for x in Scores:
        print(x.text)
        ScoresClean.append(x.text)
    ScoresClean
    
    
    ## <td class="match-date  sorting_1">11 Feb 2017</td>
    Dates = soup.find_all('td', attrs = {'class':'match-date'})
    DatesClean = []
    for x in Dates:
        print(x.text)
        DatesClean.append(x.text)
    DatesClean
    
    
    ########### put all the data into the Panda DataFrame
    ## pd.DataFrame( [AwayTeamClean, HomeTeamClean, ScoresClean, DatesClean])
    finaldata = pd.DataFrame( list(zip(AwayTeamClean, HomeTeamClean, ScoresClean, DatesClean)), columns = ['Away Team','Home Team','Score','Date'])
    finaldata.to_csv("./DownladedRugbyData-"+C+".csv")
    
    
    ####################################################################################
    
        
        