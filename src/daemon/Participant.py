__author__ = 'Luigi'

import shelve
from Event import Event
import os

#Class that represent an Event of the Framework
class Participant:

    def __init__(self,ParticipantID,ConfigPath):

        self.ConfigPath = ConfigPath
        self.filenameEvents =self.ConfigPath['prefix'] + self.ConfigPath['DB'] +'/'+str(ParticipantID)+'_EventsDB'
        db = shelve.open(self.filenameEvents)
        db.close()

    def insertEvent(self,Eventdata,fileName=None):

        db =shelve.open(self.filenameEvents)

        event = Event()
        if not fileName==None:
            password = event.parseJson(fileName)
        else:
            password= event.addData(Eventdata)

        if not str(event.data["ID"]) in db:
            db[str(event.data["ID"])]=event
            db.close()
            return [event.data["ID"],password]
        else:
            db.close()
            return False


    def setComputed(self,EventID,AlgName,Version):

        db =shelve.open(self.filenameEvents)

        if EventID in db:
            db[EventID]=db[EventID].setComputed(AlgName,Version)
            db.close()
            return True
        else:
            db.close()
            return False

    def getEvent(self,EventID):

        db = shelve.open(self.filenameEvents)

        if not str(EventID) in db:
            db.close()
            return False
        else:
            return db[EventID]
            db.close()


    def getAllEvents(self):

        db = shelve.open(self.filenameEvents)
        toreturn=[]

        for key in db.keys():
            #print (db[key])
            toreturn.append(db[key])

        db.close()
        return toreturn

    def deleteEvent(self,EventID):

        db= shelve.open(self.filenameEvents)
        if EventID not in db:
            db.close()
            return False
        else:
            del(db[EventID])
            db.close()
            return True

    def deleteEventFromPassword(self,Password):

        db = shelve.open(self.filenameEvents)

        for event in db:

            if db[event].comparePassword(Password):
                del(db[event])

        db.close()

    def deleteEventWebsite(self,Website):

        db = shelve.open(self.filenameEvents)

        for event in db:

            if db[event].compareWebiste(Website):
                del(db[event])

        db.close()

    def deleteEvents(self):
        if os.path.dirname(os.path.abspath('DB'))+'/'+self.filenameEvents:
            os.remove(os.path.dirname(os.path.abspath('DB'))+'/'+self.filenameEvents)




