# -*- coding: utf-8 -*-
"""
Simple web service making use of NLTK and Bottle.py

Currently the only endpoint is the 'extract-sentences-words', 
which performs the following operations
- Punctuation removal
- Stopwords removal
- Top N words
- Named entity extraction

Created on Thu Jul 31 21:32:03 2014

@author: Nirmalya Ghosh
"""

from bottle import post, request, response, run
from collections import Counter
from json import dumps
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import string

""" 
Extract sentences and a list of list of words and returns a JSON.
"""
@post('/extract-sentences-words')
def extractSentencesAndWords():
    text = request.forms.get('text')
    topN = int(request.forms.get("topN"))
    if topN is None:
        topN = 10
    sentences = [x.strip('"').strip("'") for x in extractSentences(text)]
    
    all_words = []
    list_of_lists = []
    for s in sentences:
        words = extractWords(s)
        all_words.extend(words)
        list_of_lists.append(words)
    
    named_entities = extractNamedEntities(sentences)
    
    filtered = [w for w in all_words if not w in stopwords.words('english')]
    count = Counter(filtered)
    
    data = { 'counts' : 
             { 'sentences':len(sentences), 'words':len(all_words), 
               'unique_words':sum(count.values())
             },
             'sentences': dumps(sentences),
             'words': dumps(filtered),
             'top_'+str(topN)+'_words':count.most_common(topN),
             'named_entities' : named_entities
           }
    response.content_type = 'application/json'
    return dumps(data)


def extractNamedEntities(sentences):
    tok_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tag_sentences = [nltk.pos_tag(sentence) for sentence in tok_sentences]
    cnk_sentences = nltk.batch_ne_chunk(tag_sentences, binary=True)
    all_named_entities = []
    for tree in cnk_sentences:      
        named_entities = extractNamedEntitiesFromChunkSentence(tree)
        all_named_entities.extend(named_entities)
    return list(set(all_named_entities))


def extractNamedEntitiesFromChunkSentence(cs):
    ne = []
    if hasattr(cs, 'node') and cs.node:
        if cs.node == 'NE':
            ne.append(' '.join([child[0] for child in cs]))
        else:
            for child in cs:
                ne.extend(extractNamedEntitiesFromChunkSentence(child))   
    return ne


def extractSentences(text):
    sentences = sent_tokenize(text)
    return sentences


def extractWords(sentence):
    no_punctuation = sentence.translate(None, string.punctuation)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens


run(host='localhost', port=8080, debug=True)