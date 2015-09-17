__author__ = 'Luigi'

import shelve
from SegText import SegText

#Class for create a Bunch of word from a WebSite's content
class CreateBoWText:

    def __init__(self,path=None):

        if path:
            self.filename = path +'Words_Website'
        else:
            self.filename = 'Words_Website'

        self.db = shelve.open(self.filename)
        self.db.close()


    def addWebsite(self,Website,Text):

        self.db = shelve.open(self.filename)

        sg = SegText(Text)

        for w in sg.wordlist:
              
            if w in self.db.keys():
                l = self.db[w]
                l.add(Website)
                self.db[w] = l
            else:
                self.db[w]={Website}

        self.db.close()


    def getWebsiteFromWord(self,Word):

        self.db = shelve.open(self.filename)

        if Word in self.db.keys():
            ret = self.db[Word]
            self.db.close()
            return ret
        else:
            self.db.close()
            return False





if __name__ == '__main__':

    sm = CreateBoWText('11')

    with open('Text','rb') as f:
         text = f.readline()
         text = text.decode('utf-8','replace')

    sm.addWebsite('tumblr',text)
    sm.addWebsite('portaaporta','letto')

    print(sm.getWebsiteFromWord('letto'))








