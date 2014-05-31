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


class Thesis:
    def __init__(self, topic, source=True):   
        title, main_point, support, url = thesis2.genThesis(topic)
        self.title = title
        self.url = url[:-15] if source else url
        self.thesis = thesis2.introduction(title, main_point, support)
        self.keywords = self.extract_keywords(title) # keywords from title        
        return

    def extract_keywords(self, s):
        keywords = ' '.join([word for word in s.lower().split() if word not in stopwords.words('english')])
        return keywords

    def __repr__(self):
        s = "%s Thesis Class %s" % ("="*30, "="*30)
        attr = ['Title', 'Thesis', 'Keywords', 'Thesis URL']
        attr_str = ''.join(['\n'+x+':\n%s\n' for x in attr])
        s += attr_str % (self.title, self.thesis, self.keywords, self.url)
        return s

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

    def get_html(self, url, debug=False):
        wt = choice(range(self.wait[0], self.wait[1]))
        sleep(wt) # be polite!
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',}
        req = urllib2.Request(url, headers=hdr)
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
            print "%s Poor Results %s" % ("="*30, "="*30)
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
        tags = self.find_tags(html, 'h3', 'r')
        urls = self.google_urls(tags)
        if not urls: return None
        return urls

    def __repr__(self):
        s = "\n%s Scrapper Class %s\n" % ("="*30, "="*30)
        s += "Section keywords: %s\n\n" % " ".join(self.section_keywords)
        s += "Query:\n%s\n\n" % self.query
        if self.debug:
            enumerated_urls = [(num, str(url)) for (num, url) in enumerate(self.urls)]
            s += "URL list:\n%s\n\n" % "\n".join(['#%d: %s'%(num, url) for (num, url) in enumerated_urls])
            s += "Broken URLs:\n%s\n\n" % "\n".join(self.broken_urls)
        return s
        

class TextFinder:
    def __init__(self, scraper, keywords_match = 2, taxonomy=0, random_pick=True, debug=True):
        self.scraper = scraper
        self.random_pick = random_pick # urls picked randomly or in order
        self.taxonomy = taxonomy
        self.urls_tried = []
        self.keywords_match = keywords_match
        self.debug = debug
        if taxonomy!=0: self.thesis_taxonomy = self.taxonomy(scraper.thesis_obj.thesis)
        
    def filter_para(self, para):
        if sum([word in para for word in self.scraper.section_keywords]) >= self.keywords_match \
           and 300<len(para)<900:
            if self.debug: print "\nCommon words: ", [word for word in self.scraper.section_keywords if word in para]
            if self.taxonomy==0: return para
            section_taxonomy = self.taxonomy(para)
            common_taxonomy = sum([category in section_taxonomy for category in self.thesis_taxonomy])
            if common_taxonomy >= self.taxonomy: return True
        return False

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
            
            html = scraper.timeout(scraper.get_html, scraper.wait[1]+2, url, self.debug)
            if not html: continue
            paras = scraper.find_tags(html, 'p')

            # filter para
            for para in paras:
                para = para.text.encode('utf-8')
                if self.filter_para(para):
                    self.text = para
                    return para
        return None

    def __repr__(self):
        s = "\n%s TextFind Class %s\n" % ("="*30, "="*30)
        enumerated_urls_tried = [(num, str(url)) for (num, url) in enumerate(self.urls_tried)]
        enumerated_urls_broken = [(num, str(url)) for (num, url) in enumerate(self.scraper.urls_broken)]
        s += "Text found: \n%s\n\n" % self.text
        s += "Random_pick: %s\n\n" % self.random_pick
        s += "Taxonomy: %s\n\n" % self.taxonomy
        s += "URLs Tried:\n%s\n\n" % "\n".join(['#%d: %s'%(num, url) for (num, url) in enumerated_urls_tried])
        s += "URLs Broken:\n%s\n\n" % "\n".join(['#%d: %s'%(num, url) for (num, url) in enumerated_urls_broken])
        return s

def main():
    my_thesis = Thesis('education')
    print my_thesis
                                                    
    section = Scraper(my_thesis, my_thesis.keywords.split(), debug=False)
    if not section.run(): return main()
    print section

    text_find = TextFinder(section, debug=True)
    text_find.run()
    print text_find
    return text_find

if __name__ == "__main__": main()
