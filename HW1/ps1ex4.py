# -*- coding: utf-8 -*-

# import modules
import re
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
    # from here to be checked !  
    allA = soup.find_all('a')
    
    all_href = [link.get("href") for link in allA if link.get("href") != None]
    pat_href=re.compile("/legal-content/EN/TXT/HTML/.") # avoid getting the initial dot
    url_href=re.findall(pat_href,all_href)
    
    # explore each of the 10 results of the search
    for doc in docs:
        rank[page*doc]=(page*doc)+1 #ranking of relevance
        # get the text
        response = requests.get('http://eur-lex.europa.eu' + url_href[doc])
        # get text follwoing first <hr> tag, where is the main text
        pattern_hr=re.compile("<hr.?",re.UNICODE) #defined by tag <hr
        paragraphs = re.split(pattern_hr, response)
        paragraphs=paragraphs[1]
        soup = BeautifulSoup(paragraphs)
        release = soup.find("p", { 'class' : ['normal', 'ti-art'] }) #CHECK OR CLAUSE
        doc_text = [p.get_text() for p in release]
        # unify all the text (TO BE CHECKED)
        text[page*doc]='\n'.join(doc_text)


# Save as data frame
import pandas as pd
data = pd.DataFrame({'title':title,'rank':rank,'date':date,'form':form,
                     'author':author,'text':text})
