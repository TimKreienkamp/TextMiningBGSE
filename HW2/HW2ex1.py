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
        self.unique = list(set([t for d in self.tokens for t in d]))


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
            for i in doc: my_dict[i]+=1             
            return my_dict.values()
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
        self.tf_idf=tf * np.log(self.N/dfv)       
        
        
# Sample try
        
import pandas as pd
data = pd.read_table("speech_data_extend.txt",encoding="utf-8")
docsobj = RawDocs(data.speech[0:100],'stopwords.txt')
docsobj.doc_term()
np.save('sample_doc_term.npy',docsobj.doc_term)
