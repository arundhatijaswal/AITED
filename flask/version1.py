import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk.data
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Global variables
issues = {}
results = []
stemmer = WordNetLemmatizer()


def genTopic(category):
	""" web scraper that returns the title and url from 
	debate.org. This will form the thesis of our script """ 

	# first, take the topic and navigate to the debates.org website
	websites = ['http://www.debate.org/opinions/'+category+'/?sort=popular', 
		   'http://www.debate.org/opinions/'+category+'/?p=2&sort=popular']
	
	web = random.choice(websites)
	r = requests.get(web)
	data = r.text
	soup = BeautifulSoup(data)
	# print soup.prettify()

	results = soup.find_all("p", "l-name") 
	for i in range(0, len(results)):
		
		# get the titles
		temp = results[i].find("span", "q-title").text
		tmps = temp.split()

		# for each title, make sure it's appropriate length and get the url
		# then, add title and url to dictionary
		if len(tmps) > 5 and len(tmps) < 20: 
			title = ' '.join(tmps)
			url = 'http://www.debate.org'+results[i].find("a").get('href')+'?nsort=3&ysort=3'
			issues[str(title)] = str(url)

	topic = random.choice(issues.keys())
	link = issues[topic]
	return topic, link, category


def genThesis(topic):
	""" 
	in order to generate the thesis, we need the following:
		- title
		- url
		- rating = opinion
		- thesis: the bold text for the yes or no section 
			** the thesis has to contain some keywords from the title
		- support: the sentence following the yes or no bold statement
	"""

	title, url, category = genTopic(topic)

	print '\n'
	print title
	print '===================================================== \n'

	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	# remove stopwords using nltk stop list and print the keywords
	keywords = [w for w in title.lower().split() if not w in stopwords.words('english')]
	keys = ' '.join(keywords)
	
	vote = soup.find("span", "no-text").text
	strings = str(vote).split()
	rating = int(strings[0][:-1]) # this is the 'no' rating
	opinions = []
	args = []
	argSplit = []

	if rating > 50:
		# print rating, " No"
		args = soup.find('div', attrs={'id':'no-arguments'}).find_all("li", "hasData")
		# print args
		for i in range(0, len(args)):
			# find the list items
			temp = args[i].find("h2").text
			userArg = args[i].find("p").text
			# print userArg
			tmps = temp.split()
			print tmps

			if len(tmps) > 3: 
				count = 0
				for i in tmps:
					for j in keywords:
						# print stemmer.lemmatize(i).lower()+','+stemmer.lemmatize(j).lower()
						if stemmer.lemmatize(i).lower() == stemmer.lemmatize(j).lower():
							count += 1
							if count > 1:
								opinions.append(' '.join(tmps))
								# print count
	else:
		# print rating, " Yes"
		args = soup.find('div', attrs={'id':'yes-arguments'}).find_all("li", "hasData")
		# print args
		for i in range(0, len(args)):
			# find the list items
			temp = args[i].find("h2").text
			userArg = args[i].find("p").text
			# print userArg
			tmps = temp.split()
			print tmps

			if len(tmps) > 3: 
				count = 0
				for i in tmps:
					for j in keywords:
						# print stesmmer.lemmatize(i).lower()+','+stemmer.lemmatize(j).lower()
						if stemmer.lemmatize(i).lower() == stemmer.lemmatize(j).lower():
							count += 1
							if count > 1:
								opinions.append(' '.join(tmps))
	
	# get the first sentence in the top user's argument
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	support = ''.join(tokenizer.tokenize(userArg.strip())[0])

	if not opinions:
		genThesis(topic)
	elif not userArg:
		genThesis(topic)
	else:
		# print 'Top Argument: '+opinions[0]+'\n'
		topArg = opinions[0].split()
		thesis = opinions[0]+' '+support
		print "Thesis: "
		print thesis
		# return title, thesis


# def cleaner(topArg, support):
# 	""" this functions improves the thesis generator in 3 ways:
# 	1.) fix the topArg by removing yes or no statements
# 	2.) include punctuations
# 	3.) make sure top argument isn't repeated in the support part
# 	"""

# 	# temp = topArg.lower()

# 	# clean top argument
# 	if "Yes." or "No." in topArg[0]:
# 		sent = topArg[1:]
# 		print sent
# 	# print topArg
# 	return

def main():
	category = raw_input ( '\nEnter Topic: ' )
	genThesis(category)

if __name__ == "__main__":
	main()