import urllib2, thesis2
from google import search
from bs4 import BeautifulSoup
from random import choice

import signal
from contextlib import contextmanager

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from alchemyapi import AlchemyAPI
#import debate_content


class TimeoutException(Exception): pass
def timeout(fun, limit, *args ):
    @contextmanager
    def time_limit(seconds):
        def signal_handler(signum, frame):
            raise TimeoutException, "Timed out!"
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
    try:
        with time_limit(limit):
            return fun(*args)
    except TimeoutException, msg:
        return None


def para_taxonomy(para):
    print
    response = AlchemyAPI().taxonomy('text', para.encode('utf8'))
    roots = [] # roots of categories
    # categorize the paragraph
    if response['status'] == 'OK':
        for category in response['taxonomy']:
            label, score = category['label'], category['score'][:4]
            root_label = label.split('/')[1]
            roots.append(str(root_label))
            #print "Root: %s \t Score: %s" % (label.ljust(40), score)
    else: print 'Error in concept tagging call: ', response['statusInfo']
    roots = list(set(roots)) # remove duplicates
    print 'Category roots', roots
    return roots


def extract_keywords(string):
    keywords = ' '.join([word for word in string.lower().split() if word not in stopwords.words('english')])
    return keywords


def filter_para(para, query_keyword, title_keywords, thesis_taxonomy):
    if query_keyword in para and 300<len(para)<900:
        section_taxonomy = para_taxonomy(para)
        common_taxonomy = sum([category in section_taxonomy for category in thesis_taxonomy])
        if common_taxonomy >0: return para
    return None


def gen_thesis(topic):    
    title, main_point, support = thesis2.genThesis(topic)
    while not bool( title and main_point and support): # check if either is empty
        title, main_point, support = thesis2.genThesis(topic)
        
    my_thesis = thesis2.introduction(title, main_point, support)
    title_keywords = extract_keywords(title)
    return title, my_thesis, title_keywords


def make_section(section_name, topic, title_keywords, thesis_taxonomy):
    print "%s %s %s" % ("="*30, section_name, "="*30) 
    query_text = "%s %s %s" % (section_name, topic, title_keywords)
    query_keyword = PorterStemmer().stem(section_name)
    print "Query: %s \n " % query_text

    # get urls and relevent para
    urls_list = text_urls(query_text, query_keyword)
    para = text_find(urls_list, query_keyword, title_keywords, thesis_taxonomy)
    para = para.replace('\n',' ').replace('\r',' ').replace('  ','') # clean para
    print "\n%s \n " % para

    
def text_urls(query_text, query_keyword):
    # get urls from query
    result_urls = search(query_text, stop=30, pause=1.0)
    urls_list = [link for (num, link) in list(enumerate(result_urls))]
                 
    # filter urls by type of link
    filters = ['.pdf', '.doc', 'debate.org']
    urls_list = [url for url in urls_list if not any(word in url for word in filters)]
    return urls_list


def get_paras(url):
    # get all paras from a url
    try:
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        tags = soup.findAll('p')
        print "URL tried: %s" % url
        return tags       
    except:
        print "URL broke: %s" % url
        return None

   
def text_find(urls_list, query_keyword, title_keywords, thesis_taxonomy):
    if not urls_list: return 'Nothing found'

    # try a random url
    url = choice(urls_list)
    urls_list.remove(url)
    tags = timeout(get_paras, 2, url) # try another url if timed out
    if not tags: return text_find(urls_list, query_keyword, title_keywords, thesis_taxonomy)
    
    # filter para by matching keyword and length
    for para in tags:
        if filter_para(para.text, query_keyword, title_keywords, thesis_taxonomy): return para.text.encode('utf8')
               
    # if no matching para found, try again 
    return text_find(urls_list, query_keyword, title_keywords, thesis_taxonomy)



def main():
    topic = 'education'
    # form thesis and query
    title, my_thesis, title_keywords = gen_thesis(topic)
    print "\nTitle: %s \n " % title
    print "Thesis: \n%s \n " % my_thesis

    # thesis taxonomy
    thesis_taxonomy = para_taxonomy(my_thesis)
    
    # print sections
    #"""
    make_section('importance', topic, title_keywords, thesis_taxonomy)
    make_section('problem', topic, title_keywords, thesis_taxonomy)
    make_section('solution', topic, title_keywords, thesis_taxonomy)
    make_section('impact', topic, title_keywords, thesis_taxonomy)
    #"""

if __name__ == "__main__":
    main()
