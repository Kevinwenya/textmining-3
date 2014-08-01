Sample Code For Text Mining Applications
==========================================

- **simple-nltk-webservice.py** : a very simple web service making use of NLTK and Bottle.py. Given text and a TopN (via an HTTP POST), it will extract the **named entities** and the **Top N** words (with the obvious punctuations and stopwords removed)