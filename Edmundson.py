
# s.split(t) will turn a sentence into a list of words based on separator 't'. (defaults to whitespace)
# Without machine learning, it is unclear how to "tune" the features. Arbitrary values will be used as
# placeholders.

from nltk import word_tokenize
from nltk.corpus import stopwords
#from . import normalize
class Edmundson():

    def __init__(self, article_dict):
        self.article_dict = article_dict  # a dictionary from summ_article.py




    def get_sent_scores(self, settings):  # call the below methods
        scores = []
        for sentence in self.article_dict['BODY']:
            scores.append(self.get_keyword_score(sentence)*(settings['keywords']) + self.get_titleword_score(sentence)*(settings['titlewords']) +
                self.get_sent_len_score(sentence)*(settings['length']) + self.get_cuephrase_score(sentence)*(settings['cuephrase']))  # len used to be 1.5



        return self.normalize(scores)



    def get_keyword_score(self, sentence):
        keywords = self.article_dict['KEYWORDS']
        words = sentence.split()
        score = 0 # the running score
        for word in words:
            if word in keywords:
                score = score + 1


        if len(words) > 0 :
            final_score = (score/len(words))  # the percentage of the sentence that is comprised of keywords
            return final_score


        return 0


    def get_cuephrase_score(self, sentence):
        score = 0
        with open('cuephrases.txt') as Cuephrases:
            bonusphrases = Cuephrases.readlines()
            bonusphrases_stripped = [item.strip() for item in bonusphrases]

            for bonus in bonusphrases_stripped:
                if bonus in sentence:
                    score += 1


        # Calculate score for stigma phrases
        return score



    def get_titleword_score(self, sentence):
        removed = set(stopwords.words('english'))
        TitleWords = set(self.article_dict['TITLE'].split()) - removed # Only thr content words from the title

        words = sentence.split()
        score = 0
        for word in words:
            if word in TitleWords:
                score = score + 1

        return score # the number of title words present in the sentence


   # def get_sent_loc_score(self, sentence):  # PnSq   where the score is determined by the values n,q


    def get_sent_len_score(self, sentence):  # determined by evaluating whether the length is an outlier

        sentences = self.article_dict['BODY']
        sent_lengths = []

        for sentence in sentences:
            words = sentence.split()
            sent_lengths.append(len(words))

        sorted(sent_lengths, key=int) # order them in ascending order
        Q1 = sent_lengths[int(len(sent_lengths)/4)] # The lower quartile
        Q3 = sent_lengths[int((len(sent_lengths) / 4) * 3)] # The upper quartile
        IQR = Q3 - Q1

        if len(sentence) > int(IQR*1.5):   # outlier above
            return 1

        elif len(sentence) < int(IQR*1.5):  # outlier below
            return -1   # we want to heavily penalize short sentences because they may be fragments

        else: return 0

    def normalize(self,data):  # A list of numbers
        i = 0

        for value in data:
            if value < 0:
                data[i] = -((data[i] - min(data)) / (max(data) - min(data)))
                i += 1
            else:
                data[i] = (data[i] - min(data)) / (max(data) - min(data))
                i += 1


        return data



