__author__ = 'Luigi'

import json

class Event:

    # def __init__(self,EventID,WebSite,Username,Password):
    #
    #     self.EventID= EventID
    #     self.WebSite= WebSite
    #     self.Username = Username
    #     self.Password = Password

    def parseJson(self,EventFile):

        f = open(EventFile,'r',-1,'utf-8','replace')
     
        self.data = json.load(f)
        password = self.data["Password"]
        #self.data["Password"] = crypt(password)
        self.data['Algorithms']=dict()
        return password


    def addData(self,Event):

        self.data = Event
        self.data['Algorithms']=dict()
        password = self.data['Password']
        #self.data['Password'] = crypt(password)
        return password

    def getID(self):
        try:
            self.EventID
        except AttributeError:
            return self.data["ID"]
        else:
            return self.EventID

    def getDataFromKeys(self,Keys):
        toreturn=[]
        for key in Keys:
            #print(key)
            toreturn.append(self.data[key])
        return toreturn


    def setComputated(self,AlgName,Version):

        self.data['Algorithms'][AlgName]=Version
        return self

    def comparePassword(self,Password):

        if self.data["HashPassword"]==Password:
            return True
        else:
            return False

    def getAlgVersion(self,AlgName):

        if AlgName in self.data['Algorithms']:
            return self.data['Algorithms'][AlgName]
        else:
            return False

    def getPrintEvent(self):

        toret = self
        try:
            del(toret.data['Algorithms'])
        except (KeyError):
            None
        return toret

    def loadConf(self):

        conf = open('Configurations/Event.yml','r')

        self.properties= dict()

        for line in conf:
            nam = line.split(':')[0]
            typ = line.split(':')[1]

            if typ == '+':
                self.properties[nam]=[]
            else:
                self.properties[nam]=str()


    def __str__(self):
        return str(self.data)

    #def __str__(self):
    #    return 'ID '+ self.EventID+ ' WebSite ' + self.WebSite + ' Username ' + self.Username + ' Password ' + self.Password


def main():

    #Eve = Event('1','google.com','a','b')

    Eve = Event()
    print(Eve.parseJson('Event1.json'))

    Eve.setComputated('CIAO','10')

    print(Eve.getAlgVersion('CIAO'))

    print(Eve.comparePassword('secret'))

    # for x in Eve.properties:
    #
    #     data = input('GIMME: ' + x + ' ')
    #
    #     if not ',' in data:
    #         Eve.properties[x]=data
    #         continue
    #
    #     for subdata in data.split(','):
    #         Eve.properties[x].append(subdata)
    #
    # print (Eve.properties)


if __name__ == "__main__":
    main()
