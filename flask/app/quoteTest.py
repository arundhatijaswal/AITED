from bs4 import BeautifulSoup
import json as m_json
import requests, random, re, string, random
import urllib2
import urllib
import sys
from TestCodeThesis import gen_thesis

topic, keyword = gen_thesis()
# print thesis
query1 = topic + " " + keyword + " site:brainyquote.com"
# print query1
query2 = urllib.urlencode ( { 'q' : query1 } )
response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query2 ).read()
json = m_json.loads ( response )
results = json [ 'responseData' ] [ 'results' ]
# print 'length of results: ', len(results)


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

# weburl = 'http://www.brainyquote.com/quotes/authors/w/walt_disney.html'  
weburl = results[0]["url"]
r = requests.get(weburl)  
# print r
req = urllib2.Request(weburl, headers=hdr)

response = urllib2.urlopen(req)
line = response.readline();
data = '';

while (len(line) != 0):    
    # print line
    data = data + line
    line = response.readline();



soup = BeautifulSoup(data)
# quotes = soup.find_all(class=re.compile("bqQuoteLink"))
# print weburl
print '"' + soup.find("span", { "class":"bqQuoteLink" }).text + '"'
print " - " + soup.find("div", {"class":"bq-aut"}).text

# for quote in soup.find_all("span", { "class":"bqQuoteLink" }):
#     print quote.text
#     break
