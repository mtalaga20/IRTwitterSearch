"""
Create index function using the search engine
"""
import sys
import os.path as osp, os

from searchEngine.invertedIndexer import invertedIndex
from searchEngine.tokenizer import tokenize
from searchEngine.search_interface import create_Index

create_Index()