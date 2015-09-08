__author__ = 'Luigi'

import shelve
import scrypt
import os,binascii

class CreateBoWPassword:

    def __init__(self,path=None):

        if path:
            self.filename = path+'Words_Password'
        else:
            self.filename = 'Words_Password'

        
        self.db = shelve.open(self.filename)

        self.name=str('salt')

        if not self.name in self.db:
            raw = os.urandom(32)
            salt = binascii.hexlify(raw)
            self.db[self.name]=salt


        self.db.close()


    def addPassword(self,ListOfWords,HashPassword):

        self.db = shelve.open(self.filename)

        salt = self.db[self.name]

        for w in ListOfWords:
            #print(w)
            w=w.lower()

            hashw = binascii.hexlify(scrypt.hash(w, salt, 2048, 8, 1, 64))

            if str(hashw) in self.db.keys():
                l = self.db[str(hashw)]
                l.add(HashPassword)
                self.db[str(hashw)] = l
                #print(l)
            else:
                self.db[str(hashw)] = {HashPassword}
                #print(self.db[str(hashw)])
        self.db.close()


    def getPasswordFromWord(self,Word):

        self.db = shelve.open(self.filename)

        salt = self.db[self.name]

        Word = Word.lower()

        hashw = binascii.hexlify(scrypt.hash(Word, salt, 2048, 8, 1, 64))
	
        #print(hashw)
        #print(salt)
        #print(self.db)
	
        if str(hashw) in self.db.keys():

            ret = self.db[str(hashw)]
            self.db.close()
            return ret

        else:

            self.db.close()
            return False








if __name__ == '__main__':

    cb = CreateBoWPassword('11')

    hasp= binascii.hexlify(scrypt.hash('asdacasfasa', str(12), 2048, 8, 1, 64))
    hasp2= binascii.hexlify(scrypt.hash('ciaobello', str(12), 2048, 8, 1, 64))

    cb.addPassword(['monkey','Fish'],hasp)
    cb.addPassword(['fish','potato'],hasp2)

    print(cb.getPasswordFromWord('FiSh'))









