### Text Mining for Social Sciences
### Problem Set 2, exercise 1
### Maria Fernandez, Tim Kreienkamp, Joan Verdu
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 13:32:58 2015

@author: basket
"""
### libraries
import codecs, re
import numpy as np
from nltk.tokenize import wordpunct_tokenize
from nltk import PorterStemmer
import pandas as pd

### Class definition

class RawDocs():

    def __init__(self, doc_data, stopword_file):

        self.docs = [s.lower() for s in doc_data]

        with codecs.open(stopword_file,'r','utf-8') as f: raw = f.read()
        self.stopwords = set(raw.splitlines())

        self.docs = map(lambda x: re.sub(u'[\u2019\']', '', x), self.docs)

        self.N = len(self.docs)
        self.tokens = map(wordpunct_tokenize,self.docs)

        #   NEW unique terms
        self.unique=list(set([t for d in self.tokens for t in d]))
        self.unique.sort()

    def token_clean(self,length):

		""" 
		strip out non-alpha tokens and length one tokens
		"""

		def clean(tokens): return [t for t in tokens if t.isalpha() == 1 and len(t) > length]

		self.tokens = map(clean,self.tokens)


    def stopword_remove(self):

		"""
		Remove stopwords from tokens.
		"""

		def remove(tokens): return [t for t in tokens if t not in self.stopwords]
		self.tokens = map(remove,self.tokens)


    def stem(self):

		"""
		Stem tokens with Porter Stemmer.
		"""

		def s(tokens): return [PorterStemmer().stem(t) for t in tokens]
		self.stems = map(s,self.tokens)

    
    #   NEW document term matrix    
    def doc_term(self):

        def count_terms(doc): #  count of doc tokens
            # first initialize dictionary
            my_dict=dict.fromkeys(self.unique,0)   
            for i in doc:  my_dict[i]+=1
            return [my_dict[key] for key in sorted(my_dict.iterkeys())]

        #self.doc_term=count_terms(self.tokens[0],self.unique)
        # Apply to tokens of each doc
        self.doc_term=np.array(map(count_terms,self.tokens))
        
    # NEW: INCIDENCE MATRIX: to be done
    def incidence(self):
        self.incidence=np.where(self.doc_term > 0,1,0)
    
    # NEW count method, doc_term should be previously run
    def count(self,dictionary):
        """
        For tokens of every document, count words present at dictionary.
        """          
        # Filter doc term by terms        
        index=[i for i in range(0,len(self.unique)) if self.unique[i] in dictionary]# locate dictionary words
        self.count= self.doc_term[:,index]
    
    # NEW tf_idf method: to be done, doc_term should be previously run
    def tf_idf(self,dictionary):
        """
        For tokens of every document, compute td_idf according to a dictionary.
        """
        # Filter doc term by terms        
        index=[i for i in range(0,len(self.unique)) if self.unique[i] in dictionary]# locate dictionary words
        # Log counts of filtered doc_term matrix (term-frequency)
        tf= np.log(self.doc_term[:,index] +1)
        # Number of documents that contain each word   
        dfv=self.incidence[:,index].sum(axis=0) # filter and then sum for all words (cols)
        # Final formula: (term-frequency) * (inverse-document-frequency)
        self.tf_idf=tf * np.log((self.N/(dfv+0.0001))+0.00001)      
        
        
'''-----------------------------------------------------------------------------
        Exercise 2
-----------------------------------------------------------------------------'''
        
# Import data
data = pd.read_table("../HW1/output_hw1ex4_fdez_verdu_kreienkamp.CSV",encoding="utf-8")

#convert text to lowercase
for i in range(0, len(data.Text)):
    data.Text[i] = data.Text[i].lower()


#Remove numerics
for i in range(0, len(data.Text)):
    no_digits = []
# Iterate through the string, adding non-numbers to the no_digits list
    for j in data.Text[i]:
        if not j.isdigit():
            no_digits.append(j)
    
    # Now join all elements of the list with '', 
    # which puts all of the characters together.
    data.Text[i]  = ''.join(no_digits)

#with one dictionary 
docsobj = RawDocs(data.Text[0:100],'stopwords.txt')
docsobj.token_clean(2)
docsobj.stopword_remove()
# If running first time
docsobj.doc_term()
docsobj.incidence()
# If already runned
docsobj.doc_term=np.load('doc_term.npy')
docsobj.incidence=np.load('incidence.npy')

Count=['Eco_Count','Legal_Count','Military_Count','Religion_Count']
TD=['Eco_TD','Legal_TD','Military_TD','Religion_TD']
dictio=['Dic_Eco.csv','Dic_Legal.csv','Dic_Military.csv','Dic_Religion.csv']

dictionaries = pd.DataFrame({'Count':Count, 'TD': TD, 'Dic':dictio})

for j in range(0,(len(dictionaries))):
    #Implement the Count and TD-IDF method for the dictionary
    docsobj = RawDocs(data.Text,'stopwords.txt')
    docsobj.token_clean(2)
    docsobj.stopword_remove()
    docsobj.doc_term=np.load('doc_term.npy')
    docsobj.incidence=np.load('incidence.npy')
    dict1=pd.read_table(dictionaries.Dic[j],encoding='utf-8', header = None)
    #convert to numpy array
    dict1 = dict1.iloc[:,0].values
    
    # convert to lowercase
    for i in range(0, len(dict1)):
        dict1[i] = dict1[i].lower()
    
    #convert to list
    dict1 = dict1.tolist()
    docsobj.count(dict1)
    data[str(dictionaries.Count[j])]=docsobj.count.sum(axis=1)
    docsobj.tf_idf(dict1)
    data[str(dictionaries.TD[j])]=docsobj.tf_idf.sum(axis=1)
    print j

data.to_csv('data_puntuation.csv', sep = '\t',encoding='utf-8')