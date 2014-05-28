import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk.data

# Global variables
issues = {}
results = []


def genTopic(category):
	""" web scraper that returns the title and url from
	debate.org. This will form the thesis of our script """

	# first, take the topic and navigate to the debates.org website
	# search = raw_input ( '\nEnter Topic: ' )
	websites = ['http://www.debate.org/opinions/'+category+'/?sort=popular',
		   'http://www.debate.org/opinions/'+category+'/?p=2&sort=popular',
		   'http://www.debate.org/opinions/'+category+'/?p=3&sort=popular']

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

	# print '\n'
	# print colored(title, 'red')
	# print '===================================================== \n'

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
			tmps = temp.split()
			if len(tmps) > 3:
				count = 0
				for i in tmps:
					for j in keywords:
						# print stemmer(i).lower()+','+stemmer(j).lower()
						if stemmer(i).lower() == stemmer(j).lower():
							count += 1
							if count > 2:
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
			tmps = temp.split()
			if len(tmps) > 3:
				count = 0
				for i in tmps:
					for j in keywords:
						# print stemmer(i).lower()+','+stemmer(j).lower()
						if stemmer(i).lower() == stemmer(j).lower():
							count += 1
							if count > 2:
								opinions.append(' '.join(tmps))
								# print count
	if not opinions:
		genThesis(topic)
	else:
		# print 'Top Argument: '+opinions[0]+'\n'
		topArg = opinions[0].split()
		# get the first sentence in the top user's argument
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		support = ''.join(tokenizer.tokenize(userArg.strip())[0])

		thesis = opinions[0]+' '+support
		# print "Thesis: "
		# print thesis
	return title, thesis


def stemmer(word):
    """Stems inputted words"""

    # List of endings
    endings = ['s', 'ed', 'es', 'ly', 'ing', 'er', 'ers']
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'

    if len(word) > 3 and word[len(word)-1] == endings[0]:       # If it ends in 's'
        if word[len(word)-2:len(word)] == endings[2]:           # If it ends in 'es'
            if word[len(word)-4:len(word)-2] in ['ch', 'sh'] \
               or word[len(word)-3] in ['x','s'] \
               or word[len(word)-3] == 'o' and word[len(word)-4] in consonants: # If singular ends in an 'o'
                                                                                # preceded by a consonant
                return word[0:len(word)-2]                      # get rid of 'es'

            elif word[-3] == 'i':
                return word[0:len(word)-3] + 'y'

        elif word[-3:-1] == 'er':
            return word[0:len(word)-4]

                                                           # Otherwise, get rid of 's'
        return word[0:len(word)-1]


    # Handles words that end in 'ed' applied -> apply, mapped -> map
    elif len(word) > 3 and word[len(word)-2:len(word)] == endings[1]:     # Words that end in 'ed'

        if word[-3] == 'i':

            if word in ['tied', 'lied', 'died']: # Y doesn't change in these words
                return word[0:len(word)]
            else:
                return word[0:len(word)-3] + 'y' # Y does change in these words

        elif word[-3] == word[-4]:               # Ends in 'ed' and has a double consonant

            if word[-4:-2] == 'ss':             # If that double consonant is 'ss'
                return word[0:len(word)-2]

            else:                               # If it's not 'ss'
                return word[0:len(word)-3]

        elif word[-3] != word[-4]:              # Words without double consonants
            return word[0:len(word)-2]


    # Handles words that end in 'ly' gladly -> glad, merrily -> merry
    elif len(word) > 3 and word[-2:len(word)] == endings[3]:
        if word[-3] == 'i':
            return word[0:len(word)-3] + 'y'
        else:
            return word[0:len(word)-2]

    # 'ing' playing -> play
    elif len(word) > 3 and word[-3:len(word)] == endings[4]:
        if word[-3] == word[-4]:
            return word[0:len(word)-3]
        elif word[-3] != word[-4]:
            return word[0:len(word)-4]

    # 'er' spammer -> spam
    if len(word) > 3 and word[-2:len(word)] == endings[5]:
        if word[-3] == word[-4]:
            return word[0:len(word)-3]
        elif word[-3] != word[-4]:
            return word[0:len(word)-4]

    # If word not inflected, return as-is.
    else:
        return word

	# query = urllib.urlencode ( { 'q' : query } )
	# response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	# json = m_json.loads ( response )

	# # stores the results of the google search
	# results = json [ 'responseData' ] [ 'results' ]


	# # use the keywords to do a search for a topic
	# websites = ['cnn.com',
	# 			'huffingtonpost.com',
	# 			'businessinsider.com',
	# 			'www.nytimes.com'
	# ]

	# web = random.choice(websites)
	# query = 'reason why ' + title + ' site:' + web



	# if len(results) > 0:
	# 	thesisURL = results[random.randint(0, (len(results) - 1))]['url']
	# 	r = requests.get(thesisURL)
	# 	data = r.text
	# 	soup = BeautifulSoup(data)
	# 	# print soup.prettify()

	# 	title = str(soup.title).replace("<title>", "").replace("</title>", "")
	# 	print title
	# 	print thesisURL
	# else:
	# 	print 'Search returned zero (0) results. Trying again...', '\n'
	# 	genThesis()




# def main():
# 	genThesis()

# if __name__ == "__main__":
# 	main()