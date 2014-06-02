# -*- coding: utf8 -*-
# scraping
import urllib2
from bs4 import BeautifulSoup
from time import sleep

# TED talk
import thesis2, quoteTest

# NLP
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from alchemyapi import AlchemyAPI

# timeout
import signal
from contextlib import contextmanager

# others
from random import choice


"""============================== Thesis Class =========================="""

class Thesis:
    def __init__(self, topic, source=True):   
        title, main_point, support, url = thesis2.genThesis(topic)
        self.title = title
        self.url = url[:-15] if source else url
        self.thesis = thesis2.introduction(title, main_point, support).encode('utf-8')
        self.keywords = self.extract_keywords(title) # keywords from title        
        return

    def extract_keywords(self, s):
        s = s[:-1] if s[-1]=='?' or s[-1]=='.' else s
        keywords = ' '.join([word for word in s.lower().split() if word not in stopwords.words('english')])
        return keywords

    def __repr__(self):
        s = "%s Thesis Class %s" % ("="*25, "="*25)
        attr = ['Title', 'Thesis', 'Keywords', 'Thesis URL']
        attr_str = ''.join(['\n'+x+':\n%s\n' for x in attr])
        s += attr_str % (self.title, self.thesis, self.keywords, self.url)
        return s


"""============================== Scraper Class =========================="""

class Scraper:
    def __init__(self, thesis_obj, section_keywords, wait=(0,2), debug=True):
        self.thesis_obj = thesis_obj
        self.section_keywords = section_keywords
        self.wait = (0,2)
        self.urls_broken = []
        self.debug = debug
        return
    
    def google_query(self, keywords, thesis_obj):
        search = "https://www.google.com/search?q="
        related = "related:%s" % thesis_obj.url
        words = '+OR+'.join(keywords)
        num_pages = '&num=%s' % 30
        self.query = "%s%s+%s%s" % (search, related, words, num_pages)
        return self.query

    def get_html(self, url, debug):
        wt = choice(range(self.wait[0], self.wait[1]))
        sleep(wt) # be polite!
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',}
        req = urllib2.Request(url, headers=hdr)
        html = None
        try:
            html = urllib2.urlopen(req).read()
            if debug: print "URL tried: %s" % url
        except urllib2.HTTPError, e:
            self.urls_broken.append(url)
            print "URL broke: %s" % url
        return html

    def find_tags(self, html, tag_name, class_name=False):
        soup = BeautifulSoup(html)
        if class_name: tags = soup.findAll(tag_name, { "class" : class_name })
        else: tags = soup.findAll(tag_name)
        return tags
        
    def google_urls(self, tags):
        urls = []
        for link in tags:
            urls.append(link.find("a")["href"])

        # check for poor results
        if 'www.procon.org/debate-topics.php' in urls[0]:
            print "%s Poor Results %s" % ("="*25, "="*25)
            return None
        
        # filter urls by type of link
        filters = ['.pdf', '.doc']
        self.urls = [url for url in urls if not any(word in url for word in filters)]
        return self.urls

    class TimeoutException(Exception): pass
    def timeout(self, fun, limit, *args ):
        @contextmanager
        def time_limit(seconds):
            def signal_handler(signum, frame):
                raise self.TimeoutException, "Timed out!"
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(seconds)
            try:
                yield
            finally:
                signal.alarm(0)
        try:
            with time_limit(limit):
                return fun(*args)
        except self.TimeoutException, msg:
            return None

    def run(self):
        query = self.google_query(self.section_keywords, self.thesis_obj)
        html = self.get_html(query, self.debug)
        if not html:
            print "%s%s%s\n" % ("-"*25, "Cannot open html", "-"*25)
            return None
        tags = self.find_tags(html, 'h3', 'r')
        urls = self.google_urls(tags)
        if not urls: return None
        return urls

    def __repr__(self):
        s = "\n%s %s %s\n" % ("="*25, self.section_keywords[0], "="*25)
        s += "Section keywords: %s\n\n" % " ".join(self.section_keywords)
        s += "Query:\n%s\n\n" % self.query
        if self.debug:
            enumerated_urls = [(num, str(url)) for (num, url) in enumerate(self.urls)]
            s += "URL list:\n%s\n\n" % "\n".join(['#%d: %s'%(num, url) for (num, url) in enumerated_urls])
            s += "Broken URLs:\n%s\n\n" % "\n".join(self.urls_broken)
        return s


        
"""============================== TextFind Class =========================="""

class TextFinder:
    def __init__(self, scraper, talk, title_match, section_match, taxonomy=0, random_pick=True, debug=True):
        self.scraper = scraper
        self.random_pick = random_pick # urls picked randomly or in order
        self.taxonomy = taxonomy
        self.urls_tried = []
        self.title_match = title_match
        self.section_match = section_match
        self.talk = talk
        self.debug = debug
        if taxonomy!=0: self.thesis_taxonomy = self.taxonomy(scraper.thesis_obj.thesis)
    
    def filter_common_words(self, para, keywords):
        """ returns True if number of common words in para and keywords >= num """
        return [word for word in keywords if word in para]

    def filter_length(self, para): return 300<len(para)<900
    
    def apply_filters(self, para):
        title_keywords = self.scraper.thesis_obj.keywords.split()
        section_keywords = self.scraper.section_keywords
        self.common_title_keywords = self.filter_common_words(para, title_keywords)
        self.common_section_keywords = self.filter_common_words(para, section_keywords)
        # filters - 1) common words from title, 2) common words from section keywords, 3) length
        if len(self.common_title_keywords) >= self.title_match \
           and len(self.common_section_keywords) >= self.section_match \
           and self.filter_length(para) \
           and para not in self.talk:
            if self.taxonomy==0: return para
            else: return self.filter_common_words(self.taxonomy(para), self.thesis_taxonomy, self.taxonomy)

    def taxonomy(self, para):
        response = AlchemyAPI().taxonomy('text', para)
        roots = [] # roots of categories
        # categorize the paragraph
        if response['status'] == 'OK':
            for category in response['taxonomy']:
                label, score = category['label'], category['score'][:4]
                root_label = label.split('/')[1]
                roots.append(str(root_label))
                if self.debug: print "Root: %s \t Score: %s" % (label.ljust(40), score)
        else: print 'Error in concept tagging call: ', response['statusInfo']
        roots = list(set(roots)) # remove duplicates
        if self.debug: print 'Category roots', roots
        return roots

    def run(self):
        scraper = self.scraper
        while scraper.urls:
            if self.random_pick: url = choice(scraper.urls)
            scraper.urls.remove(url)
            self.urls_tried.append(url)

            html = scraper.get_html(url, self.debug)
            #html = scraper.timeout(scraper.get_html, scraper.wait[1]+2, url, self.debug)
            if not html:
                print "%s%s%s" % ("-"*20, "html timed out", "-"*20)
                continue
            paras = scraper.find_tags(html, 'p')

            # filter para
            for para in paras:
                # clean para
                para = para.text.encode('utf-8')
                para = "%s" % para.replace('\n',' ').replace('\r',' ').replace('   ','')
                if self.apply_filters(para):
                    self.text = para
                    return para
        return "Nothing Found"

    def __repr__(self):
        s = "\n%s TextFind Class %s\n" % ("="*25, "="*25)
        enumerated_urls_tried = [(num, str(url)) for (num, url) in enumerate(self.urls_tried)]
        enumerated_urls_broken = [(num, str(url)) for (num, url) in enumerate(self.scraper.urls_broken)]
        s += "Text found: \n%s\n\n" % self.text
        if self.debug:
            s += "Random_pick: %s\n\n" % self.random_pick
            s += "Taxonomy: %s\n\n" % self.taxonomy
            s += "Common title keywords: %s\n\n" % str(self.common_title_keywords)
            s += "Common section keywords: %s\n\n" % str(self.common_section_keywords)
            s += "URLs Tried:\n%s\n\n" % "\n".join(['#%d: %s'%(num, url) for (num, url) in enumerated_urls_tried])
            s += "URLs Broken:\n%s\n\n" % "\n".join(['#%d: %s'%(num, url) for (num, url) in enumerated_urls_broken])
        return s


"""=========================== Main functions =========================="""

def run(topic, debug):
    # write to file
    f = open('talk.txt', 'w+')
    f.truncate()
    
    # section names to be used for search
    section_names  = [["importance"], ["problem"], ["solution"], ["should"]]

    # generate thesis
    my_thesis = Thesis(topic)
    talk = [my_thesis.title, my_thesis.thesis]
    f.write("%s\n\n%s" % (my_thesis.title, my_thesis.thesis))
    if debug: print my_thesis

    # generate sections
    for section_name in section_names:
        # make a scraper that returns url links
        section = Scraper(my_thesis, section_name, debug=False)
        if not section.run(): return run(topic, debug)
        if debug: print section

        # find the text from the urls with approriate filters
        text_find = TextFinder(section, talk, title_match=2, section_match=0, debug=debug)
        talk.append(text_find.run())
        f.write("\n\n%s" % text_find.text)

        # printing
        if debug: print text_find

    # add quote
    quote, author = quoteTest.gen_quotes(topic, my_thesis.title)
    quote = '"' + quote + '"' + "--" + author
    talk.append(quote)
    f.write("\n\n%s" % quote)

    print "\n\n%s%s%s" % ("="*25, "Final Talk", "="*25)
    for section in talk:
        print "\n%s" % section
    
    f.close()
    return talk


def main(topic): return run(topic, debug=False)

if __name__ == "__main__": main("education")
