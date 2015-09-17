__author__ = 'Luigi'

import os
import nltk.stem as lem

#Class for parsing a content of website
class SegText:

    def __init__(self,Text):
        self.symbols = ['!', "+", '=', '?', '/', '\\', '#', '%', '&', '*', ';', ':','.',',']
        self.wordlist=[]
        self.createList(Text)

    def createList(self,Text):

        f = open(os.path.dirname(os.path.realpath(__file__))+'/StopWords',"r")
        stopwords = f.readlines()

        for word in Text.split(' '):

            word = word.lower()

            wnl = lem.WordNetLemmatizer()
            #lemmatization
            word = wnl.lemmatize(word)

            for x in self.symbols:
                if x in word:
                    word = word.replace(x,'')

            by = str.encode(word)

            #removing stopwords
            if by in stopwords:
                continue

            try:
                a =float(word)
                #print (a)
                continue
            except ValueError:
                True

            if word not in self.wordlist:
                self.wordlist.append(word)


def main():


     with open('Text') as f:
         text = f.readline()

     st = SegText(text)
     print(st.wordlist)



if __name__ == '__main__':

    main()


