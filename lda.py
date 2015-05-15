# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:47:20 2015

@author: timkreienkamp
"""
from __future__ import division
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time 

#change directory to where topicmodels is 
os.chdir('/users/timkreienkamp/documents/text-mining-tutorial/')

import topicmodels

#change it back to the folder for the homework
os.chdir('/users/timkreienkamp/documents/textminingbgse/HW4/')


#load data
data = pd.read_table("../HW2/data_puntuation.csv")

docsobj = topicmodels.RawDocs(data.Text, "../HW2/stopwords.txt")

docsobj.token_clean(1)

print docsobj.tokens[3]


docsobj.stopword_remove("tokens")

print docsobj.tokens[3]

docsobj.stem()

print docsobj.stems[3]

docsobj.tf_idf("stems")

plt.plot([x[1] for x in docsobj.tfidf_ranking_stems])
plt.savefig("tfidf_ranking.png")

docsobj.stopword_remove("stems", 8000)

all_stems = [s for d in docsobj.stems for s in d]

print("number of unique stems = %d" % len(set(all_stems)))
print("number of total stems = %d" % len(all_stems))


###### now the fun starts#########


ldaobj = topicmodels.LDA(docsobj.stems, 15)

print ldaobj.K

print ldaobj.alpha

print ldaobj.beta

print ldaobj.topic_seed[:10]

print ldaobj.topic_seed.shape

ldaobj.sample(0,50, 10)


plot1 = plt.plot(ldaobj.perplexity())
plt.ylabel("Perplexity")
plt.xlabel("Samples")
plt.title("First Markov Chain")
plt.savefig("firstchain.png")

ldaobj.sample(0,50, 20)


plot2 = plt.plot(ldaobj.perplexity())
plt.ylabel("Perplexity")
plt.xlabel("Samples")
plt.title("Second Markov Chain")
plt.savefig("secondchain.png")


time_start = time.clock()
ldaobj.sample(0,50, 10)
time_ = time.clock()-time_start


plot3 = plt.plot(ldaobj.perplexity())
plt.ylabel("Perplexity")
plt.xlabel("Iterations")
plt.title("Third Markov Chain")
plt.savefig("thirdchain.png")


ldaobj.samples_keep(10)


print ldaobj.tt.shape
print ldaobj.dt.shape

ldaobj.topic_content(10)

dt = ldaobj.dt_avg()

tt = ldaobj.tt_avg()

ldaobj.dict_print()


###############################
#Querying on titles
###############################


#first clean the data
titleobj = topicmodels.RawDocs(data.Title)
titleobj.token_clean(1)
titleobj.stem()

queryobj = topicmodels.Query(titleobj.tokens,ldaobj.token_key,ldaobj.tt)


queryobj.query(10) 

queryobj.perplexity()
queryobj.query(30) 
queryobj.perplexity()

dt_query = queryobj.dt_avg()

topics_documents = np.zeros(171, dtype = int)

topics_titles = np.zeros(171, dtype = int)

for i in range(0, 171):
    topics_documents[i] = np.argmax(dt[i,])
    topics_titles[i] = np.argmax(dt_query[i,])
    

equality_array = np.in1d(topics_documents,topics_titles)

matching_quota = np.mean(equality_array)


plt.hist(topics_documents, bins = 15)
plt.savefig("doctopicshist.png")

plt.hist(topics_titles, bins = 15)
plt.savefig("titletopicshist.png")


