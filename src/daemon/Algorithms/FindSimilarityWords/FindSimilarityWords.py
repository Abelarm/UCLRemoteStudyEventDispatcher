__author__ = 'Luigi'
import shelve
import wordsegment
import nltk.stem as lem
import nltk
from pydoc import locate
import sys,os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from CreateBoWText import CreateBoWText
from CreateBoWPassword import CreateBoWPassword

class FindSimilarityWords:

    def __init__(self,Text,Website,Password,HashPassword,writePath=None,Path=None):

        if Path:
            self.filenamePass = Path + 'SimilarityObjects_Pass'
            self.filenameText  = Path + 'SimilarityObjects_Text'
            self.path = Path
        else:
            self.filenamePass = 'SimilarityObjects_Pass'
            self.filenameText  = 'SimilarityObjects_Text'
            self.path=''

        if writePath:
            self.writePath=writePath
        else:
            self.writePath=''

        self.dbPass = shelve.open(self.filenamePass)
        self.dbText = shelve.open(self.filenameText)

        self.dbPass.close()
        self.dbPass.close()

        self.Text = Text
        self.Website = Website
        self.Password = Password
        self.HashPassword = HashPassword

        nltk.data.path.append("/opt/python3-inst/share/")
        
        self.ComputeSimilarity()       
 
    def ComputeSimilarity(self):

        self.dbPass = shelve.open(self.filenamePass)
        self.dbText = shelve.open(self.filenameText)

        CBOWP  = CreateBoWPassword        
       
        try:
            self.dbPass["Class"]
        except KeyError:
            self.dbPass["Class"] = CBOWP(self.path)

        CBOWT = CreateBoWText

        try:
            self.dbText["Class"]
        except KeyError:
            self.dbText["Class"] = CBOWT(self.path)

        self.dbPass.close()
        self.dbText.close()
    
        self.dbPass = shelve.open(self.filenamePass)
        self.dbText = shelve.open(self.filenameText)   
  
        ListOfWords = wordsegment.segment(self.Password)

        ListOfWordsLem = set()
        wnl = lem.WordNetLemmatizer()

        for word in ListOfWords:
            ListOfWordsLem.add(wnl.lemmatize(word))

        listOfWebsite = set()
        listOfPassword = set()

        for word in ListOfWordsLem:
            Web=self.dbText["Class"].getWebsiteFromWord(word)
            Pass=self.dbPass["Class"].getPasswordFromWord(word)
            
            if Web:
                #print(set(Web))
                [listOfWebsite.add(w) for w in Web]
            if Pass:
                #print(set(Pass))    
                [listOfPassword.add(p) for p in Pass]

        #Maybe create 2 process for doing this and wait until finish
        self.dbPass["Class"].addPassword(ListOfWordsLem,self.HashPassword)
        self.dbText["Class"].addWebsite(self.Website,self.Text)
        print('DONE FindSimilarityWord')

        #print(listOfWebsite)
        #print(listOfPassword)

        self.dbPass.close()
        self.dbPass.close()

        with open(self.writePath+'FindSimilarity','w') as o:
            if listOfWebsite:
                o.write('Password found in website:')
                o.write(str(listOfWebsite))
            if listOfPassword:
                o.write('Password found in word:')
                o.write(str(listOfPassword))


if __name__ == '__main__':

    with open('Text','rb') as f:
         btext = f.readline()
         text = btext.decode("utf-8", "replace")

    FSW = FindSimilarityWords(text,'tumblr','gif','asdasdasda','','')
    #print(FSW.ComputeSimilarity(text,'tumblr','gif','dascasdasca'))
    #print(FSW.ComputeSimilarity(text,'google','cervello','asdasda'))



