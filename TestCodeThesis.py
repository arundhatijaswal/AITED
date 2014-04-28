import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string, random
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from sets import Set


def textFinder(results, synonyms):
    challengeURL = results[random.randint(0, (len(results) - 1))]['url']

    print challengeURL
    r = requests.get(challengeURL)
    data = r.text
    soup = BeautifulSoup(data)
    # print snippets
    for syn in synonyms:
        # print syn
        snippets = [t.parent for t in soup.findAll(text=re.compile(syn))]
        if len(snippets) != 0:
            print random.choice(snippets).text
            return 0
        else:
            print syn, " not found"
    return -1


def genThesis():
    """ google search API scraper that returns the
	title of an article based on the selected topic 
	and keyword """
    topic = raw_input('\nTopic: ')
    keyword = raw_input('\nkeyword: ')
    websites = {'businessinsider.com': 'h1', 'cnn.com': 'h1'}
    web = random.choice(websites.keys())
    queryText = 'reason why '
    query = queryText + topic + ' and ' + keyword + ' is important site:' + web
    query = urllib.urlencode({'q': query})
    response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query).read()
    json = m_json.loads(response)
    results = json['responseData']['results']
    # print query
    # print json

    print '\nSite searched: ', web
    print 'length of results: ', len(results)

    thesisURL = results[random.randint(0, (len(results) - 1))]['url']

    print thesisURL
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

    thesisTemp = thesisTemp.lower()
    mykeywords = [w for w in thesisTemp.split() if not w in stopwords.words('english')]
    mykeywordsstr = []
    for word in mykeywords:
        try:
            mykeywordsstr.append(str(word))
        except:
            pass
    print mykeywordsstr
    #
    #
    #
    #generate the bottleneck section
    #
    #
    #
    queryText = 'biggest challenge in ' + topic + " " + keyword
    for word in mykeywordsstr:
        queryText = queryText + ' ' + word
    queryText = urllib.urlencode({'q': queryText})
    response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + queryText).read()
    json = m_json.loads(response)
    results = json['responseData']['results']
    # print query
    # print json

    print 'length of results: ', len(results)

    syns_tmp = wordnet.synsets('challenge')
    syns = [l.name for s in syns_tmp for l in s.lemmas]
    syns_set = Set(syns)
    for syn in syns_set:
        syn.replace("_", " ")
    if textFinder(results, syns_set) == -1:
        print "no bottleneck found"

    #
    #
    #
    #generate the solution section
    #
    #
    #
    queryText = 'solution to ' + topic + " " + keyword
    for word in mykeywordsstr:
        queryText = queryText + ' ' + word
    queryText = urllib.urlencode({'q': queryText})
    response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + queryText).read()
    json = m_json.loads(response)
    results = json['responseData']['results']
    # print query
    # print json

    print 'length of results: ', len(results)

    syns_tmp = wordnet.synsets('solution')
    syns = [l.name for s in syns_tmp for l in s.lemmas]
    syns_set = Set(syns)
    for syn in syns_set:
        syn.replace("_", " ")
    if textFinder(results, syns_set) == -1:
        print "no solution found"
        
        
        
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


