# -*- coding: utf-8 -*-
"""
Extracts the most frequent n-grams from text read from an indicated file.

Created on Sun Mar 15 20:55:35 2015

@author: Nirmalya Ghosh
"""

import gensim, heapq
from nltk.tokenize import sent_tokenize
   
   
def most_frequent_n_grams(n, f, q):
    """Gets the most frequent n-grams from text read from the indicated file
    
    n -- the 'n' of the n-gram
    f -- the file to be read
    q -- indicates how many most frequent n-grams needs to be returned
    """
    doc = open(f).read()
    sent_tokenize_list = sent_tokenize(doc.decode('utf8').replace(".",". "))
    ngrams = dict()
    for i in range(len(sent_tokenize_list) - n + 1):
        sentence = sent_tokenize_list[i]
        wordlist = []
        for word in gensim.utils.tokenize(sentence, lowercase=True, deacc=True, 
                                          errors="ignore") :
            wordlist.append(word)
        for ii in range(len(wordlist) - n + 1):
            ngram = tuple(wordlist[ii:ii+n])
            if ngram in ngrams:
                ngrams[ngram] += 1
            else:
                ngrams[ngram] = 1
    results = dict()
    for ngram, freq in heapq.nlargest(q, ngrams.iteritems(), 
                                      key=lambda (k, v): (v, k)):
        results[ngram] = freq
    return results
