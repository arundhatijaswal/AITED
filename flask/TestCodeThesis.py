import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string, random
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from sets import Set


def text_find(results, synonyms):
    challenge_url = results[random.randint(0, (len(results) - 1))]['url']

    print challenge_url
    r = requests.get(challenge_url)
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


def gen_thesis():
    """ google search API scraper that returns the
    title of an article based on the selected topic
    and keyword """
    topic = raw_input('\nTopic: ')
    keyword = raw_input('\nkeyword: ')
    websites = {'businessinsider.com': 'h1', 'cnn.com': 'h1'}
    web = random.choice(websites.keys())
    query_text = 'reason why '
    query = query_text + topic + ' and ' + keyword + ' is important site:' + web
    query = urllib.urlencode({'q': query})
    response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query).read()
    json = m_json.loads(response)
    results = json['responseData']['results']
    # print query
    # print json

    print '\nSite searched: ', web
    print 'length of results: ', len(results)

    thesis_url = results[random.randint(0, (len(results) - 1))]['url']

    print thesis_url
    r = requests.get(thesis_url)
    data = r.text
    soup = BeautifulSoup(data)

    if websites[web] == 'h1':
        thesis_raw = str(soup.h1)
        thesis_temp = soup.h1.text
    else:
        print('other token')

    print '\nGenerated Topic: ', thesis_temp, '\n'

    #print thesis_raw
    print 'text version--- ', thesis_temp
    # title = '\nTitle: ', re.sub(r'<|>|\/|h1', r'', thesis_raw), '\n'
    # print title

    thesis_temp = thesis_temp.lower()
    mykeywords = [w for w in thesis_temp.split() if not w in stopwords.words('english')]
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
    query_text = 'biggest challenge in ' + topic + " " + keyword
    for word in mykeywordsstr:
        query_text = query_text + ' ' + word
    query_text = urllib.urlencode({'q': query_text})
    response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query_text).read()
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
    if text_find(results, syns_set) == -1:
        print "no bottleneck found"

    #
    #
    #
    #generate the solution section
    #
    #
    #
    query_text = 'solution to ' + topic + " " + keyword
    for word in mykeywordsstr:
        query_text = query_text + ' ' + word
    query_text = urllib.urlencode({'q': query_text})
    response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query_text).read()
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
    if text_find(results, syns_set) == -1:
        print "no solution found"
    #
    #
    #
    #generate the impact section
    #
    #
    #
    # query_text = 'impact of ' + topic + " " + keyword
    # for word in mykeywordsstr:
    #     query_text = query_text + ' ' + word
    # query_text = urllib.urlencode({'q': query_text})
    # response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query_text).read()
    # json = m_json.loads(response)
    # results = json['responseData']['results']
    # # print query
    # # print json
    #
    # print 'length of results: ', len(results)
    #
    # syns_tmp = wordnet.synsets('impact')
    # syns = [l.name for s in syns_tmp for l in s.lemmas]
    # syns_set = Set(syns)
    # for syn in syns_set:
    #     syn.replace("_", " ")
    # if textFinder(results, syns_set) == -1:
    #     print "no impact found"
    return thesis_temp, keyword
# to open the document and read the text

# send generated topic to stop words to be cleaned
# filtered_words = [w for w in topic.split() if not w in stopwords.words('english')]
# print filtered_words


def main():
    query, keyword = gen_thesis()
    return query, keyword


if __name__ == "__main__":
    main()

