# -*- coding: utf-8 -*-

# import modules
import requests
from bs4 import BeautifulSoup
import time 

# list of webs related to 'palestine' at eur-lex.europa.eu
base_url='http://eur-lex.europa.eu/search.html?qid=1429221052950&text=palestine&scope=EURLEX&type=quick&lang=en'
# subsequent pages add '&page=2', '&page=3', etc
pages=range(1,5,1)
# docs per page
docs=range(0,10,1)

# define text and metadata variables
title = []
rank=[]
date=[]
form=[]
author=[]
text = []

time_start = time.clock()
for page in pages:
    # get next search result page
    response = requests.get(base_url+'&page'+str(page))
    soup = BeautifulSoup(response.content)
    
    #search results are organized in an html table
    table = soup.find('table', { 'class' : 'documentTable' })
    
    #now we iterate through the results rowwise
    rows = table.find_all('tr')
    
   #titles are at position 1, metadata is at position 3
    #WARNING: we are still not taking into account all edge cases here so as is this will not work every time!!!
    for i in range(0, len(rows), 3):
        title.append(rows[i].find('td', {'class':'publicationTitle'}).get_text())
        metadata = rows[i+2]
        
        
        
    
    #get titles
   # Atitle=table.find_all('td', {'class':'publicationTitle'})
    #for p in Atitle:
     #   title.append(p.get_text())
    #for link in table.find_all('a'):
     #     if link.get('href') == 
        
    

