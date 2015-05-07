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
docsobj = F.RawDocs(data.Text,'stopwords.txt')
docsobj.token_clean(2)
docsobj.stopword_remove()
# If running first time
docsobj.doc_term()
docsobj.incidence()

dictionary=docsobj.unique

#removing the symbols from the dictionary
words=[]
for word in dictionary:
    if word.isalnum() == True:
        words.append(word)

docsobj.tf_idf(words) ##count all the terms in our unique

X=docsobj.tf_idf
X=X.T

'''-----------------------------------------------------------------------------
Single Value Decomposition of X (numpy)
-----------------------------------------------------------------------------'''

import numpy as np

U, S, V = np.linalg.svd(X, full_matrices=False)

singlevalues=[]
for ss in S:
    singlevalues.append(np.power(ss,2))

NormSV =[] 
for ss in singlevalues:
    NormSV.append(ss/sum(singlevalues))
    
cumSV=[]
cumSV.append(NormSV[0])
for i in range(2,99):
    cumSV.append(sum(NormSV[0:i]))

#See how many we should keep:
import matplotlib.pyplot as plt
plt.plot(cumSV)
plt.ylabel('Sumulative Sum of Squares of Singular Value Vector')
plt.show()

#Element 17th is the first one to contain 99% of the variance:
k=17
U_k = U[:, :k]
sigma = np.diag(S)[:k,:k]
V_k = V[:k, :]
X_k = np.dot(U_k, np.dot(sigma,V_k))

##Now we have the new X_k matrix
cs=np.zeros((len(X.T),len(X.T)))


for i in range(0,len(X)):
    for j in range(0,len(X)):
        d1=X[:,i]
        d2=X[:,j]
        cs[i,j]=np.dot(d1.T,d1)/(np.linalg.norm((d1), ord=2)*np.linalg.norm((d1), ord=2))
    
cs_k=np.zeros((len(X.T),len(X.T)))

for i in range(0,len(X)):
    for j in range(0,len(X)):
        d1=X_k[:,i]
        d2=X_k[:,j]
        cs_k[i,j]=np.dot(d1.T,d1)/(np.linalg.norm((d1), ord=2)*np.linalg.norm((d1), ord=2))
    
