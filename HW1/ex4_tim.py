# -*- coding: utf-8 -*-

## COMMENTS

## -- when we extract the date we can keep it as a string or date
##    both ways are done in the code (we need to uncomment one to decide what to keep)
## -- the last part with the loop of the different years, I don't know how to
##      append the results of the different years.
# import modules

import requests
from bs4 import BeautifulSoup
import datetime
import time 
import re


## Function that returns the number of pages of that search and how many results
def numberpages(base_url):
    # Get the number of results/pages
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content)
    p_results=soup.find('p', {'class':'resultNumber'})
    p_results = p_results.get_text()
    pat_pres=re.compile("\xa0[0-9]+")
    results= re.findall(pat_pres,p_results)[-1]
    results=int(results)
    # Number of pages assuming 10 results per page
    docs_page=10
    npages=results/docs_page +1
    # subsequent pages add '&page=2', '&page=3', etc
    pages=range(1,npages+1,1)
    return(results,pages)

#Funcions that extracts the metadata from the url
 def getdata(base_url): 
    date=[]
    form=[]
    author=[]
    text = []  
    title=[]    
    #get the number of results of the search and number of pages
    results,pages=numberpages(base_url)
    rank=range(1,results+1,1)    
    
    for page in pages:
        # get next search result page
        response = requests.get(base_url+'&page='+str(page))
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
            
            #get the author and date of the paper
            right=metadata.find('ul', {'class':'metadata'}).find_all('li')
            author.append(right[0].get_text()[8:])
            
            #date.append(datetime.strptime(right[1].get_text()[18:], "%d/%m/%Y" ).date())## in date format
            date.append(right[1].get_text()[18:])## in string format        
            form.append(left.find_all('li')[1].get_text()[6:])
            
            
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
    return(rank, author, date, form, text)
    
    
 #From the different years the only thing that changes is the end 
    #create a loop so it extracts the files of all the choosen years
    
years=range(2005,2015,1)  
base_url='http://eur-lex.europa.eu/search.html?text=palestine&scope=EURLEX&qid=1429221052950&type=quick&lang=en&DTS_SUBDOM=LEGISLATION&DD_YEAR=' 

for i in years:
    base_url=(base_url+str(years[i]))
    Trank,Tauthor,Tdate,Tform,Ttex=getdata(base_url)## how to append in a loop?

        
    
    #get titles
   # Atitle=table.find_all('td', {'class':'publicationTitle'})
    #for p in Atitle:
     #   title.append(p.get_text())
    #for link in table.find_all('a'):
     #     if link.get('href') == 

