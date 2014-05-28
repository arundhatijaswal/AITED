from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from google import search
import json as m_json
import requests,string,re
import urllib2
import urllib
import thesis2
import HTMLParser


def gen_quotes(category, title):
    keyword = ""

    '''delete punctuation in title'''
    exclude = set(string.punctuation)
    title = ''.join(ch for ch in title if ch not in exclude)
    # print "%s %s %s" % ("="*30, "title without punctuation", "="*30)
    # print title

    '''generate the list of keywords from title'''
    keywords = [word for word in title.lower().split() if word not in stopwords.words('english')]

    web_url = ""
    while web_url == "":
        keywords_str = ' '.join(keywords)
        query1 = category + " " + keywords_str + " site:brainyquote.com"
        query2 = urllib.urlencode({'q': query1})
        response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query2).read()
        json = m_json.loads(response)
        try:
            results = json['responseData']['results']
            try:
                print "Query tried: ", query1
                web_url = results[0]["url"]
                print web_url
                contents = results[0]['content'].split("...")
                contents = filter(None, contents)
                h = HTMLParser.HTMLParser()
                target_content = h.unescape(contents[1])
            except Exception:
                print "-----broke"
                del keywords[-1]
        except Exception:
            result_urls = search(query1, num=20, pause=2.0)
            urls_list = [link for (num, link) in list(enumerate(result_urls))]
            web_url = urls_list[0]
            print web_url
            target_content = category


    target_content = BeautifulSoup(target_content).text
    target_content = " ".join(target_content.split())
    print "target_content:" + target_content

    '''start to fetch quotes from the right link'''
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
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
    # except Exception:
    #     data = urllib2.urlopen(web_url).read()

    soup = BeautifulSoup(data)
    quotes_in_link = soup.find_all("div", {"class": "masonryitem"})
    print len(quotes_in_link)
    quote = ""
    author = ""
    for q in quotes_in_link:
        if target_content in q.text:
            quote = q.find("span", { "class": "bqQuoteLink"}).text
            author = q.find("div", {"class": "bq-aut"}).text
            break
    if quote == "":
        quote = quotes_in_link[0].find("span", {"class": "bqQuoteLink"}).text
        author = quotes_in_link[0].find("span", {"class": "bq-aut"}).text
    print "%s %s %s" % ("="*30, "quotes", "="*30)
    return quote, author


def main():

    category = 'education'
    title, link, category = thesis2.genTopic(category)
    print "%s %s %s" % ("="*30, "title", "="*30)
    print title
    print "%s %s %s" % ("="*30, "quote", "="*30)
    # print "title: ", title
    quote, author = gen_quotes(category, title)
    print quote
    print " - " + author

if __name__ == "__main__":
    main()


