# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:23:13 2015

@author: Maria F. & Tim K. & Joan V.
"""
from __future__ import division
import function as F #import function 
import pandas as pd   
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np  
        
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

np.savetxt("X_Matrix.csv", X, delimiter="\t")


'''-----------------------------------------------------------------------------
Single Value Decomposition of X (numpy)
-----------------------------------------------------------------------------'''



U, S, V = np.linalg.svd(X, full_matrices=False)

singlevalues=[]
for ss in S:
    singlevalues.append(np.power(ss,2))

NormSV =[] 
for ss in singlevalues:
    NormSV.append(ss/sum(singlevalues))
    
cumSV=[]
cumSV.append(NormSV[0])
for i in range(2,170):
    cumSV.append(sum(NormSV[0:i]))

#See how many we should keep:
import matplotlib.pyplot as plt
plt.plot(cumSV)
plt.ylabel('Cumulative Sum of Squares of Singular Value Vector')
plt.show()

#Element 17th is the first one to contain 99% of the variance:
k=10
U_k = U[:, :k]
sigma = np.diag(S[:k])
V_k = V[:k, :]
X_k = np.dot(U_k, np.dot(sigma,V_k))


'''-----------------------------------------------------------------------------
Cosine Similarity
-----------------------------------------------------------------------------'''
cs=cosine_similarity(X.T)
cs_k=cosine_similarity(X_k.T)

'''-----------------------------------------------------------------------------
Check with results of previous HW
-----------------------------------------------------------------------------'''

result = pd.read_table("../HW2/data_puntuation.csv")

topics=result[['Eco_TD','Legal_TD','Military_TD','Religion_TD']]
topics=topics.reset_index(drop=True)
rowmax = topics.max(axis=1)
maxTopic=np.where(topics.values == rowmax[:,None]) # which is maximum of the 4 categories
maxTopicInd=maxTopic[1]
IndTopic=maxTopic[0]

#None of the documents prefare Religion theme, so we'll study 
## the other topics.

#Sometimes there are ties, so we will keep only one of the 3 topics,
#well keep only one
TopicIndex=[]
j=0
for i in range(0,186):
    if IndTopic[i]==j:
        TopicIndex.append(maxTopicInd[i])
        j=j+1
        
        
    

def similarity(topic1, topic2, topicInd, cs_mat):
    similarity = 0.0
    counter = 0.0
    for i in range(0, len(topicInd)):
        for j in range(0, len(topicInd)):
            if topicInd[i] == topic1 and topicInd[j] == topic2 and i != j:
                similarity += cs_mat[i,j]
                counter +=1.0
    similarity = similarity/counter
    return similarity

noTopics = len(np.unique(TopicIndex))
similarity_matrix_k = np.zeros((noTopics, noTopics))


for i in range(0, noTopics):
    for j in range(0, noTopics):
        similarity_matrix_k[i,j] = similarity(i, j, TopicIndex, cs_k)
    


