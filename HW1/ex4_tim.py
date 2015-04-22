# -*- coding: utf-8 -*-

# import modules
import requests
from bs4 import BeautifulSoup
import time 
import re

# list of webs related to 'palestine' at eur-lex.europa.eu
base_url='http://eur-lex.europa.eu/search.html?text=palestine&scope=EURLEX&DD_YEAR=2014&qid=1429221052950&type=quick&lang=en&DTS_SUBDOM=LEGISLATION'
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
   
    for i in range(0, len(rows), 3):
        title.append(rows[i].find('td', {'class':'publicationTitle'}).get_text())
        #filter out the metadata
        metadata = rows[i+2]
        # get the left metadata
        left = metadata.find('td', {'class':'leftMetadata'})
        # get the direct text access class
        directtextaccess = left.find('li', {'class': 'directTextAccess'})
        #get all the links
        access_links = directtextaccess.find_all('a', href = True)
        for link in access_links:
            if '/EN/TXT/HTML/' in link['href']:
                #now "click" the link
                print link['href']
                text_page = requests.get("http://eur-lex.europa.eu/"+link['href'][1:])
                #soupify
                text_page_soup = BeautifulSoup(text_page.content)
                text_page_text = text_page_soup.get_text()
                text.append(text_page_text)
            else:
                text.append('NA')
        
            
        
        
    
    #get titles
   # Atitle=table.find_all('td', {'class':'publicationTitle'})
    #for p in Atitle:
     #   title.append(p.get_text())
    #for link in table.find_all('a'):
     #     if link.get('href') == 
        
    

