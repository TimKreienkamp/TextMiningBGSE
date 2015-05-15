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

iterations = np.arange(50, 550, 50)

plot1 = plt.plot(iterations, ldaobj.perplexity())
plt.ylabel("Perplexity")
plt.xlabel("Iterations")
plt.title("First Markov Chain")

time_start = time.clock()
ldaobj.sample(0,50, 20)
time_ = time.clock()-time_start

avg_time = time_/1000


plot2 = plt.plot(ldaobj.perplexity())
plt.ylabel("Perplexity")
plt.xlabel("Iterations")
plt.title("Second Markov Chain")


time_start = time.clock()
ldaobj.sample(0,50, 10)
time_ = time.clock()-time_start


plot3 = plt.plot(ldaobj.perplexity())
plt.ylabel("Perplexity")
plt.xlabel("Iterations")
plt.title("Third Markov Chain")


ldaobj.samples_keep(20)


print ldaobj.tt.shape
print ldaobj.dt.shape


ldaobj.topic_content(10)

dt = ldaobj.dt_avg()

tt = ldaobj.tt_avg()

ldaobj.dict_print()