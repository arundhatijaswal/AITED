import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string, random
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


def genThesis():
	""" google search API scraper that returns the 
	title of an article based on the selected topic 
	and keyword """
	query = raw_input ( '\nTopic: ' )
	keyword = raw_input ( '\nkeyword: ' )
	websites = {'businessinsider.com': 'h1', 'cnn.com': 'h1'}
	web = random.choice(websites.keys())
	queryText = 'reason why '
	query = queryText + query + ' and ' + keyword +' is important site:' + web
	query = urllib.urlencode ( { 'q' : query } )
	response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	json = m_json.loads ( response )
	results = json [ 'responseData' ] [ 'results' ]
	# print query 
	# print json

	print '\nSite searched: ', web
	print 'length of results: ', len(results)

	thesisURL = results[random.randint(0, (len(results) - 1))]['url']
	r = requests.get(thesisURL)
	data = r.text
	soup = BeautifulSoup(data)

	if websites[web] == 'h1':
	    thesisRaw = str(soup.h1)
	    thesisTemp = soup.h1.text
	else:
	    print('other token')

	print '\nGenerated Topic: ', thesisTemp, '\n'

	#print thesisRaw
	print 'text version--- ', thesisTemp
	# title = '\nTitle: ', re.sub(r'<|>|\/|h1', r'', thesisRaw), '\n'
	# print title

	mykeywords = [w for w in thesisTemp.split() if not w in stopwords.words('english')]
	print mykeywords
	
	return thesisTemp, keyword

	# to open the document and read the text

	# send generated topic to stop words to be cleaned
	# filtered_words = [w for w in topic.split() if not w in stopwords.words('english')]
	# print filtered_words


def main():
	query, keyword = genThesis()
	return query, keyword

if __name__ == "__main__":
	main()


