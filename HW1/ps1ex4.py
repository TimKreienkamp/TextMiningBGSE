# -*- coding: utf-8 -*-

# import modules
import requests
from bs4 import BeautifulSoup

# list of webs related to 'palestine' at eur-lex.europa.eu
base_url='http://eur-lex.europa.eu/search.html?qid=1429221052950&text=palestine&scope=EURLEX&type=quick&lang=en'
# subsequent pages add '&page=2', '&page=3', etc
pages=range(1,101,1)
# docs per page
docs=range(0,10,1)

# define text and metadata variables
title = []
rank=[]
date=[]
form=[]
author=[]
text = []

for page in pages:
    # get next search result page
    response = requests.get(base_url+'&page'+str(page))
    soup = BeautifulSoup(response.content)
    
    table = soup.find('table', { 'class' : 'documentTable' })
    #get titles
    Atitle=soup.find_all('a', {'class':'title'})
    title = [p.get_text() for p in Atitle] # falta poner append
    


    
# to get html: a xmlns="" xmlns:innerXml="innerXml" href="./legal-content/EN/TXT/HTML/?uri=OJ:JOL_2011_328_R_0002_01&amp;rid=1    
# from here to be done !    
allA = [link.get("href") for link in allA if link.get("href") != None]
# explore each of the 10 results of the search
for doc in docs:
    rank[page*doc]=(page*doc)+1 #ranking of relevance
        
        
    
# get all <a> tags
allA = soup.find_all('a')
# get web
all_links = [link.get("href") for link in allA if link.get("href") != None]
press_links = [link for link in all_links if link.startswith('/Media/PressReleases/Show')]
# get the text
response2 = requests.get('https://www.flsenate.gov' + press_links[0])
soup = BeautifulSoup(response2.content)

# Save as data frame
import pandas as pd
#data = pd.DataFrame({'title':title,'text':text})
