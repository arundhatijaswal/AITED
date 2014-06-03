from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from google import search
import json as m_json
import requests, string, re
import urllib2
import urllib
import HTMLParser
import thesis2
from alchemyapi import AlchemyAPI


def gen_quotes(category, title):
    #print "%s %s %s" % ("=" * 30, "quotes", "=" * 30)
    keyword = ""

    '''delete punctuation in title'''
    exclude = set(string.punctuation)
    title = ''.join(ch for ch in title if ch not in exclude)
    # print "%s %s %s" % ("="*30, "title without punctuation", "="*30)
    # print title

    '''generate the list of keywords from title'''
    keywords = alchemy_keywords(title)
    if len(keywords) <= 1:
        #print "keywords not good from alchemyapi"
        keywords = [word for word in title.lower().split() if word not in stopwords.words('english')]
    elif len(keywords) > 3:
        keywords = keywords[:2]
        #print "shorten the keywords: " + keywords

    web_url = ""
    while web_url == "":
        keywords_str = ' '.join(keywords)
        query1 = category + " " + keywords_str + " site:brainyquote.com"
        query2 = urllib.urlencode({'q': query1})
        response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query2).read()
        json = m_json.loads(response)
        '''in case we hit the limit of searching'''
        try:
            results = json['responseData']['results']
            '''too many keywords for finding a good result'''
            try:
                #print "Query tried: ", query1
                web_url = results[0]["url"]
                #print web_url
                contents = results[0]['content'].split("...")
                contents = filter(None, contents)
                h = HTMLParser.HTMLParser()
                if len(contents) == 1:
                    index = 0
                else:
                    index = 1
                target_content = h.unescape(contents[index])
                target_content = BeautifulSoup(target_content).text
                target_content = " ".join(target_content.split())
            except Exception:
                #print "-----broke"
                del keywords[-1]
                '''lower the quality of target_content in except'''
                target_content = category
        except Exception:
            #print "query no result: " + query1
            result_urls = search(query1, num=10, pause=1.0)
            urls_list = [link for (num, link) in list(enumerate(result_urls))]
            web_url = urls_list[0]
            #print web_url
            target_content = category

    #print "target_content:" + target_content

    '''start to fetch quotes from the right link'''
    success, quote, author = get_quote(web_url, target_content)

    '''if can't find one quote with target_content which happens in two cases: 1. the quote is in a later page. 2. the target_content is not right'''
    if success == -1:
        #first case: do another search with target_content
        requery = target_content + " site:brainyquote.com"
        #print "requery: " + requery
        #print "target_content: " + target_content
        quotes_urls = search(requery, num=20, pause=2.0)
        urls_list = [link for (num, link) in list(enumerate(quotes_urls))]
        quote_url = urls_list[0]
        success, quote, author = get_quote(quote_url, target_content)
        #second case: pick the first quote

    return quote, author


def alchemy_keywords(title):
    response = AlchemyAPI().keywords('text', title.encode('utf8'))
    keywords = []  # roots of categories
    # categorize the paragraph
    if response['status'] == 'OK':
        for keyword in response['keywords']:
            #print keyword
            label, score = keyword['text'], keyword['relevance'][:4]
            keywords.append(str(label))
    else: pass
        #print 'Error in concept tagging call: ', response['statusInfo']
    # roots = list(set(roots)) # remove duplicates
    #print 'Keywords: ', keywords
    return keywords


def get_quote(web_url, target_content):
    success = 1
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    # try:
    req = urllib2.Request(web_url, headers=hdr)
    response = urllib2.urlopen(req)
    line = response.readline()
    data = ''

    while len(line) != 0:
        data = data + line
        line = response.readline()

    soup = BeautifulSoup(data)
    quotes_in_link = soup.find_all("div", {"class": "masonryitem"})
    # print len(quotes_in_link)
    quote = ""
    author = ""
    for q in quotes_in_link:
        if target_content in q.text:
            quote = q.find("span", {"class": "bqQuoteLink"}).text
            author = q.find("div", {"class": "bq-aut"}).text
            break
    if quote == "":
        #print "fall to bad mode"
        sucess = -1
        quote = quotes_in_link[0].find("span", {"class": "bqQuoteLink"}).text
        author = author = quotes_in_link[0].find("div", {"class": "bq-aut"}).text
    return success, quote, author

def main():
    category = 'education'
    title, link, category = thesis2.genTopic(category)
    print "%s %s %s" % ("=" * 30, "title", "=" * 30)
    print title
    print "%s %s %s" % ("=" * 30, "quote", "=" * 30)
    # print "title: ", title
    quote, author = gen_quotes(category, title)
    print '"' + quote + '"'
    print " - " + author



