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
        print " ".join(ngram)+", "+str(freq)
    return results


def most_frequent_phrases(min_n_gram, max_n_gram, file_name, how_many):
    tmp_results = dict()
    for n in range(min_n_gram,max_n_gram+1):
        tmp_results.update(most_frequent_n_grams(n, file_name, how_many))
        most_frequent_phrases = dict()
        # We want to get rid of the shorter n-gram if it has same support
        # First, sort the n-grams
        l = []
        for ngram, freq in tmp_results.iteritems():
            l.append(ngram)
            l = sorted(l, key=lambda tup: tup[0])
        # Next, compare and trim
        prev_ngram = None
        for ngram in l:
            print ngram
            if prev_ngram is not None:
                prev_ngram_freq = tmp_results[prev_ngram]
                curr_ngram_freq = tmp_results[ngram]
                if prev_ngram_freq == curr_ngram_freq:
                    print("==> '%s' has same frequency (%s) as '%s', so deleting the shorter n-gram" %\
                    (" ".join(prev_ngram), prev_ngram_freq, " ".join(ngram)) )
                    del tmp_results[prev_ngram]
            prev_ngram = ngram

    print "====== most frequent phrases ======"
    for ngram, freq in heapq.nlargest(how_many, tmp_results.iteritems(), key=lambda (k, v): (v, k)):
        print " ".join(ngram), freq
        most_frequent_phrases[ngram] = freq

    return most_frequent_phrases

#most_frequent_n_grams(7, "C:/nirmalya/dev/projects/textmining/paper-abstracts.txt", 15)
most_frequent_phrases(6,24,"C:/nirmalya/dev/projects/textmining/paper-abstracts.txt", 20)