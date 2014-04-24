import urllib
import json as m_json
import requests, random, re, string
from urllib.request import urlopen
from bs4 import BeautifulSoup


# query = raw_input ( '\nTopic: ' )
req = urllib.request('http://www.brainyquote.com/quotes/authors/w/walt_disney.html', headers={'User-Agent': 'Mozilla/5.0'})
data = urlopen(req).read()
# data = urllib.urlopen ('http://www.brainyquote.com/quotes/authors/w/walt_disney.html', headers={'User-Agent': 'Mozilla/5.0'}).read()
print data
soup = BeautifulSoup(data)
quotes = soup.find_all('span')
for quote in soup.find_all('span'):
    print quote.attrs
    # if quote['class'] == 'bqQuoteLink'
    #         print quotehttp://www.brainyquote.com/quotes/authors/w/walt_disney.html
