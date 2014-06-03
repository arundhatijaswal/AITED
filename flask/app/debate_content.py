import urllib2
import re
from bs4 import BeautifulSoup
from random import choice
from google import search
from os.path import basename

""" ------------------------- Functions ---------------------------"""
def stripTags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', str(data))

def getQuery(topic, keywords, debug):    
    site = "http://www.nytimes.com/roomfordebate/"
    query = "%s %s site:%s" % (topic, keywords, site)
    if debug: print "Query: %s\n" % query
    return query

# Get a random debate url
def getDebateURLRoot(query, debug):
    urls =  search(query, stop=20, pause=0.5)
    debate_url_root = choice(list(enumerate(urls)))[1]
    try:
        while ( "topics" in debate_url_root): # avoid the topics page
            debate_url_root = getDebateURLRoot(query, debug)
        int(debate_url_root.split('/')[-2]) # see if url is debate root
    except:
        # get debate root
        debate_url_root = '/'.join(debate_url_root.split('/')[:-1]) + '/'
    if debug: print"Debate url root: %s\n" % debate_url_root
    return debate_url_root

def getDebateURL(query, debate_url_root, debug):
    html = urllib2.urlopen(debate_url_root).read()
    soup = BeautifulSoup(html)
    try:
        debate_url = "http://www.nytimes.com" + \
                     soup.find("a", { "class" : "nytint-enter-discussion"})['href']
    except:
        debate_url_root = getDebateURLRoot(query, debug)
        debate_url = getDebateURL(query, debate_url_root, debug)
    if debug: print "Debate url: %s\n" % debate_url
    return debate_url

# Get html from debate_url and make a soup
def getSoup(debate_url):
    html = urllib2.urlopen(debate_url).read()
    soup = BeautifulSoup(html)
    return soup

def getDebateTitle(soup):
    parent_tag = soup.find("div", { "class" : "nytint-discussion-overview"} )
    title = stripTags(parent_tag.find('a'))
    overview = stripTags(parent_tag.find('p'))[:-23]
    return '%s. %s \n' % (title, overview)

# Get links to different speakers
def getLinks(soup, debate_url):
    links = [debate_url]
    a_tags = soup.findAll("a", { "class" : "nytint-rfd-headline"} )
    for a_tag in a_tags[2:]:
        links.append("http://www.nytimes.com" + a_tag['href'])
    return links

def getTitle(soup):
    title = stripTags(soup.title)[:-14]
    return title

def getQuote(soup):
    quote = stripTags(soup.blockquote)
    return quote

def getAuthor(soup):
    parent_tag = soup.find("p", { "class" : "nytint-post-leadin"} )
    author = stripTags(parent_tag.find('a'))
    return author

def getAuthorList(soup):
    authors = []
    tags = soup.findAll("p", { "class" : "nytint-bylines"} )
    for tag in tags:
        authors.append(stripTags(tag).strip())
    return authors

def getParasList(soup):
    div_tags = soup.findAll("div", { "class" : "nytint-post" })
    seen = ''
    paras = []
    for p_tag in div_tags[0].findAll('p'):
        p_tag = str(p_tag)
        # filter results
        filters = ['<em>', 'Room for Debate']
        if ( not any(word in p_tag for word in filters) \
             and p_tag not in seen ):
            seen = p_tag # avoid duplicates
            para = stripTags(p_tag)
            if(len(para)): paras.append(para) # check for empty paras
    return paras

""" ------------------------- Debate Class -------------------------"""
class Debate:
    def __init__(self, debate_url):
        soup = getSoup(debate_url)
        self.debateTitle = getDebateTitle(soup)
        self.speakers = []
        self.authorList = getAuthorList(soup)
        self.links = getLinks(soup , debate_url)
        self.numLinks = len(self.links)
        
    def addSpeaker(self, speaker):
        self.speakers.append(speaker)
        
    def getSpeaker(self, num):
        return self.speakers[num]
        
class Speaker:
    def __init__(self, title, author, quote, paras):
        self.title = title
        self.author = author
        self.authorFirstName = ''.join(author.split()[0])
        self.quote = quote if len(quote)>5 else title
        self.paras = paras
        
    def getPara(self, num):
        return self.paras[num]
    
    def getParaLine(self, para_num, line_num):
        para = self.getPara(para_num)
        para_lines = re.compile('[.]\\s').split(para)
        para_lines = [line for line in para_lines if bool(line.strip())] # check for empty lines
        return para_lines[line_num]
    
def getDebate(topic, keywords, debug=False):   
    query = getQuery(topic, keywords, debug)
    debate_url_root = getDebateURLRoot(query, debug)
    debate_url = getDebateURL(query, debate_url_root, debug)
    #debate_url = "http://www.nytimes.com/roomfordebate/2013/10/08/what-federal-spending-are-we-better-off-without/the-sequester-and-the-shutdown-provide-a-lesson-in-nothing"
    debate = Debate(debate_url)
    
    for link in debate.links:
        debate_url = link
        soup = getSoup(debate_url)
        title = getTitle(soup)
        author = getAuthor(soup)
        quote = getQuote(soup)
        paras = getParasList(soup)
        speaker = Speaker( title, author, quote, paras )
        debate.addSpeaker( speaker )
    return debate


""" ---------------------- Script Gen Functions --------------------"""
def importance(debate):
    speaker0 = debate.getSpeaker(0)
    s = "%s %s" % (speaker0.getPara(0), speaker0.quote)
    return s

def problem(debate):
    speaker0 = debate.getSpeaker(0)
    speaker1 = debate.getSpeaker(1)
    s = "The problem is that some people think that %s And this to me is sad. It's sad because %s \n" % \
      (speaker1.quote, speaker0.getParaLine(-1,-1))
    return s

def solution(debate):
    speaker2 = debate.getSpeaker(2)
    s = "I think %s had the right idea. %s said %s So I make the argument that %s \n" % \
        (speaker2.author, speaker2.authorFirstName, speaker2.quote, speaker2.getParaLine(-1,-1))
    return s

def getSpeechSummary(debate, speaker_num):
    speaker = debate.getSpeaker(speaker_num)
    print "-"*60
    print "Speaker %d's Title: %s \n" % (speaker_num, speaker.title)
    print "Quote: %s - %s \n" % (speaker.quote, debate.authorList[speaker_num])
    print "Main argument: %s \n" % speaker.getPara(0)
    print "Concluding statement: %s \n" % speaker.getParaLine(-1, -1)
    #print "Paragraphs:"
    #for para in speaker.paras: print para,'\n'
    print "-"*60

def getSpeakerPara(debate, speaker_num, para_num):
    speaker = debate.getSpeaker(speaker_num)
    para = speaker.getPara(para_num)
    return para


""" ------------------------   main   ----------------------------"""

#topic = 'education'
#keywords = 'school waste time?'
#debate = getDebate(topic, keywords, debug=True)
#print "Debate Title: %s \n" % debate.debateTitle


# -------------------- Usage 1 - Use these functions -----------------
"""
print "Importance: %s \n" % importance(debate)
print "Problem: %s \n" % problem(debate)
print "Solution: %s \n" % solution(debate)
"""


# ------------ Usage 2 - Look at a summary and choose  ---------------
#for speaker in range(debate.numLinks): getSpeechSummary(debate, speaker)



# ------------ Usage 3 - Get any para from any speaker  ---------------
#speaker_num, para_num = 0, 1
#print "Speaker %d, Para %d: %s" % (speaker_num, para_num, getSpeakerPara(debate, speaker_num, para_num))
