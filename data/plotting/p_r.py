import os.path as osp, os
import matplotlib.pyplot as plt  
import numpy as np

from searchEngine.invertedIndexer import invertedIndex
from searchEngine.tokenizer import tokenize
from searchEngine.search_interface import load_data

"""
Function to plot P/R curves based on average of each query. File needs to be moved to root project folder (IRTwitterSearch) to be functional
"""

#relevant = 34
#relevant = 15
#total = 88
#total = 33
total = 15
#relevant = 15
correct = 0
queries = 3
data = [3,2,2,2,2,3,2,2,3,1,2,2,1,2,0] #This is the total # of relevant tweets for all the test queries. 
relevant = (np.sum(data) / queries) #Compute average for p/r curve

#Data below represents binary classification of relevant/irrelevant docs return in search engine (manual classification and implementation)
#data = [1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,0,1,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1]
#data = [1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1]

precision = [1] #Ensure the line begins at the top
recall = [0]
position = 1
for i in range(len(data)):

    if data[i] >= 1:
        correct += data[i] / queries
    try:
        precis = correct/position
    except ZeroDivisionError:
        precis = 1

    position += 1
    precision.append(precis)
    recall.append(correct/relevant)
decreasing_max_precision = np.maximum.accumulate(precision[::-1])[::-1]

plt.title("Precision Recall")
plt.ylabel("Precision")
plt.xlabel("Recall")
plt.xlim(0, 1.005)
plt.ylim(-.1, 1.1)
plt.plot(recall, precision)
plt.step(recall, decreasing_max_precision, '-r')
plt.legend(["Precision", "Interpolated precision"])
plt.show()