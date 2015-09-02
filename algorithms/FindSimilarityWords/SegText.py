__author__ = 'Luigi'

import mmap
import nltk.stem as lem

class SegText:

    def __init__(self,Text):
        self.symbols = ['!', "+", '=', '?', '/', '\\', '#', '%', '&', '*', ';', ':','.',',']
        self.wordlist=[]
        self.createList(Text)

    def createList(self,Text):

        f = open('StopWords')
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        for word in Text.split(' '):

            wnl = lem.WordNetLemmatizer()
            word = wnl.lemmatize(word)

            for x in self.symbols:
                if x in word:
                    word = word.replace(x,'')

            by = str.encode(word)

            if not s.find(by):
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


