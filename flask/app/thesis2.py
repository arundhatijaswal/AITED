import urllib
from pprint import pprint
import json as m_json
import requests, random, re, string, os
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk.data
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


# Global variables
issues = {}
results = []
stemmer = WordNetLemmatizer()


def genTopic(category):
    """ web scraper that returns the title and url from
    debate.org. This will form the thesis of our script """

    """ first, take the topic and navigate to the debates.org website """
    # category = raw_input ( '\nEnter Topic: ' )
    websites = ['http://www.debate.org/opinions/' + category + '/?sort=popular',
                'http://www.debate.org/opinions/' + category + '/?p=2&sort=popular']

    web = random.choice(websites)
    r = requests.get(web)
    data = r.text
    soup = BeautifulSoup(data)
    # print soup.prettify()

    results = soup.find_all("p", "l-name")
    for i in range(0, len(results)):

        """ get the titles """
        temp = results[i].find("span", "q-title").text
        tmps = temp.split()

        """ for each title, make sure it's appropriate length and get the url
            then, add title and url to dictionary """
        if len(tmps) > 5 and len(tmps) < 20:
            title = ' '.join(tmps)
            url = 'http://www.debate.org' + results[i].find("a").get('href') + '?nsort=3&ysort=3'
            issues[str(title)] = str(url)

    topic = random.choice(issues.keys())
    link = issues[topic]
    return topic, link, category


def dePunc(rawword):
    """ remove punctuation in the input string """
    L = [c for c in rawword if 'A' <= c <= 'Z' or 'a' <= c <= 'z']
    word = ''.join(L)
    return word


def genThesis(topic):
    """
    in order to generate the thesis, we need the following:
        - title
        - url
        - rating = opinion
        - thesis: the bold text for the yes or no section 
            ** the thesis has to contain some keywords from the title
        - support: the sentence following the yes or no bold statement
    """

    title, url, category = genTopic(topic)

    # print '\n'
    # print title
    # print '===================================================== \n'

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    cleaned = []

    """ remove stopwords using nltk stop list and print the keywords """
    # stoppers = stopWords()

    keywords = [w for w in title.lower().split() if not w in stopwords.words("english")]
    # print "keywords: ", keywords
    for i in keywords:
        cleaned.append(dePunc(i))
    # print "cleaned: ", cleaned

    # cleaned list of keywords
    keys = ' '.join(cleaned)

    vote = soup.find("span", "no-text").text
    strings = str(vote).split()
    rating = int(strings[0][:-1])  # this is the 'no' rating
    opinions = []
    args = []
    argSplit = []
    clean_keys = []
    data = {}

    """ for each top argument, check if it is long enough and contains more than one word from
    the list of title keywords. """
    if rating > 50:
        # vote is " No"
        args = soup.find('div', attrs={'id': 'no-arguments'}).find_all("li", "hasData")
        # print args
        for i in range(0, len(args)):
            # find the list items
            temp = args[i].find("h2").text
            userArg = args[i].find("p").text
            # print userArg
            tmps = temp.split()
            # print tmps
            for i in tmps:
                clean_keys.append(dePunc(i))

            if len(clean_keys) > 3:
                count = 0
                for i in clean_keys:
                    for j in cleaned:
                        # print stemmer.lemmatize(i).lower()+','+stemmer.lemmatize(j).lower()
                        if stemmer.lemmatize(i).lower() == stemmer.lemmatize(j).lower():
                            count += 1
                            if count > 1:
                                # opinions.append(' '.join(tmps))
                                # data[str(temp).encode('utf8')] = str(userArg).encode('utf8')

                                data[u''.join(temp).encode('utf-8')] = u''.join(userArg).encode('utf-8') #try to solve ASCII error
                            # print count
    else:
        # vote is " Yes"
        args = soup.find('div', attrs={'id': 'yes-arguments'}).find_all("li", "hasData")
        # print args
        for i in range(0, len(args)):
            # find the list items
            temp = args[i].find("h2").text
            userArg = args[i].find("p").text
            # print userArg
            tmps = temp.split()
            # print tmps
            for i in tmps:
                clean_keys.append(dePunc(i))

            if len(clean_keys) > 3:
                # opinions.append(' '.join(tmps))
                # print opinions
                count = 0
                for i in clean_keys:
                    for j in cleaned:
                        # print stemmer.lemmatize(i).lower()+','+stemmer.lemmatize(j).lower()
                        if stemmer.lemmatize(i).lower() == stemmer.lemmatize(j).lower():
                            count += 1
                            if count > 1:
                                # opinions.append(temp)
                                data[temp.encode('utf8')] = userArg.encode('utf8')
                            # print count

    """ form the thesis by taking a random opinion and it's supporting argument """
    # long_support = userArg

    # print data

    # if not opinions: #checking if opinions is empty
    #   print "Couldn't find anything - opinions"
    #   # return "", ""
    # elif not userArg: #checking if userArgs is empty
    #   print "Couldn't find anything - arguments"
    #   # return "", ""
    # else: #if they aren't empty, do this
    #   # print 'Top Argument: '+opinions[0]+'\n'
    #   # topArg = opinions[0].split()
    #   """ send the thesis and userArgs off to the function to be strengthened """
    #   # thesis = opinions[0]+' '+long_support
    #   thesis_stmt = thesis(arg, long_support)
    #   print "Thesis: "
    #   print thesis
    #   # return title, thesis

    if not data:
        # print "Couldn't find anything - data dictionary"
        return "", "", "", ""
    else:  #if they aren't empty, do this
        # print 'Top Argument: '+opinions[0]+'\n'
        # topArg = opinions[0].split()
        """ send the thesis and userArgs off to the function to be strengthened """
        # thesis = opinions[0]+' '+long_support
        # thesis_stmt = improvements(title, data)
        # print "Thesis: "
        # print thesis
        one = random.choice(data.keys())
        two = data[one]

        if two == "":
            return "", "", "", ""
        else:
            punct = ['!', '?']

            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            tokens = tokenizer.tokenize(two.strip())
            # for token in tokens:
            #     print token, "\n"
            thesis_len = len(tokens)
            support = ' '.join(tokenizer.tokenize(two.strip()))
            while thesis_len > 5:
                one = random.choice(data.keys())
                two = data[one]
                tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                thesis_len = len(tokenizer.tokenize(two.strip()))
                support = ' '.join(tokenizer.tokenize(two.strip()))
            # print "support: ", support
            if tokens[0] == one:
                one = ""

            if one[-1] == '.':
                one = one
            elif one[-1] in punct or one[-1] not in punct:
                one = one + '.'
            # print one

            thesis = one + " " + support
            # print title
            # print 'Thesis: ', thesis
            return title, one, support, url


def introduction(title, one, support):

    thesis = ""
    exclude = set(string.punctuation)
    # print "title: " + title
    # try:
    if title[-1] in exclude:
         title = title[0:-1]
    if one != "" and one[0] != "I":
        one = one[0].lower() + one[1:] #lower the first character
        thesis = one + " " + support
    elif one == "" or one == support[0:len(one)]:
        support = support[0].lower() + support[1:]
        thesis = support
    else:
        thesis = one + " " + support
    # except: pass
    temp1 = "When asked " + title[0].lower() + title[1:] + ", the short answer is " + thesis
    temp2 = "If asked " + title[0].lower() + title[1:] + ", I would say " + thesis
    temp3 = "When we think " + title[0].lower() + title[1:] + ", some of us will say " + thesis
    temps = [temp1, temp2, temp3]
    intro = random.choice(temps)
    return intro


def main():
    topic = raw_input("Enter topic: ")
    title, one, support, url = genThesis(topic)
    # print "%s %s %s" % ("="*30, "title", "="*30)
    # print title
    #
    # print "%s %s %s" % ("="*30, "one", "="*30)
    # print one
    #
    # print "%s %s %s" % ("="*30, "support", "="*30)
    # print support
    #
    print "%s %s %s" % ("="*30, "intro", "="*30)
    print introduction(title, one, support)

if __name__ == "__main__":
    main()
