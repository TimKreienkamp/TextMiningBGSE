# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:24:20 2015

@author: timkreienkamp
"""

similarity_same_topic = 0
counter_same_topic = 0
similarity_across_topics = 0
counter_different_topics = 0
for i in range(0, 171):
    for j in range(0, 171):
        if maxTopicInd[i] == maxTopicInd[j] and i != j:
            similarity_same_topic += cs[i,j]
            counter_same_topic += 1
        elif maxTopicInd[i] != maxTopicInd[j] and i != j:
            similarity_across_topics += cs[i,j]
            counter_different_topics += 1

avg_similarity_same_topic = similarity_same_topic/counter_same_topic
avg_similarity_different_topic = similarity_across_topics/counter_different_topics

similarity_same_topic = 0
counter_same_topic = 0
similarity_across_topics = 0
counter_different_topics = 0

for i in range(0, 171):
    for j in range(0, 171):
        print cs_k[i,j]
        if maxTopicInd[i] == maxTopicInd[j] and i != j:
            similarity_same_topic += cs_k[i,j]
            counter_same_topic += 1
        elif maxTopicInd[i] != maxTopicInd[j] and i != j:
            similarity_across_topics += cs_k[i,j]
            counter_different_topics += 1

avg_similarity_same_topic_svd = similarity_same_topic/counter_same_topic
avg_similarity_different_topic_svd = similarity_across_topics/counter_different_topics
