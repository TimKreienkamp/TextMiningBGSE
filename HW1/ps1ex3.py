# read data
import codecs
with codecs.open('sou_all.txt','r','utf-8') as file_obj:
	data=file_obj.read()

### First version
# paragraphs using regular expression
import re
pattern_paragraph=re.compile("\*\*\*\*\*\*+.\.?",re.UNICODE) #defined by more than 5 *
paragraphs = re.split(pattern_paragraph, data)
paragraphs= paragraphs[1:]
paragraphs=[par.strip("*_") for par in paragraphs] # here we get paragraphs with headers
# years using regular expression
pat_year=re.compile("\*\*\*\*\*\*+_[0-9][0-9][0-9][0-9]")
years=re.findall(pat_year,data)
years=[year[-4:] for year in years]
# Last name of President using regular expression
pat_pres=re.compile("[A-Z][a-z]+_\*\*\*\*\*")
pres_name=re.findall(pat_pres,data)
pres_name=[pres[:-6] for pres in pres_name]

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
years=[text[0:3] for text in headers]
# Extract last name from headers
pat_pres=re.compile("[A-Z][a-z]+")
pres_name=[re.findall(pat_pres,text)[-1] for text in headers] # last word of each header
