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

""" 
THE IDEA BEHIND THIS....

we need a way to generate a better "title" for each chosen topic.

Version 1: no keywords
======================
1. user selects a topic out of a list of 5-6 topics
2. the topic chosen will determine the specific site that is used
	a.) the site that's used is a predetermined one that lists issues related
		to the topic and will be easy for us to extract info from
3. based on the topic and website, the "title" is generated 


Version 2: with keywords
======================== 
"""

def genTopic():
	""" web scraper that returns the title debate from debate.org. 
	this will serve as the main topic of our script """ 

	# first, take the topic and navigate to the debates.org website
	search = raw_input ( '\nEnter Topic: ' )
	web = 'http://www.debate.org/opinions/'+search
	
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
	print '\n', colored(title, 'red')

	# remove stopwords using nltk stop list and print the keywords
	keywords = [w for w in title.lower().split() if not w in stopwords.words('english')]
	keys = ' '.join(keywords)
	print '\nStripped Keywords: ', keys, '\n'

	# use the keywords to do a search for a topic
	websites = {'www.usnews.com/opinion/articles': 'h1', 
				'cnn.com': 'h1', 
				'huffingtonpost.com': 'h1',
				'businessinsider.com': 'h1',
				'www.nytimes.com': 'h1'
		}
	web = random.choice(websites.keys())
	query = keys + ' site:' + web

	query = urllib.urlencode ( { 'q' : query } )
	response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	json = m_json.loads ( response )

	# stores the results of the google search
	results = json [ 'responseData' ] [ 'results' ]
	# print results.prettify()

	if len(results) > 0:
		thesisURL = results[random.randint(0, (len(results) - 1))]['url']

		r = requests.get(thesisURL)
		data = r.text
		soup = BeautifulSoup(data)
		# print soup.prettify()

		title = str(soup.title).replace("<title>", "").replace("</title>", "")
		print title
	else:
		print 'Search returned zero (0) results. Trying again...', '\n'
		genThesis()




def main():
	genThesis()

if __name__ == "__main__":
	main()