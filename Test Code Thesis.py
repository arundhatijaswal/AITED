import urllib
import json as m_json
query = raw_input ( 'Query: ' )
import requests, random, re, string
from bs4 import BeautifulSoup

query = raw_input ( '\nTopic: ' )
queryText = 'issues in '
query = queryText + query + ' site:businessinsider.com'
query = urllib.urlencode ( { 'q' : query } )
response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
json = m_json.loads ( response )
results = json [ 'responseData' ] [ 'results' ]
for result in results:
    title = result['title']
    url = result['url']   # was URL in the original and that threw a name error exception
    print ( title + '; ' + url )

thesisURL = results[random.randint(0, (len(results) - 1))]['url']
r = requests.get(thesisURL)
data = r.text
soup = BeautifulSoup(data)


#print thesisURL
thesisRaw = str(soup.h1)
#print thesisRaw
print '\nThesis: ', re.sub(r'<|>|\/|h1', r'', thesisRaw), '\n'
#print thesis
# print(soup.get_text())

# for result in results:
#     title = result['title']
#     url = result['url']   # was URL in the original and that threw a name error exception
#     print ( title + '; ' + url )
