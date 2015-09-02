__author__ = 'Luigi'

#from wordsegment import segment
#from nltk.stem import WordNetLemmatizer
#import nltk
from zxcvbn import main as zx

if __name__ == '__main__':
    
    #print(segment('provagiallo'))
    #nltk.data.path.append("/opt/python3-inst/share/");
    #wnl = WordNetLemmatizer()
    #print(wnl.lemmatize('dogs'))
    print(zx.password_strength('ciao'))   
