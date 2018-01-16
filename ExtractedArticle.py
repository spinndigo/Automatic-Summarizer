# This file will take the output of html_parse as input.
# It will generate the tokenized, chunked version of the text we wish to summarize
# Please refer to http://www.nltk.org/book/ch07.html for more info

#grammer = "NP: {<DT>?<JJ>*<NN>}" \
#                 "VP: {<VB.*><NP|PP|CLAUSE>+$}" \
#                "CLAUSE: {<NP><VP>}" \
#               "PP: {<IN><NP}" \
#              "BONUS: {<NNP|NNPS><VP><PP*><VB*><NP*>}" \
#             "BONUS2: {<DT>?<JJ>*<NNP|NNPS>}"

# 10/23/17 not yet working

import nltk
import re
import pprint

class ExtractedArticle():  # this is a super object of Article. It is essentially article with more things

    def __init__(self, article):
        self.article = article  # an article object from the article class. Contains metadata about article a dictionary
        self.bare_sents = self.set_bare_sents()   # the bare sentences in a list of strings. Printable and readable by humans
        self.tokenized_sents = self.set_tokenized_sents() # list of lists of strings. All the sentences separated.
        self.tagged_sents =  self.set_tagged_sents() # list of list of tuples   [[(), (), ()], [(), (), ()], [(), ()]]


    def set_bare_sents(self):  # intended to be private
        return self.article['BODY']                       #(self.article['BODY'])  # pass in the doc_name


    def set_tokenized_sents(self): # intended to be private
        return [nltk.word_tokenize(sent) for sent in self.bare_sents]  # pass in bare sentences


    def set_tagged_sents(self): # intended to be private
        return [nltk.pos_tag(sent) for sent in self.tokenized_sents] # pass in tokenized sentences


    def draw_chunked_sents(self): # must call above three beforehand

         noun_phrase_grammar = "NP: {<DT>?<JJ>*<NN>}"
         cp = nltk.RegexpParser(noun_phrase_grammar)

         for sentence in self.tagged_sents:
            result = cp.parse(sentence)
            #print(result)
            result.draw()
            print('\n\n')

    def get_bare_sents(self):
        print(self.bare_sents)

    def get_tokenized_sents(self):
        print(self.tokenized_sents)

    def get_tagged_sents(self):
        print(self.tagged_sents)



    def num_matches(self,tree,label):  #takes a tree and a string
        total = 0
        for subtree in tree.subtrees():
            if subtree.label() == label:
                total += 1

        return total


    def get_Pronoun_Action_scores(self):    # return a list of subscores:   [double , double , double, etc]
        clause_scores = []

        grammar = r"""
          NP: {<DT>?<JJ>*<NN>}          # Chunk sequences of DT, JJ, NN
          PP: {<IN><NP>}               # Chunk prepositions followed by NP
          VP: {<VB|VBZ>+<PP|NP>*/$} # Chunk verbs and their arguments
          CLAUSE: {<NNP|NNPS>+<VP>}           # Chunk NP, VP
          
          """
        parser = nltk.RegexpParser(grammar)


        for sentence in self.tagged_sents:
            chunked = parser.parse(sentence)
           # chunked.draw()
           # print(chunked)
            clause_scores.append(self.num_matches(chunked, "CLAUSE")) # an int?



        return clause_scores

    def get_CoordinatingConjunctionPhrase_scores(self):  # return a list of subscores:   [double , double , double, etc]
        pronoun_scores = []

        grammar = r"""

             CLAUSE: {<CC>}           
             """
        parser = nltk.RegexpParser(grammar)

        for sentence in self.tagged_sents:
            chunked = parser.parse(sentence)
            # chunked.draw()
            # print(chunked)
            pronoun_scores.append(self.num_matches(chunked, "CLAUSE"))  # an int?

        return pronoun_scores



    def get_Article_scores(self):    # return a list of subscores:   [double , double , double, etc]
        pronoun_scores = []

        grammar = r"""
          CLAUSE: {<DT>}           
          """
        parser = nltk.RegexpParser(grammar)


        for sentence in self.tagged_sents:
            chunked = parser.parse(sentence)
           # chunked.draw()
           # print(chunked)
            pronoun_scores.append(self.num_matches(chunked, "CLAUSE")) # an int?

        return pronoun_scores



    def get_PrepositionalPhrase_scores(self):    # return a list of subscores:   [double , double , double, etc]
        pronoun_scores = []

        grammar = r"""
          NP: {<DT>?<JJ>*<NN>} 
          PP: {<IN><NP>} 
          CLAUSE: {<PP>}           
          """
        parser = nltk.RegexpParser(grammar)


        for sentence in self.tagged_sents:
            chunked = parser.parse(sentence)
           # chunked.draw()
           # print(chunked)
            pronoun_scores.append(self.num_matches(chunked, "CLAUSE")) # an int?

        return pronoun_scores




    def get_sent_scores(self, settings): # master method
        scores = [(subscore1*settings['pronounphrase']) + (subscore2*settings['articles']) + (subscore3*settings['prepositionalphrase'] )
                  + (subscore4*settings['conjunctionphrase']) for subscore1, subscore2, subscore3, subscore4
                  in zip(self.get_Pronoun_Action_scores(), self.get_Article_scores(), self.get_PrepositionalPhrase_scores(),
                         self.get_CoordinatingConjunctionPhrase_scores())]

        return self.normalize(scores)



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
