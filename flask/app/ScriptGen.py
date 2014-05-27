import urllib2, thesis2
from google import search
from bs4 import BeautifulSoup
from random import choice

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from alchemyapi import AlchemyAPI
#import debate_content

"""
alchemyapi = AlchemyAPI()

Tresponse = alchemyapi.taxonomy('text', my_thesis)
if Tresponse['status'] == 'OK':
    for category in Tresponse['taxonomy']:
        print category['label'], ' : ', category['score']
        if category.has_key('confident'):
            print 'confident: ', category['confident']
else:
    print('Error in concept tagging call: ', response['statusInfo'])


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
"""

def extract_keywords(string):
    keywords = ' '.join([word for word in string.lower().split() if word not in stopwords.words('english')])
    return keywords


def filter_para(para, query_keyword, title_keywords):
    if query_keyword in para and \
       300<len(para)<900:
       #any(word in para for word in title_keywords.split()):
        return para
    return None


def gen_thesis(topic):    
    title, main_point, support = thesis2.genThesis(topic)
    while not bool( title and main_point and support): # check if either is empty
        title, main_point, support = thesis2.genThesis(topic)
        
    my_thesis = thesis2.introduction(title, main_point, support)
    title_keywords = extract_keywords(title)
    return title, my_thesis, title_keywords


def make_section(section_name, topic, title_keywords):
    print "%s %s %s" % ("="*30, section_name, "="*30) 
    query_text = "%s %s %s" % (section_name, topic, title_keywords)
    query_keyword = PorterStemmer().stem(section_name)
    print "Query: %s \n " % query_text

    # get urls and relevent para
    urls_list = text_urls(query_text, query_keyword)
    para = text_find(urls_list, query_keyword, title_keywords)
    para = para.replace('\n',' ').replace('\r',' ').replace('  ','') # clean para
    print "\n %s \n " % para

    
def text_urls(query_text, query_keyword):
    # get urls from query
    result_urls = search(query_text, stop=30, pause=1.0)
    urls_list = [link for (num, link) in list(enumerate(result_urls))]
                 
    # filter urls by type of link
    filters = ['.pdf', '.doc', 'debate.org']
    urls_list = [url for url in urls_list if not any(word in url for word in filters)]
    return urls_list


def text_find(urls_list, query_keyword, title_keywords):
    if not urls_list: return None

    # try a random url
    while True:
        try:
            url = choice(urls_list)
            html = urllib2.urlopen(url).read()
            break
        except:
            print "URL broke: %s" % url
            urls_list.remove(url)
    print "URL tried: %s" % url

    myThesis = thesis2.introduction(myTitle, myOne, mySupport)
    
    
    # keywords = 'coding'
    # myDebate = debate_content.getDebate(topic, keywords, debug=True)
    # myTitle = myDebate.getArgument(0).title + ". " + myDebate.getArgument(0).quote
    # myThesis = debate_content.importance(myDebate)
    
    print "\nTitle: ", myTitle
    print "\nThesis: "
    print "================================================="
    print myThesis

    thesisKeywords = extract_keywords(myTitle)
    section.append(myTitle)
    section.append(myThesis)

    tax = []

    Tresponse = alchemyapi.taxonomy('text',myThesis)
    if Tresponse['status'] == 'OK':
        for category in Tresponse['taxonomy']:
            print category['label'], ' : ', category['score']
            tax.append(category['label'])
            if category.has_key('confident'):
                print 'confident: ', category['confident']
    else:
        print('Error in concept tagging call: ', response['statusInfo'])

    section.append(tax[0])
    print "\nTaxonomy: "
    print "================================================="
    print tax[0]

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

    # get all paragraphs
    soup = BeautifulSoup(html)
    tags = soup.findAll('p')


    # filter para by matching keyword and length
    for para in tags:
        if filter_para(para.text, query_keyword, title_keywords): return para.text
               
    # if no matching para found, remove link and try again 
    urls_list.remove(url)
    return text_find(urls_list, query_keyword, title_keywords)



def main():
    topic = 'education'
    # form thesis and query
    title, my_thesis, title_keywords = gen_thesis(topic)
    print "Title: %s \n " % title
    print "Thesis: %s \n " % my_thesis

    # print sections
    make_section('importance', topic, title_keywords)
    make_section('problem', topic, title_keywords)
    make_section('solution', topic, title_keywords)
    make_section('impact', topic, title_keywords)

if __name__ == "__main__":
    main()
