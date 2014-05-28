import urllib2, cookielib
import thesis2, debate_content
from google import search
from bs4 import BeautifulSoup
from random import choice

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from alchemyapi import AlchemyAPI

import signal
from contextlib import contextmanager


def extract_keywords(string):
    keywords = ' '.join([word for word in string.lower().split() if word not in stopwords.words('english')])
    return keywords


class Thesis:
    def __init__(self, topic):   
        title, main_point, support, url = thesis2.genThesis(topic)
        self.title = title
        self.url = url
        self.thesis = thesis2.introduction(title, main_point, support)
        self.keywords = extract_keywords(title) # keywords from title        
        return

    def __repr__(self):
        print "\nTitle: %s \n " % self.title
        print "\nThesis: \n%s \n " % self.thesis
        print "\nKeywords: \n%s \n " % self.keywords
        
my_thesis = Thesis('education')
print my_thesis
