# -*- coding: utf-8 -*-

# import modules
import re
import requests
from bs4 import BeautifulSoup

# list of webs related to 'palestine' at eur-lex.europa.eu, subdomain LEGISLATION year 2014
# Base url
base_url='http://eur-lex.europa.eu/search.html?text=palestine&scope=EURLEX&DD_YEAR=2014&qid=1429221052950&type=quick&lang=en&DTS_SUBDOM=LEGISLATION'
# Get the number of results/pages
response = requests.get(base_url)
soup = BeautifulSoup(response.content)
p_results=soup.find('p', {'class':'resultNumber'})
p_results = p_results[0].get_text()
pat_pres=re.compile("&nbsp;[0-9]+")
results= re.findall(pat_pres,p_results)[-1]
results=results[6:]
# Number of pages assuming 10 results per page
docs_page=10
npages=results/docs_page +1
# subsequent pages add '&page=2', '&page=3', etc
pages=range(1,npages+1,1)
pages[1:]=['&page'+str(page) for page in pages if page!='1']
pages[0]=''

# define text and metadata variables
title = []
rank=range(1,results+1,1)
date=[]
form=[]
author=[]
text = []


for page in pages:
    # get next search result page
    response = requests.get(base_url+page)
    soup = BeautifulSoup(response.content)
     
    
    # get titles
    Atitle=soup.find('a', {'class':'title'})
    title = [p.get_text() for p in Atitle] # falta poner append
    
    # Get rank and text of each doc
    # to get html: a xmlns="" xmlns:innerXml="innerXml" href="./legal-content/EN/TXT/HTML/?uri=OJ:JOL_2011_328_R_0002_01&amp;rid=1      
    allA = soup.find_all('a')
    all_href = [link.get("href") for link in allA if link.get("href") != None]
    pat_href=re.compile("/legal-content/EN/TXT/HTML/.") # avoid getting the initial dot
    url_href=re.findall(pat_href,all_href)
    docs=range(0,len(url_href),1) #number of docs in this page
    # explore each of the 10 results of the search
    for doc in docs:
        # get the text
        response_doc = requests.get('http://eur-lex.europa.eu' + url_href[doc])
        
        # case 1: all text in a 'box', exists a <div id='TexteOnly'>
        soup_doc= BeautifulSoup(response_doc.content)                
        div_box= soup_doc.find('div', { 'id' : 'TexteOnly' })
        if div_box != None :
            paragraphs = [p.get_text() for p in div_box.find_all('p')]
        # case 2: Main text follwoing first <hr> tag   
        else :
            pattern_hr=re.compile("<hr.?",re.UNICODE) #defined by tag <hr
            hr_doc = re.split(pattern_hr, response_doc.content)
            hr_doc= hr_doc[1]
            soup_doc = BeautifulSoup(hr_doc)
            p_doc = soup_doc.find("p", { 'class' : ['normal', 'ti-art'] }) #CHECK OR CLAUSE
            paragraphs = [p.get_text() for p in p_doc]
        text = text + paragraphs    
        
        
        # unify all the text (TO BE CHECKED)
        # text[page*doc]='\n'.join(doc_text)


# Save as data frame
import pandas as pd
data = pd.DataFrame({'title':title,'rank':rank,'date':date,'form':form,
                     'author':author,'text':text})
