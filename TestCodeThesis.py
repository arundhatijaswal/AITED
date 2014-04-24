import urllib
import json as m_json
import requests, random, re, string, random
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


def genThesis():
	topic = raw_input ( '\nTopic: ' )
	keyword = raw_input ( '\nkeyword: ' )
	websites = {'businessinsider.com': 'h1', 'cnn.com': 'h1'}
	#web = random.choice(websites.keys())
	web = 'businessinsider.com'
	queryText = 'reason why '
	query = queryText + topic + ' and ' + keyword + ' is important site:' + web
	query = urllib.urlencode ( { 'q' : query } )
	response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	json = m_json.loads ( response )
	results = json [ 'responseData' ] [ 'results' ]
    # print 'length of results: ', len(results)

	thesisURL = results[random.randint(0, (len(results) - 1))]['url']
	r = requests.get(thesisURL)
	data = r.text
	soup = BeautifulSoup(data)


	#print thesisURL
	if websites[web] == 'h1':
	    thesisRaw = str(soup.h1)
	    thesisTemp = soup.h1.text
	else:
	    print('other token')

	#print thesisRaw
	print 'text version--- ', thesisTemp
	# title = '\nTitle: ', re.sub(r'<|>|\/|h1', r'', thesisRaw), '\n'
	# print title

	mykeywords = [w for w in thesisTemp.split() if not w in stopwords.words('english')]
	print mykeywords
	
	return topic, keyword

	# to open the document and read the text


	#print thesis
	# print(soup.get_text())

def main():
	query, keyword = genThesis()
	return query, keyword

if __name__ == "__main__":
	main()

# for result in results:
#     title = result['title']
#     url = result['url']   # was URL in the original and that threw a name error exception
#     print ( title + '; ' + url )


# import urllib
# import json as m_json
# <<<<<<< HEAD
# import requests, random, re, string
# from bs4 import BeautifulSoup

# query = raw_input ( '\nTopic: ' )
# queryText = 'issues in '
# query = queryText + query + ' site:businessinsider.com'
# query = urllib.urlencode ( { 'q' : query } )
# =======

# keyword = 'sports'
# searchQuery = 'issues in ' + keyword + ' site:businessinsider.com'

# query = urllib.urlencode ( { 'q' : searchQuery } )
# >>>>>>> FETCH_HEAD
# response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
# json = m_json.loads ( response )
# results = json [ 'responseData' ] [ 'results' ]

# <<<<<<< HEAD
# thesisURL = results[random.randint(0, (len(results) - 1))]['url']
# r = requests.get(thesisURL)
# data = r.text
# soup = BeautifulSoup(data)


# #print thesisURL
# thesisRaw = str(soup.h1)
# #print thesisRaw
# print '\nThesis: ', re.sub(r'<|>|\/|h1', r'', thesisRaw), '\n'
# #print thesis
# # print(soup.get_text())

# # for result in results:
# #     title = result['title']
# #     url = result['url']   # was URL in the original and that threw a name error exception
# #     print ( title + '; ' + url )
# =======


# for result in results:
#     title = result['titleNoFormatting']
#     #"""
#     if 'Business Insider' in title:
#         questionIndex = title.index('Business Insider')
#         newTitle = title[:questionIndex-3]
#         print newTitle
#     #"""
#     #print title
# >>>>>>> FETCH_HEAD
