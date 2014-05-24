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
import debate_content
from alchemyapi import AlchemyAPI
import nltk.data

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


def taxonomy_check(thesisTaxonomy, section_text):
    section_text = section_text.encode('utf8')
    response = alchemyapi.taxonomy('text',section_text)
    if response['status'] == 'OK':
        for category in response['taxonomy']:
            localCateg = category['label'].split('/')[1]
            print 'section root taxonomy: ', localCateg
            for categ in thesisTaxonomy:
                thesisCateg = categ['label'].split('/')[1]
                if localCateg == thesisCateg:
                    return 1
    else:
        return -1



def text_find(query_text, queryKeyword, thesisTaxonomy):

    urls = search(query_text, stop=20, pause=2.0)

    syns_tmp = wordnet.synsets(queryKeyword)
    syns = [l.name for s in syns_tmp for l in s.lemmas]
    syns_set = Set(syns)
    urls_dict = list(enumerate(urls))
    urls_list = [link for (num, link) in urls_dict]

    section_url = random.choice(urls_list)

    urls_list = [url for url in urls_list if '.pdf' not in url and '.doc' not in url]

    while urls_list:
        print section_url
        r = requests.get(section_url)
        data = r.text
        soup = BeautifulSoup(data)
        for syn in syns_set:
            syn = syn.replace("_", " ")
            syn = stemmer.stem(syn)
            body = soup.findAll('p')
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            for i in body:
                i = i.text
                if syn in i:
                    section_text = i
                    section_len = len(tokenizer.tokenize(i.strip()))
                    if 2 < section_len < 8:
                        related = taxonomy_check(thesisTaxonomy, section_text)
                        if related == 1:
                            print section_text
                            return section_text
                        else:
                            pass
                    else:
                        pass
        if section_url in urls_list: urls_list.remove(section_url)
        section_url = random.choice(urls_list)
    return -1


def gen_thesis(topic):
    """ google search API scraper that returns the
    title of an article based on the selected topic
    and keyword """

    section = []
    
    myTitle, myOne, mySupport = thesis2.genThesis(topic)
    while myTitle == "" or myOne == "" or mySupport == "":
        myTitle, myOne, mySupport = thesis2.genThesis(topic)
    

    myThesis = thesis2.introduction(myTitle, myOne, mySupport)
    
    """
    keywords = 'coding'
    myDebate = debate_content.getDebate(topic, keywords, debug=True)
    myTitle = myDebate.getArgument(0).title + ". " + myDebate.getArgument(0).quote
    myThesis = debate_content.importance(myDebate)
    """
    print "\nTitle: ", myTitle
    print "\nThesis: "
    print "================================================="
    print myThesis

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
    print '\nimportance section:'
    print "================================================="
    importance = text_find(query_text, queryKeyword, Tresponse['taxonomy'])
    if importance == -1:
        importance = "nothing found for importance"
        print "nothing found for importance"
    section.append(importance)

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
    print "================================================="
    bottleneck = text_find(query_text, queryKeyword, Tresponse['taxonomy'])
    if bottleneck == -1:
        bottleneck = 'nothing found for bottlenect'
        print 'nothing found for bottlenect'
    section.append(bottleneck)

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
    print "================================================="
    solution = text_find(query_text, queryKeyword, Tresponse['taxonomy'])
    if solution == -1:
        solution = "nothing found for solution"
        print "nothing found for solution"
    section.append(solution)

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
    print "================================================="
    impact = text_find(query_text, queryKeyword, Tresponse['taxonomy'])
    if impact == -1:
        impact = "nothing found for impact"
        print impact
    section.append(impact)
    
    return section
# to open the document and read the text

# send generated topic to stop words to be cleaned
# filtered_words = [w for w in topic.split() if not w in stopwords.words('english')]
# print filtered_words


def main():
    topic = raw_input("Enter topic: ")
    try:
        gen_thesis(topic)
    except:
        main()
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
