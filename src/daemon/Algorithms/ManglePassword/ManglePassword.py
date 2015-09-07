# -*- coding: utf-8 -*-
__author__ = 'Luigi'

import shelve
import scrypt
import os,binascii
import os


class ManglePassword:
    def __init__(self, password,writePath=None,path=None):



        self.password = password

        if path:
            self.filepath = path  + 'HashPass'
        else:
            self.filepath =  'HashPass'

        print(self.filepath)

        db = shelve.open(self.filepath)

        name="salt"

        if not name in db:
            raw = os.urandom(16)
            salt = binascii.hexlify(raw)
            db[name]=salt


        db.close()
        db = shelve.open(self.filepath)

        self.hashPassword()

        try:
            # print(db['variations'])
            hasedvar = db['variations']
            if self.hashedpassword in list(hasedvar.values()):
                with open(writePath+'ManglePassword') as o:
                    o.write('hash found:')
                    o.write(self.hashedpassword)
                return

        except KeyError:
            # return
            True
            # print('Hash not found')
            # traceback.print_exc(file=sys.stdout)

        db.close()
        self.hashedpass = {}

        self.rules = []
        self.symbols = []
        self.keyboardrule= {}

        self.variations = []
        self.subvariations = []

        print('Appling the rules')
        self.addRules()
        self.addSymbol()
        pathFi = os.path.dirname(os.path.realpath(__file__))
        self.parseKeyboardFile(pathFi+'/KeyboardUK')


        self.applyMangle(5000)


    def addRules(self, otherrule=None):

        self.rules.append(['@', 'a', 'A'])
        self.rules.append(['i', '1'])
        self.rules.append(['o', 'O', '0'])
        self.rules.append(['$', 's', 'S', '5'])
        self.rules.append(['3', 'e', 'E', '€'])
        self.rules.append(['9', '6', 'g', 'G'])
        self.rules.append(['8', 'B', 'b'])
        self.rules.append(['"', '2'])
        self.rules.append(['£', '3'])
        self.rules.append(['$', '€', '4'])
        self.rules.append(['%', '5'])
        self.rules.append(['^', '6'])
        self.rules.append(['&', '7'])
        self.rules.append(['*', '8'])
        self.rules.append(['(', '9'])
        self.rules.append([')', '0'])
        self.rules.append(['-', '_', '–'])
        self.rules.append(['(', '{', '['])
        self.rules.append([')', '}', ']'])
        self.rules.append([';', ':'])
        self.rules.append(['@', '\''])
        self.rules.append(['~', '#'])
        self.rules.append(['<', ','])
        self.rules.append(['>', '.'])
        self.rules.append(['?', '/'])
        self.rules.append(['|', '\\'])

        if otherrule:
            self.rules.append(otherrule)


    def parseKeyboardFile(self, path):

        with open(path,'rb') as f:
            for raw in f:
               
                line = raw.decode('utf-8','replace')
                line=line.strip('\n')

                div= line.split("= ",1)
                c = div[0]
                lis = div[1].split(' ')

                self.keyboardrule[c] = lis



        return


    def addSymbol(self, othersymbol=None):

        self.symbols = ['!', "+", '=', '?', '/', '\\', '#', '%', '&', '*', ';', ':']

        if othersymbol:
            self.symbols.append(othersymbol)


    def substitute(self,Threshold=10):


        for s in self.rules:
            for c in self.password:
                if c in s:
                    i = 1
                    while i <= self.password.count(c) and i <= Threshold:
                        for x in s:
                            if not x == c:
                                self.variations.append(self.password.replace(c, x, i))
                        i = i + 1


    def resubsitute(self,Threshold=10):


        resos = []

        for s in self.rules:
            for v in self.variations:
                for c in v:
                    if c in s:
                        i = 1
                        while i <= v.count(c) and i <= Threshold:
                            for x in s:
                                if not x == c:
                                    tmp = v.replace(c, x, i)
                                    if not tmp == self.password and not tmp in self.variations:
                                        resos.append(tmp)
                            i = i + 1

        self.variations = self.variations + resos


    def substituteKeyboard(self,Threshold=10):

        for k in self.keyboardrule.keys():

            for c in self.password:

                if c == k:
                    i = 0
                    while i <= self.password.count(c) and i <= Threshold :
                        for r in self.keyboardrule[k]:
                            rep= self.password.replace(c,r,i)

                            if rep not in self.variations:
                                self.variations.append(rep)
                        i = i +1


    def appendSymbol(self):

        for s in self.symbols:
            self.variations.append(self.password + s)
            self.variations.append(s + self.password)


    def appendNumber(self,MAX):

        for i in range(0,MAX):

            self.variations.append(self.password+str(i))


    def incrementNumber(self):

        for n in range(0, 9):
            if str(n) in self.password:
                i = self.password.index((str(n)))

                self.variations.append(self.password[:(i)] + str(n + 1) + self.password[(i + 1):])


    def appendYear(self, year):

        self.variations.append(self.password + str(year))
        self.variations.append(self.password + str(year)[2:])


    def reverse(self):

        self.variations.append(self.password[::-1])


    def upperLower(self):

        man=[]
        man.append(self.password.upper())
        man.append(self.password.lower())
        man.append(self.password[0].upper()+self.password[1:])
        man.append(self.altLowUpp(self.password))
        man.append(self.altUppLow(self.password))

        for x in man:
            if x not in self.variations:
                self.variations.append(x)

        sosupplow=[]

        for v in self.variations:

            man=[]

            u = v.upper()
            if len(u) == len(v):
                man.append(u)

            l = v.lower()
            if len(l) == len(v):
                man.append(l)

            fu = v[0].upper()+v[:1]
            if len(fu) == len(v):
                man.append(fu)

            man.append(self.altLowUpp(v))
            man.append(self.altUppLow(v))

            for x in man:
                if x not in self.variations and x not in sosupplow:
                    sosupplow.append(x)

        self.variations = self.variations + sosupplow


    def altLowUpp(self,string):

        i=0
        ret = ''
        for c in string:
            if (i % 2) ==0:
                ret = ret + c.lower()
            else:
                ret = ret + c.upper()

            i = i+1

        if len(ret) == len(string):
            return ret
        else:
            return None


    def altUppLow(self,string):

        i=0
        ret = ''
        for c in string:
            if (i % 2) ==0:
                ret = ret + c.upper()
            else:
                ret = ret + c.lower()

            i = i + 1

        if len(ret) == len(string):
            return ret
        else:
            return None


    def removeDuplicate(self):

        self.variations=list(set(self.variations))


    def hashPassword(self):

        db = shelve.open(self.filepath)
        name="salt"
        salt = db[name]
        hashedpass=binascii.hexlify(scrypt.hash(self.password, salt, 2048, 8, 1, 64))

        db.close()

        self.hashedpassword = hashedpass


    def hashVariations(self):
        i = 0

        db = shelve.open(self.filepath)
        salt = db[str("salt")]
        for p in self.variations:
            #print("Hashing " + str(i) + " variations")
            self.hashedpass['var' + str(i)] = binascii.hexlify(scrypt.hash(p, salt, 2048, 8, 1, 64))
            i = i + 1

        self.hashedpass['var' + str(i + 1)] = self.hashedpassword

        try:
            oldhash = db['variations']
        except KeyError:
            oldhash = {}

        newhash = oldhash.copy()
        newhash.update(self.hashedpass)
        db['variations'] = newhash
        db.close()


    def applyMangle(self,N, listofyears=['2015']):

        self.substitute()
        self.resubsitute()
        self.substituteKeyboard()
        self.appendSymbol()
        self.incrementNumber()
        self.appendNumber(N)
        for y in listofyears:
            self.appendYear(y)
        self.reverse()
        self.upperLower()
        self.removeDuplicate()

        #self.hashVariations()

        #print(self.variations)
        #print(len(self.variations))


def main():
    ManglePassword('asdasd')

    # print(len(mp.variations))
    # print(mp.variations)


if __name__ == "__main__":
    main()
