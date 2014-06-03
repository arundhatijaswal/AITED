import urllib2, thesis2, cookielib, urllib
from google import search
from bs4 import BeautifulSoup
from random import choice
from time import sleep

import signal
import quoteTest
from contextlib import contextmanager

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from alchemyapi import AlchemyAPI
import debate_content


def google_results(query):
    query = "https://www.google.com/search?q=" + query + "&num=30"
    print "Query: %s \n " % query
    html = get_HTML(query)
    soup = BeautifulSoup(html)
    links = soup.findAll("h3", { "class" : "r"} )
    urls_list = []
    for link in links:
        urls_list.append(link.find("a")["href"])
    if 'www.procon.org/debate-topics.php' in urls_list[0]:
        print "%s Wrong Debate %s" % ("="*30, "="*30)
        return -1
    return urls_list


def get_HTML(url):
    wt = choice(range(2,5))
    sleep(wt) # Time in seconds.
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',}
    req = urllib2.Request(url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'Could not open HTML'
    return page.read()



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



def gen_thesis(topic):    
    title, main_point, support, talk_url = thesis2.genThesis(topic)
    while not bool( title and main_point and support): # check if either is empty
        title, main_point, support, talk_url = thesis2.genThesis(topic)
        
    my_thesis = thesis2.introduction(title, main_point, support)
    title_keywords = extract_keywords(title)
    return title, my_thesis, title_keywords, talk_url

def gen_thesis_NYT(topic):
    keywords = ''
    myDebate = debate_content.getDebate(topic, keywords, debug=False)
    myTitle = myDebate.getSpeaker(0).title + ". " + myDebate.getSpeaker(0).quote
    myThesis = debate_content.importance(myDebate)
    url = myDebate.links[0]
    return myTitle, myThesis, url
    

def make_section(section_name, topic, title_keywords, thesis_taxonomy):
    print "%s %s %s" % ("="*30, section_name, "="*30) 
    query_text = "%s+%s" % (topic, section_name)
    query_keyword = PorterStemmer().stem(section_name)
    
    # get urls and relevent para
    #urls_list = text_urls(query_text, query_keyword)
    urls_list = google_results(query_text)
    if urls_list == -1: return -1
    para = text_find(urls_list, query_keyword, title_keywords, thesis_taxonomy)
    para = "%s" % para.replace('\n',' ').replace('\r',' ').replace('  ','') # clean para
    print para
    return para

    
def text_urls(query_text, query_keyword):
    # get urls from query
    result_urls = search(query_text, stop=30, pause=2.0)
    urls_list = [link for (num, link) in list(enumerate(result_urls))]
                 
    # filter urls by type of link
    filters = ['.pdf', '.doc']
    urls_list = [url for url in urls_list if not any(word in url for word in filters)]
    return urls_list


def get_paras(url):
    # get all paras from a url
    try:
        html = get_HTML(url)
        soup = BeautifulSoup(html)
        tags = soup.findAll('p')
        print "URL tried: %s" % url
        return tags       
    except:
        print "URL broke: %s" % url
        return None


def filter_para(para, query_keyword, title_keywords, thesis_taxonomy):
    if query_keyword in para and 300<len(para)<900:
        section_taxonomy = para_taxonomy(para)
        common_taxonomy = sum([category in section_taxonomy for category in thesis_taxonomy])
        if common_taxonomy >=0: return para
        #return para
    return None

   
def text_find(urls_list, query_keyword, title_keywords, thesis_taxonomy):
    if not urls_list: return 'Nothing found'

    # try a random url
    url = choice(urls_list)
    #num += 1
    urls_list.remove(url)
    tags = timeout(get_paras, 7, url) # try another url if timed out
    if not tags: return text_find(urls_list, query_keyword, title_keywords, thesis_taxonomy)
    
    # filter para by matching keyword and length
    for para in tags:
        if filter_para(para.text, query_keyword, title_keywords, thesis_taxonomy): return para.text.encode('utf8')
               
    # if no matching para found, try again 
    return text_find(urls_list, query_keyword, title_keywords, thesis_taxonomy)



def main(topic):
    #topic = 'education'
    # topic = raw_input("Enter topic: ")
    category = topic
    # form thesis and query
    category = topic
    title, my_thesis, title_keywords, talk_url = gen_thesis(topic)
    talk_url = talk_url[:-15]
    #title, my_thesis, talk_url = gen_thesis_NYT(topic)

    print "\nTitle: %s \n " % title
    print "Thesis: \n%s \n " % my_thesis

    # add related
    topic = "related:%s" % (talk_url)

    #thesis taxonomy
    #thesis_taxonomy = para_taxonomy(my_thesis)
    thesis_taxonomy = ''
    #title_keywords = ''
    
    # print sections
    talk = [title, my_thesis]
    sections = ['importance', 'problem', 'solution', 'should']
    #"""
    for section in sections:
        para = make_section(section, topic, title_keywords, thesis_taxonomy)
        if para == -1: return main(category)
        talk.append(para)
  
    quote, author = quoteTest.gen_quotes(category, title)
    talk.append('"' + quote + '"' + "--" + author)
    # print '"',quote, '"'
    # print "--", author

    print "%s Final Talk %s" % ("="*30, "="*30)
    for para in talk:
        print "\n%s" % str(para)

    return talk
    


if __name__ == "__main__":
    main('education')
