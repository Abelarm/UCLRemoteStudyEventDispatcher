__author__ = 'Luigi'

import json

#Class that represent an Event of the Framework
class Event:

    def __init__(self):
        self.data=dict()

    #Create the Event data from a json file
    def parseJson(self,EventFile):

        f = open(EventFile,'r',-1,'utf-8','replace')
     
        self.data = json.load(f)
        password = self.data["Password"]
        del self.data["Password"]
        #Algorithms that have been calculated for this Event
        self.data["Algorithms"]=dict()
        return password

    #Create the Event from a dict
    def addData(self,Event):

        self.data = Event
        #Algorithms that have been calculated for this Event
        self.data["Algorithms"]=dict()
        password = self.data["Password"]
        del self.data["Password"]
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
            toreturn.append(self.data[key])
        return toreturn


    def setComputed(self,AlgName,Version):

        self.data['Algorithms'][AlgName]=Version
        return self

    def comparePassword(self,HashPassword):

        if self.data["HashPassword"]==HashPassword:
            return True
        else:
            return False

    def compareWebsite(self,Website):

        if self.data["HashPassword"]==Website:
            return True
        else:
            return False

    def getAlgVersion(self,AlgName):

        if AlgName in self.data['Algorithms']:
            return self.data['Algorithms'][AlgName]
        else:
            return False

    def getPrintEvent(self):

        toret = dict(self)
        try:
            del(toret.data['Algorithms'])
        except (KeyError):
            True
        return toret


    def __str__(self):
        return str(self.data)


def main():

    Eve = Event()
    print(Eve.parseJson('Event1.json'))

    Eve.setComputated('CIAO','10')

    print(Eve.getAlgVersion('CIAO'))

    print(Eve.comparePassword('secret'))



if __name__ == "__main__":
    main()
