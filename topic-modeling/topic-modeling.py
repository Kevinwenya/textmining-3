# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 04:53:18 2015

@author: Nirmalya Ghosh
"""

from gensim import corpora, models, utils
import itertools, os

stoplist = set('for a of the and to in'.split())
# Alternatively, use gensim.parsing.preprocessing.STOPWRORDS

def iter_documents(top_directory):
    """
    Generator: iterate over all relevant files 
    (no matter how deep under top_directory), yielding documents 
    (=list of unicode tokens) read from one file at a time.
    """
    # Credit : http://bit.ly/1BqQBAD
    for root, dirs, files in os.walk(top_directory):
        for fname in filter(lambda fname: fname.endswith('.txt'), files):
            # Read each line as document 
            for line in open(os.path.join(root, fname)):
                yield tokenize(line, stoplist)


def tokenize(text, stoplist):
    # Output tokens are unicode strings, that won’t be processed any further
    return [token for token in  utils.simple_preprocess(text) \
            if token not in stoplist]


class TxtSubdirsCorpus(object):
    """
    Iterable: on each iteration, return bag-of-words vectors,
    one vector for each document.
 
    Process one document at a time using generators, never
    load the entire corpus into RAM.
 
    """
    # Credit : http://bit.ly/1BqQBAD
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.dictionary = corpora.Dictionary(iter_documents(top_dir))
 
    def __iter__(self):
        """
        Again, __iter__ is a generator => TxtSubdirsCorpus is a streamed iterable.
        """
        for tokens in iter_documents(self.top_dir):
            # transform tokens (strings) into a sparse vector, one at a time
            yield self.dictionary.doc2bow(tokens)

 
# that's it! the streamed corpus of sparse vectors is ready
corpus = TxtSubdirsCorpus(r'C:\nirmalya\dev\projects\textmining\topic-modeling')
once_ids = [tokenid for tokenid, docfreq in corpus.dictionary.dfs.iteritems() \
            if docfreq == 1]
corpus.dictionary.filter_tokens(once_ids) # remove words that appear only once
corpus.dictionary.compactify() # remove gaps in id sequence after words that were removed
#print(corpus.dictionary.token2id) # Prints word-id mapping
corpus.dictionary.save('testdictionary3.dict')# store the dictionary, for future reference

# print the corpus vectors
for vector in corpus:
    print vector

# Topics identified by LSI model
# Credit : http://stackoverflow.com/q/15016025
print "Topics identified by the LSI model"
lsi = models.LsiModel(corpus, id2word=corpus.dictionary, num_topics=2)
corpus_lsi = lsi[corpus]
for l,t in itertools.izip(corpus_lsi,corpus):
  print l,"#",t
print
for top in lsi.print_topics(2):
  print top
  print "------"
corpus_lsi = None

# Topics identified by the LDA model
print "Topics identified by the LDA model"
lda = models.LdaModel(corpus, id2word=corpus.dictionary, num_topics=2)
corpus_lda = lda[corpus]
for l,t in itertools.izip(corpus_lda,corpus):
  print l,"#",t
print
for i in range(0, lda.num_topics):
    print lda.print_topic(i)
    print "------"
