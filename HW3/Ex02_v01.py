# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:23:13 2015

@author: Maria F. & Tim K. & Joan V.
"""
import function as F #import function 
import pandas as pd      
        
'''-----------------------------------------------------------------------------
        Exercise 1
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
docsobj = F.RawDocs(data.Text[0:100],'stopwords.txt')
docsobj.token_clean(2)
#docsobj.stopword_remove()
# If running first time
docsobj.doc_term()
docsobj.incidence()

dictionary=docsobj.unique

'''-----------------------------------------------------------------------------
!!!!Should remove the symbols from the unique!
-----------------------------------------------------------------------------'''
 
docsobj.tf_idf(dictionary) ##count all the terms in our unique

X=docsobj.tf_idf

'''-----------------------------------------------------------------------------
Value Decomposition (numpy)
-----------------------------------------------------------------------------'''

##Keep only few hundred of words to approximate the X matrix


