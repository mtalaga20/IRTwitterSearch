"""
#NOTE Needs OS for import files
"""

from pickle import TRUE
import os.path as osp, os
import matplotlib.pyplot as plt  
from searchEngine.invertedIndexer import invertedIndex
from searchEngine.tokenizer import tokenize
from searchEngine.search_interface import load_data
import numpy as np

_, index, _ = load_data()
sums = []
c = 23089
for term, values in index.items():
    doc_sum = 0
    for doc in values:
        indices = doc[2]
        doc_sum += (len(indices))
    sums.append((term, doc_sum))
sums = sorted(sums, key=lambda x: x[1])
#sums = sorted(sums, reverse=True)
print(sums)
X = list(range(1, (len(sums) +1)))

plt.title("Zipf Term Distribution")
plt.ylabel("Frequency")
plt.xlabel("Terms")
plt.xlim(0, 2000)
#plt.ylim(-0.01, 400)
plt.plot(X, sums)
plt.show()


