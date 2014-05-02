import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from termcolor import colored

# Global variables
issues = []
results = []
keywords = []


def genTopic():
	""" web scraper that returns the title debate from debate.org. 
	this will serve as the main topic of our script """ 

	# first, take the topic and navigate to the debates.org website
	search = raw_input ( '\nEnter Topic: ' )
	websites = ['http://www.debate.org/opinions/'+search+'/?sort=popular', 
		   'http://www.debate.org/opinions/'+search+'/?p=2&sort=popular',
		   'http://www.debate.org/opinions/'+search+'/?p=3&sort=popular']
	
	web = random.choice(websites)
	r = requests.get(web)
	data = r.text
	soup = BeautifulSoup(data)
	# print soup.prettify()

	# gather all of the debates on that page and remove html tags
	results = soup.find_all("span", "q-title")
	for i in range(0, len(results)):
		x = str(results[i]).replace('<span class="q-title">', '').replace('</span>', '')
		issues.append(x)

	title = random.choice(issues)
	return title


def genThesis():
	title = genTopic()

	# print a random topic
	print '\n', colored(title, 'white')

	# remove stopwords using nltk stop list and print the keywords
	keywords = [w for w in title.lower().split() if not w in stopwords.words('english')]
	keys = ' '.join(keywords)
	print '\nStripped Keywords: ', keys, '\n'

	# use the keywords to do a search for a topic
	websites = ['cnn.com', 
				'huffingtonpost.com',
				'businessinsider.com',
				'www.nytimes.com'
	]

	web = random.choice(websites)
	query = 'reason why ' + title + ' site:' + web

	query = urllib.urlencode ( { 'q' : query } )
	response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	json = m_json.loads ( response )

	# stores the results of the google search
	results = json [ 'responseData' ] [ 'results' ]

	if len(results) > 0:
		thesisURL = results[random.randint(0, (len(results) - 1))]['url']
		r = requests.get(thesisURL)
		data = r.text
		soup = BeautifulSoup(data)
		# print soup.prettify()

		title = str(soup.title).replace("<title>", "").replace("</title>", "")
		print title
		print thesisURL
	else:
		print 'Search returned zero (0) results. Trying again...', '\n'
		genThesis()




def main():
	genThesis()

if __name__ == "__main__":
	main()