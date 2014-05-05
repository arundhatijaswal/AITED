import urllib
import json as m_json

keyword = 'sports'
searchQuery = 'issues in ' + keyword + ' site:businessinsider.com'

query = urllib.urlencode ( { 'q' : searchQuery } )
response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
json = m_json.loads ( response )
results = json [ 'responseData' ] [ 'results' ]



for result in results:
    title = result['titleNoFormatting']
    #"""
    if 'Business Insider' in title:
        questionIndex = title.index('Business Insider')
        newTitle = title[:questionIndex-3]
        print newTitle
    #"""
    #print title
