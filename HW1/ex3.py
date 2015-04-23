# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:06:14 2015

@author: timkreienkamp
"""
import re
import numpy as np
import codecs
import pandas as pd
with codecs.open('sou_all.txt','r','utf-8') as file_obj:
	data=file_obj.read()
 

 
#### Second version: Better alternative
# split into headers and paragraphs directly
pattern_paragraph=re.compile("\*\*+.?",re.UNICODE) #defined by more than 1 *
sessions = re.split(pattern_paragraph, data)
# note sessions[0] is void, don't use it
# Go for paragraphs
sliceObj=slice(2,len(sessions),2) #paragraphs are in odd positions
paragraphs=sessions[sliceObj]
paragraphs=[par.strip("\n") for par in paragraphs] # remove initial/final line breaks
# Go for headers
sliceObj=slice(1,len(sessions),2) #paragraphs are in odd positions
headers=sessions[sliceObj]
headers=[text.strip("_") for text in headers]
# Extract years from headers
years=[text[0:4] for text in headers]
# Extract last name from headers
pat_pres=re.compile("[A-Z][a-z]+")
pres_name=[re.findall(pat_pres,text)[-1] for text in headers] # last word of each header

#convert years to integers to do arithmetic, comparisons, whatever with them
years = np.asarray(years, dtype = int)
years.tolist()


# put the data in paragraphs
i=0
pattern_speech=re.compile("\n\n+?",re.UNICODE)

yearsPar=[]
presidentPar=[]
SpeechPar=[]


for speeches in paragraphs:
    paragraphsSpeech=re.split(pattern_speech, speeches)
    del paragraphsSpeech[0]
    del paragraphsSpeech[len(paragraphsSpeech)-1]
    for numpara in paragraphsSpeech:
        yearsPar.append(years[i])
        presidentPar.append(pres_name[i])
        SpeechPar.append(numpara)
    i=i+1

#Put it all in the data frame
sou_all_frame = pd.DataFrame({'Year':yearsPar, 'President':presidentPar, 'Paragraph':SpeechPar})
    

 
#recall we had to order them chronologically
sou_all_frame = sou_all_frame.sort("Year", ascending = False)