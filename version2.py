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
	""" web scraper that returns the list of issues found in the
	article that correspond to the topic """

	# based on selected topic, we will visit one of these sites
	data = {'education': 'http://www.huffingtonpost.com/lydia-dobyns/top-10-education-issues_b_2726942.html',
			'parenting': 'http://www.parenting.com/article/the-top-10-concerns-of-new-parents',
			'technology':'http://scottberkun.com/2011/the-top-10-unsolved-tech-problems-help-wanted/',
			'politics' : 'http://www.policymic.com/articles/21496/the-10-biggest-political-issues-we-ll-be-taking-about-in-2013',
			'fashion'  : 'http://smallbusiness.chron.com/top-ten-ethical-issues-fashion-business-21866.html'
			}

	topic = raw_input ( '\nEnter Topic: ' )
	
	if topic in data.keys():
		# if topic == 'education':
		# 	web = random.choice(data[topic])
		# else :
		web = data[topic]

	r = requests.get(web)
	data = r.text
	soup = BeautifulSoup(data)
	# print soup.prettify()
	
	# for each topic, gather all of the issues on that page and remove html tags
	if topic == 'education':
		results = soup.find('div', 'entry_body_text').find_all("strong")
		# print results
		for i in range(0, len(results)):
			x = str(results[i]).replace('<strong>', '').replace('</strong>', '')
			issues.append(x)
			# print x
		title = random.choice(issues)
		# return title
		handleEdu(title, web, soup)

	elif topic == 'parenting':
		results = soup.find_all("li")
		# print results
		for i in range(0, len(results)):
			x = str(results[i]).replace('<h5>', '').replace('</h5>', '')
			issues.append(x)
		print issues
		title = random.choice(issues)
		return title

	elif topic == 'technology':
		results = soup.find("ol").find_all("li")
		# print results
		for i in range(0, len(results)):
			x = str(results[i]).replace('<li>', '').replace('</li>', '')
			x = re.sub(r'\(([^)]+)\)', r'', x)
			# print x
			issues.append(x)
		# print issues
		title = random.choice(issues)
		handleTech(title, web, soup)


def handleEdu(title, web, soup):
	""" function for returning thesis statement regarding tehcnology"""
	print '\n', colored('Education', 'white')
	print ('\nIssue: Why '+ title +' is a problem within education')

	keys = [w for w in title.lower().split() if not w in stopwords.words('english')]
	print keys
	keywords = dePunc(keys) 
	# keys = ' '.join(keywords)
	print '\nStripped Keywords: ', keywords, '\n'

	# use the keywords to do a search for a topic
	websites = ['cnn.com', 
				'huffingtonpost.com',
				'businessinsider.com',
	]

	web = random.choice(websites)
	query = 'issue in education: ' + str(keys) + ' site:' + web

	query = urllib.urlencode ( { 'q' : query } )
	response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	json = m_json.loads ( response )
	results = json [ 'responseData' ] [ 'results' ]
	# print results

	if len(results) > 0:
		thesisURL = results[random.randint(0, (len(results) - 1))]['url']
		r = requests.get(thesisURL)
		data = r.text
		soup = BeautifulSoup(data)
		# print soup.prettify()

		title = str(soup.title).replace("<title>", "").replace("</title>", "")
		print title
		print ('URL: ' + thesisURL)
	else:
		print 'Search returned zero (0) results. Ending...', '\n'
		# handleTech(title, web, soup)





def dePunc(rawword):
    """ remove punctuation in the input string """
    L = [ c for c in rawword if 'A' <= c <= 'Z' or 'a' <= c <= 'z' ]
    word = ' '.join(L)
    return word


	# websites = {'www.usnews.com/opinion/articles': 'h1', 'cnn.com': 'h1', 'huffingtonpost.com': 'h1'}
	# web = random.choice(websites.keys())
	# web = 'list25.com'
	# phrase = ['list of challenges within ', 'list of problems in ', 'top issues in ']
	# querySearch = random.choice(phrase)

	# if keyword == '':
	# 	query = querySearch + topic + ' site:' + web
	# else:
	# 	query = querySearch + topic + ' and ' + keyword + ' site:' + web
	# query = 
	# query = urllib.urlencode ( { 'q' : query } )
	# response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	# json = m_json.loads ( response )

	# stores the results of the google search
	# results = json [ 'responseData' ] [ 'results' ]
	# print results.prettify()

	
	# results = soup.findAll("span", {"class": "q-title"})
	# print random.choice(results)

	# if len(results) > 0:
	# 	URL = results[random.randint(0, (len(results) - 1))]['url']
	# 	r = requests.get(URL)
	# 	data = r.text
	# 	soup = BeautifulSoup(data)
	# 	# print soup.prettify()

	# 	# print URL 
	# 	print '\nURL: ', URL

	# 	# get the list items
	# 	print soup.findAll("div", {"class": "list-entry"})

		
	# else:
	# 	print 'Search returned zero (0) results. Trying again...', '\n'
	# 	genTopic()





# def genTopic():
# 	""" google search API scraper that returns the 
# 	title of an article based on the selected topic 
# 	and keyword """
# 	# topic = raw_input ( '\nEnter Topic: ' )
# 	# keyword = raw_input ( 'Enter Keyword (optional): ' )
# 	topic = 'education'
# 	keyword = 'money'
# 	# websites = {'www.usnews.com/opinion/articles': 'h1', 'cnn.com': 'h1', 'huffingtonpost.com': 'h1'}
# 	# web = random.choice(websites.keys())
# 	web = 'list25.com'
# 	queryText = {'list of challenges within ': 'one', 'list of problems in ': 'two', 'top issues in ': 'three'}
# 	querySearch = random.choice(queryText.keys())

# 	if keyword == "":
# 		query = querySearch + topic + ' site:' + web
# 	else:
# 		query = querySearch + topic + ' and ' + keyword + ' site:' + web

# 	# query = queryText + keys + ' site:' + web
# 	query = urllib.urlencode ( { 'q' : query } )
# 	response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
# 	json = m_json.loads ( response )

# 	# stores the results of the google search
# 	results = json [ 'responseData' ] [ 'results' ]
# 	# print results.prettify()

# 	if len(results) > 0:
# 		# print '\nSite searched: ', web
# 		# print 'length of results: ', len(results)

# 		URL = results[random.randint(0, (len(results) - 1))]['url']
# 		# URL = "money.cnn.com"
# 		# URL = 'http://www.cnn.com/2011/12/02/opinion/vedder-college-costs/'
# 		r = requests.get(URL)
# 		data = r.text
# 		soup = BeautifulSoup(data)
# 		# print soup.prettify()

# 		# title = str(soup.title).replace("<title>", "").replace("</title>", "")
# 		# print title
# 		print '\nURL: ', URL

# 		response = alchemyapi.text('url', URL)

# 		if response['status'] == 'OK':
# 			# print('## Response Object ##')
# 			# print(json.dumps(response, indent=4))

# 			print('')
# 			print('## Text ##')
# 			print('text: ', response['text'].encode('utf-8'))
# 			print('')
# 		else:
# 			print('Error in text extraction call: ', response['statusInfo'])	

# 		# remove stopwords using nltk stop list
# 		# keywords = [w for w in topic2.split() if not w in stopwords.words('english')]
# 		# keys = ' '.join(keywords)
# 		# print 'Stripped Keywords: ', keys, '\n'	

# 		# if web == 'money.cnn.com': handleCNN(URL, soup)
# 		# elif web == 'businessinsider.com': handleBI(URL, soup)
# 		# elif web == 'huffingtonpost.com': handleHuff(URL, soup)
# 		# r = requests.get("http://money.cnn.com/2013/10/24/news/economy/american-skills/")
# 		# data = r.text
# 		# soup = BeautifulSoup(data)
# 		# handleCNN(URL, soup)
# 	else:
# 		print 'Search returned zero (0) results. Trying again...', '\n'
# 		genTopic()



# def handleCNN(link, data):
# 	""" when searching on cnn.com, this is how to proceed """

# 	# print title of article
# 	title = str(data.title).replace("<title>", "").replace("</title>", "")
# 	print '\nTopic: ', title, '\n'
# 	print '====================================================', '\n'
	
# 	# check the url to see what site it went to, then handle accordingly
# 	one = 'money.cnn.com'
# 	two = 'schoolsofthought.blogs.cnn.com'
# 	three = 'cnn.com'

# 	if link[7:20] == one:
# 		# print the subtitle of article as the topic
# 		thesis = str(data.h2).replace("<h2>", "").replace("</h2>", "")
# 		print 'Generated Thesis: ', colored(thesis, 'red'), '\n'
# 		# if it's in <i> tags, get the first paragraph instead
# 		# also, if it returns 'none' then try a different article
# 	# else if link[7:37] == two:


		
	# print data.prettify()

# print the first paragraph to see if it's a good thesis
# content = soup.find("div", {"id": "storytext"}).p
# print 'Generated Thesis: ', content

# topic = "11 Reasons To Ignore The Haters And Major In The Humanities "
# topic2 = "These Two Charts Prove A College Education Just Isn't Worth The Money Anymore"
# topic3 = "Americans lacking in basic skills"
# print '\nChosen Topic: ', topic2, '\n'


def main():
	genTopic()

if __name__ == "__main__":
	main()
