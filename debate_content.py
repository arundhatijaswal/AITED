import urllib2
import re
from bs4 import BeautifulSoup
from random import choice
from google import search
from os.path import basename

""" ------------------------- Functions ---------------------------"""
# Remove tags
def stripTags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', str(data))

# Get a query using topic and keywords
def getQuery(topic, keywords):    
    site = "http://www.nytimes.com/roomfordebate/"
    query = "%s %s site:%s" % (topic, keywords, site)
    #print "Query: %s\n" % query
    return query

# Get a random debate url
def getDebateURLRoot(query):
    urls =  search(query, stop=20, pause=0.5)
    try:
        debate_url_root = choice(list(enumerate(urls)))[1]
        while ( "topics" in debate_url_root): # avoid the topics page
            getDebateURLRoot(query)
        int(debate_url_root.split('/')[-2]) # see if url is debate root
    except:
        # get debate root
        debate_url_root = '/'.join(debate_url_root.split('/')[:-1]) + '/' 
    #print "Debate url root: %s\n" % debate_url_root
    return debate_url_root

def getDebateURL(query, debate_url_root):
    html = urllib2.urlopen(debate_url_root).read()
    soup = BeautifulSoup(html)
    try:
        debate_url = "http://www.nytimes.com" + \
                     soup.find("a", { "class" : "nytint-enter-discussion"})['href']
    except:
        debate_url_root = getDebateURLRoot(query)
        getDebateURL(query, debate_url_root)
    #print "Debate url: %s\n" % debate_url
    return debate_url

# Get html from debate_url and make a soup
def getSoup(debate_url):
    html = urllib2.urlopen(debate_url).read()
    soup = BeautifulSoup(html)
    return soup

# Print title
def getTitle(soup):
    title = stripTags(soup.title)[:-14]
    #print "Title: %s\n" % title
    return title

# Print quote
def getQuote(soup):
    quote = stripTags(soup.blockquote)
    #print "Quote: %s\n" % quote
    return quote

# Print paragraphs
def getParas(soup):
    div_tags = soup.findAll("div", { "class" : "nytint-post" })
    #print "Paragraphs: \n"
    seen = ''
    paras = []
    for p_tag in div_tags[0].findAll('p'):
        if ( (not '<em>' in str(p_tag)) and (str(p_tag) not in seen) ): # ignore the blockquote in the end
            seen = str(p_tag) # avoid duplicates
            para = stripTags(str(p_tag))
            if (len(para) > 5): paras.append(para)
    return paras

def getLine(para, line_num):
    if len(para) > 5: # check for empty paras
        para_lines = para.replace('.','.<').split('<')[:-1]
        return para_lines[line_num]
    return ''

# Get links to different arguments
def getLinks(soup, debate_url):
    links = [debate_url]
    a_tags = soup.findAll("a", { "class" : "nytint-rfd-headline"} )
    for a_tag in a_tags[2:]:
        links.append("http://www.nytimes.com" + a_tag['href'])
    #print "%d links to different argumens \n" % len(links)
    return links


""" ------------------------- Debate Class -------------------------"""
class debate:
    arguments = []
    def addArgument(self, argument):
        self.arguments.append(argument)
    def getArgument(self, num):
        return self.arguments[num]
        
class argument:
    def __init__(self, title, quote, paras):
        self.title = title
        self.quote = quote
        self.paras = paras
        
    def getPara(self, num):
        return self.paras[num]
    
    def getParaLine(self, paraNum, lineNum):
        return getLine(self.paras[paraNum], lineNum)
    

""" ---------------------- Fill Debate Class ----------------------"""

query = getQuery('technology', '')
debate_url_root = getDebateURLRoot(query)
debate_url = getDebateURL(query, debate_url_root)
soup = getSoup(debate_url)
links = getLinks(soup, debate_url)

myDebate = debate()
for link in links:
    debate_url = link
    soup = getSoup(debate_url)
    title = getTitle(soup)
    quote = getQuote(soup)
    paras = getParas(soup)
    myArg = argument( title, quote, paras )
    myDebate.addArgument( myArg )


""" ---------------------- Script Gen Functions --------------------"""
def importance():
    s = "%s %s \n" % (myDebate.getArgument(0).getPara(0), \
                     myDebate.getArgument(0).quote)
    return s

def problem():
    s = "The problem is that some people think that %s And this to me is sad. It's sad because %s \n" % \
      (myDebate.getArgument(1).quote, \
       myDebate.getArgument(0).getParaLine(-1,-1))
    return s

def solution():
    s = "I think Diane Ravitch had the right idea. He said %s So I make the argument that %s \n" % (myDebate.getArgument(2).quote, \
                     myDebate.getArgument(2).getParaLine(-1,-1))
    if len(links)>5: s += "%s" % myDebate.getArgument(4).getParaLine(-1,-1)
    return s

""" ---------------------- Templates ----------------------"""

print "Title: %s \n" % myDebate.getArgument(0).title

print importance()
print problem()
print solution()




