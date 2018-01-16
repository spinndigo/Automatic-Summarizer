# This file contains functions that will be used for textrank algorithm
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
from nltk.corpus import brown

# Currently only takes into account how many non stopwords two sentences share
class TextRank():


    def __init__(self, sentences):
        self.sentences = sentences


    def sentence_similiarity(self,sentence1, sentence2):  # String, String  private

        Stop = set(stopwords.words('english'))
        s1 = [ word.lower() for word in sentence1]  # list of words    for word in sentence1.strip()
        s2 = [ word.lower() for word in sentence2]  # list of words    for word in sentence1.strip()


        all_words = list(set(s1 + s2)) # Every word in both sentences once

        s1_vector = [0] * len(all_words) # [0 , 0 , 0 , 0 , ... ]
        s2_vector = [0] * len(all_words)  # [0 , 0 , 0 , 0 , ... ]

        for word in s1:
            if word in Stop:
                continue # ignore

            s1_vector[all_words.index(word)] += 1

        for word in s2:
            if word in Stop:
                continue # ignore

            s2_vector[all_words.index(word)] += 1


        return 1 - cosine_distance(s1_vector, s2_vector) # similiarity measure


# Constructs a "transition matrix" which the pagerank algorithm will use
# Right now all it looks for words that sentences share
    def similiarity_matrix(self): # private

         #   print("Entered SIM matrix")
            Matrix = np.zeros((len(self.sentences), len(self.sentences))) #  Matrix = np.zeros((len(self.sentences), len(self.sentences)))


            for index1 in range(len(self.sentences)):
                for index2 in range(len(self.sentences)):
                    if index1 == index2:
                        Matrix[index1][index2] = 1 # same sentence; main diagonal
                        continue


                    Matrix[index1][index2] = self.sentence_similiarity((self.sentences[index1].split()), (self.sentences[index2].split())) # passing ints?

            for row in range(len(Matrix)):   # Normalize each row
          #      print("row:")
           #     print(Matrix[row])
                Matrix[row] = Matrix[row] / Matrix[row].sum()


            return Matrix


    def page_rank(self, Matrix , epsilon , damping_factor):  # private
        #print("Entered PAGE rANK")
        Probability = np.ones(len(Matrix)) / len(Matrix)
        #print (Probability)
        while True:
            new_Prob = (np.ones(len(Matrix)) * (((1-damping_factor) / (len(Matrix))))) + (damping_factor * (Matrix.T.dot(Probability)))
         #   print(new_Prob)
            delta = abs((new_Prob - Probability).sum())
         #   print(delta)
            if delta <= epsilon:
                return new_Prob
            Probability = new_Prob


    def get_sent_scores(self):

        Matrix = self.similiarity_matrix()
       # print(Matrix)


        return self.page_rank(Matrix, 0.0001 , .85)
