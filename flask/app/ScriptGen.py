import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string, random
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from sets import Set
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from google import search
import thesis2
from alchemyapi import AlchemyAPI

section = []
# stemmer = WordNetLemmatizer()
stemmer = PorterStemmer()
alchemyapi = AlchemyAPI()

def extract_keywords(myThesis):
    myThesis_temp = myThesis.lower()
    Keywords = [w for w in myThesis_temp.split() if not w in stopwords.words('english')]
    Keywordsstr = []
    for word in Keywords:
        try:
            Keywordsstr.append(str(word))
        except:
            pass
    # print "Keywordsstr: ", Keywordsstr
    return Keywordsstr

def text_find(query_text, queryKeyword, url_used):
    #print "query test: ", query_text

    # query_text = urllib.urlencode({'q': query_text})
    # response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query_text).read()

    urls = search(query_text, stop=10, pause=2.0)

    # json = m_json.loads(response)
    # results = json['responseData']['results']


    syns_tmp = wordnet.synsets(queryKeyword)
    syns = [l.name for s in syns_tmp for l in s.lemmas]
    syns_set = Set(syns)


    # section_url = results[random.randint(0, (len(results) - 1))]['url']
    section_url = random.choice(list(enumerate(urls)))[1]

    if ".pdf" in section_url or ".doc" in section_url:
        return -1, section_url
    if url_used:
        while section_url in url_used:
            # section_url = results[random.randint(0, (len(results) - 1))]['url']
            section_url = random.choice(list(enumerate(urls)))[1]

    print section_url
    r = requests.get(section_url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    # print snippets
    for syn in syns_set:
        # print syn
        syn = syn.replace("_", " ")
        # syn = stemmer.lemmatize(syn).lower()
        syn = stemmer.stem(syn)
        # snippets = [t.parent for t in soup.findAll(text=re.compile(syn))]
        body = soup.findAll('p')
        # print len(body)
        for i in body:
            i = i.text
            if syn in i:
                section_text = i
                print section_text
                return 1, section_text




        # print "stemmed syn: ", syn


        #
        # if len(snippets) != 0:
        #     section_text = random.choice(snippets).text
        #     print section_text
        #     return 1, section_text


        # else:
        #     print syn, " not found"
    return -1, section_url


def gen_thesis(topic):
    """ google search API scraper that returns the
    title of an article based on the selected topic
    and keyword """

    myTitle, myOne, mySupport = thesis2.genThesis(topic)
    while myTitle == "" or myOne == "" or mySupport == "":
        myTitle, myOne, mySupport = thesis2.genThesis(topic)
    myThesis = thesis2.introduction(myTitle, myOne, mySupport)
    print "\nTitle: ", myTitle
    print "\nThesis: ", myThesis
    thesisKeywords = extract_keywords(myTitle)
    section.append(myTitle)
    section.append(myThesis)

    Tresponse = alchemyapi.taxonomy('text',myThesis)
    if Tresponse['status'] == 'OK':
        for category in Tresponse['taxonomy']:
            print category['label'], ' : ', category['score']
            if category.has_key('confident'):
                print 'confident: ', category['confident']
    else:
        print('Error in concept tagging call: ', response['statusInfo'])

    #
    # return
    #
    #
    #generate the importance section
    #
    #
    #
    query_text = 'importance of ' + topic
    for word in thesisKeywords:
        query_text = query_text + ' ' + word
    queryKeyword = 'importance'
    print '\nimportance section'
    used_url = []
    success, importance = text_find(query_text, queryKeyword, used_url)
    while(success == -1):
        used_url.append(importance)
        success, importance = text_find(query_text, queryKeyword, used_url)
    section.append(importance)
    importance = importance.encode('utf8')

    response = alchemyapi.taxonomy('text',importance)
    if response['status'] == 'OK':
        for category in response['taxonomy']:
            for categ in Tresponse['taxonomy']:
                if category['label'].rstrip('/') == categ['label'].rstrip('/'):
                    print 'related\n', category['label'], ' : ', category['score']
                    if category.has_key('confident'):
                        print 'confident: ', category['confident']
                print 'unrelated\n', category['label'], ' : ', category['score']
                if category.has_key('confident'):
                    print 'confident: ', category['confident']
    else:
        print('Error in concept tagging call: ', response['statusInfo'])

    #
    #
    #
    #generate the bottleneck section
    #
    #
    #
    query_text = 'biggest challenge in ' + topic
    for word in thesisKeywords:
        query_text = query_text + ' ' + word
    queryKeyword = 'challenge'
    print '\nchallenge section'
    used_url = []
    success, bottleneck = text_find(query_text, queryKeyword, used_url)
    bottleneck = bottleneck.encode('utf8')
    while(success == -1):
        used_url.append(bottleneck)
        success, bottleneck = text_find(query_text, queryKeyword, bottleneck)
    section.append(bottleneck)

    response = alchemyapi.taxonomy('text',bottleneck)
    if response['status'] == 'OK':
        for category in response['taxonomy']:
            for categ in Tresponse['taxonomy']:
                if category['label'].rstrip('/') == categ['label'].rstrip('/'):
                    print 'related\n', category['label'], ' : ', category['score']
                    if category.has_key('confident'):
                        print 'confident: ', category['confident']
                print 'unrelated\n', category['label'], ' : ', category['score']
                if category.has_key('confident'):
                    print 'confident: ', category['confident']
    else:
        print('Error in concept tagging call: ', response['statusInfo'])

    # query_text = urllib.urlencode({'q': query_text})
    # response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query_text).read()
    # json = m_json.loads(response)
    # results = json['responseData']['results']
    # # print query
    # # print json

    # print 'length of results: ', len(results)

    # syns_tmp = wordnet.synsets('challenge')
    # syns = [l.name for s in syns_tmp for l in s.lemmas]
    # syns_set = Set(syns)
    # for syn in syns_set:
    #     syn.replace("_", " ")
    # if text_find(results, syns_set) == -1:
    #     print "no bottleneck found"

    #
    #
    #
    #generate the solution section
    #
    #
    #
    query_text = 'remedy for ' + topic
    for word in thesisKeywords:
        query_text = query_text + ' ' + word
    queryKeyword = 'remedy'
    # print query_text
    print '\nsolution section'
    used_url = []
    success, solution = text_find(query_text, queryKeyword, used_url)
    solution = solution.encode('utf8')
    while(success == -1):
        used_url.append(solution)
        success, solution = text_find(query_text, queryKeyword, solution)
    section.append(solution)

    response = alchemyapi.taxonomy('text',solution)
    if response['status'] == 'OK':
        for category in response['taxonomy']:
            for categ in Tresponse['taxonomy']:
                if category['label'].rstrip('/') == categ['label'].rstrip('/'):
                    print 'related\n', category['label'], ' : ', category['score']
                    if category.has_key('confident'):
                        print 'confident: ', category['confident']
                print 'unrelated\n', category['label'], ' : ', category['score']
                if category.has_key('confident'):
                    print 'confident: ', category['confident']
    else:
        print('Error in concept tagging call: ', response['statusInfo'])

    # query_text = urllib.urlencode({'q': query_text})
    # response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query_text).read()
    # json = m_json.loads(response)
    # results = json['responseData']['results']
    # # print query
    # # print json

    # print 'length of results: ', len(results)

    # syns_tmp = wordnet.synsets('solution')
    # syns = [l.name for s in syns_tmp for l in s.lemmas]
    # syns_set = Set(syns)
    # for syn in syns_set:
    #     syn.replace("_", " ")
    # if text_find(results, syns_set) == -1:
    #     print "no solution found"
    #
    #
    #
    #generate the impact section
    #
    #
    #
    query_text = 'impact of ' 
    solutionKeywords = extract_keywords(solution)
    # for word in solutionKeywords:
    #     query_text = query_text + ' ' + word
    #     print word
    # query_text = query_text + ' on ' + topic
    for word in thesisKeywords:
        query_text = query_text + ' ' + word
        # print word
    queryKeyword = 'impact'
    print '\nimpact section'
    used_url = []
    success, impact = text_find(query_text, queryKeyword, used_url)
    impact = impact.encode('utf8')
    while(success == -1):
        used_url.append(impact)
        success, impact = text_find(query_text, queryKeyword, impact)
    section.append(impact)

    response = alchemyapi.taxonomy('text',impact)
    if response['status'] == 'OK':
        for category in response['taxonomy']:
            for categ in Tresponse['taxonomy']:
                if category['label'].rstrip('/') == categ['label'].rstrip('/'):
                    print 'related\n', category['label'], ' : ', category['score']
                    if category.has_key('confident'):
                        print 'confident: ', category['confident']
                print 'unrelated\n', category['label'], ' : ', category['score']
                if category.has_key('confident'):
                    print 'confident: ', category['confident']
    else:
        print('Error in concept tagging call: ', response['statusInfo'])

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
    # return thesis_temp, keyword

    return section
# to open the document and read the text

# send generated topic to stop words to be cleaned
# filtered_words = [w for w in topic.split() if not w in stopwords.words('english')]
# print filtered_words


def main():
    topic = raw_input("Enter topic: ")
    gen_thesis(topic)
    # query, keyword =
    # return query, keyword


if __name__ == "__main__":
    main()


 # topic = raw_input('\nTopic: ')
    # keyword = raw_input('\nkeyword: ')
    # websites = {'businessinsider.com': 'h1', 'cnn.com': 'h1'}
    # web = random.choice(websites.keys())
    # query_text = 'reason why '
    # query = query_text + topic + ' and ' + keyword + ' is important site:' + web
    # query = urllib.urlencode({'q': query})
    # response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query).read()
    # json = m_json.loads(response)
    # results = json['responseData']['results']
    # # print query
    # # print json

    # print '\nSite searched: ', web
    # print 'length of results: ', len(results)

    # thesis_url = results[random.randint(0, (len(results) - 1))]['url']

    # print thesis_url
    # r = requests.get(thesis_url)
    # data = r.text
    # soup = BeautifulSoup(data)

    # if websites[web] == 'h1':
    #     thesis_raw = str(soup.h1)
    #     thesis_temp = soup.h1.text
    # else:
    #     print('other token')

    # print '\nGenerated Topic: ', thesis_temp, '\n'

    # #print thesis_raw
    # print 'text version--- ', thesis_temp
    # # title = '\nTitle: ', re.sub(r'<|>|\/|h1', r'', thesis_raw), '\n'
    # # print title

    # thesis_temp = thesis_temp.lower()
    # mykeywords = [w for w in thesis_temp.split() if not w in stopwords.words('english')]
    # mykeywordsstr = []
    # for word in mykeywords:
    #     try:
    #         mykeywordsstr.append(str(word))
    #     except:
    #         pass
    # print mykeywordsstr
