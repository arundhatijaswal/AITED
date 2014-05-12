import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string, random
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from sets import Set
import version1


def extract_keywords(myThesis):
    myThesis_temp = myThesis.lower()
    Keywords = [w for w in myThesis_temp.split() if not w in stopwords.words('english')]
    Keywordsstr = []
    for word in Keywords:
        try:
            Keywordsstr.append(str(word))
        except:
            pass
    # print Keywordsstr
    return Keywordsstr

def text_find(query_text, queryKeyword):

    query_text = urllib.urlencode({'q': query_text})
    response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query_text).read()
    json = m_json.loads(response)
    results = json['responseData']['results']
    # print query
    # print json

    # print 'length of results: ', len(results)

    syns_tmp = wordnet.synsets(queryKeyword)
    syns = [l.name for s in syns_tmp for l in s.lemmas]
    syns_set = Set(syns)


    section_url = results[random.randint(0, (len(results) - 1))]['url']

    print section_url
    r = requests.get(section_url)
    data = r.text
    soup = BeautifulSoup(data)
    # print snippets
    for syn in syns_set:
        # print syn
        syn = syn.replace("_", " ")
        snippets = [t.parent for t in soup.findAll(text=re.compile(syn))]
        if len(snippets) != 0:
            section_text = random.choice(snippets).text
            print section_text
            return section_text
        # else:
        #     print syn, " not found"
    return "no section text found"


def gen_thesis(topic):
    """ google search API scraper that returns the
    title of an article based on the selected topic
    and keyword """

    myTitle, myThesis = version1.genThesis(topic)
    while myTitle == "" or myThesis == "":
        myTitle, myThesis = version1.genThesis(topic)
    thesisKeywords = extract_keywords(myThesis)

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
    text_find(query_text, queryKeyword)


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
    text_find(query_text, queryKeyword)
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
    query_text = 'solution to ' + topic
    for word in thesisKeywords:
        query_text = query_text + ' ' + word
    queryKeyword = 'solution'
    print '\nsolution section'
    solution = text_find(query_text, queryKeyword)
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
    for word in solutionKeywords:
        query_text = query_text + ' ' + word
    query_text = query_text + ' on ' + topic
    for word in thesisKeywords:
        query_text = query_text + ' ' + word
    queryKeyword = 'impact'
    print '\nimpact section'
    text_find(query_text, queryKeyword)
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


