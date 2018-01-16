# Parse HTML
# try this: https://www.nytimes.com/2017/09/04/us/hurricane-irma.html?rref=collection%2Fsectioncollection%2Fus&action=click&contentCollection=us&region=rank&module=package&version=highlights&contentPlacement=5&pgtype=sectionfront
# try this: http://money.cnn.com/2017/09/04/technology/culture/elon-musk-ai-world-war/index.html
# http://www.foxnews.com/entertainment/2017/09/10/it-shatters-weekend-box-office-records-despite-threats-from-hurricane-irma.html
# http://www.cnn.com/2017/10/02/opinions/america-lethal-nation-opinion-bergen/index.html

# This file should be renamed Article.py !!

import sys
from newspaper import Article
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.tokenize.punkt import PunktSentenceTokenizer
#  ''.join(list)  <-- will turn a list into a string

class Summ_Article():

    def __init__(self, url):
        self.url = url  # pass url as cmd line argument
        self.article = {}



    def create_file(self):
        new_article = self.create_article()
        separator = '-------------------------------------------------------------'
        pretty_article = open(new_article['FILE'], 'w')
        pretty_article.write('\nTITLE: ' + new_article['TITLE'] + '\n' + 'BY: ' +
                             ', '.join(new_article['AUTHORS']) + '\n\n' + 'BODY: \n' + '\n'.join(new_article['BODY'])
                             + '\n\n' + 'ENDBODY' + '\n\n'
                             + separator + '\n\n' + 'KEYWORDS: ' + ', '.join(new_article['KEYWORDS']) + '\n' +
                             '# OF SENTENCES: '  + str(new_article['LENGTH']) + '\n' + 'SOURCE: ' + new_article['URL'])

        pretty_article.close()



    def article_sentences(self, article_text):  # take in article.text

        document = ' '.join(article_text.strip().split('\n'))
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.tokenize(document)

        return sentences




       # candidates = re.split(r'[A-Z][^\.!?\n]*[\.!?]+', article_text)  # capture the delim so we save it  re.split('(. ? !)', article_text)
        #bonafide_sentence = re.compile(r'[A-Z][^\.!?\n]*[\.!?]+')
        #return bonafide_sentence.findall(str(candidates))




    def create_article(self):

        article_dictionary = {}  # the returned value

        try:
            article = Article(self.url)
            self.article = article


        except:
            print("Please enter a url to a news article!")
            return # leave the method if errant

        article.download()
        article.parse()
        article.nlp()
        article.html

        article_dictionary['LENGTH'] =  len(article.text.split("."))  # int DOES NOT WORK
        article_dictionary['KEYWORDS'] = article.keywords  # list of strings
        article_dictionary['BODY'] = self.article_sentences(article.text)  #article.text.split(".")
        article_dictionary['AUTHORS'] = article.authors   # list of strings
        article_dictionary['TITLE'] = article.title       # string ?
        article_dictionary['FILE'] = article_dictionary['TITLE'][:4] + '.txt'  # used to be article_dictionary['TITLE'][:4] + '.txt'
        article_dictionary['URL'] = self.url

        return article_dictionary
