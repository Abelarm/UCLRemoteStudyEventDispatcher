__author__ = 'Luigi'

import shelve
from Event import Event
import os

class Participant:

    def __init__(self,ParticipantID):

        self.filenameEvents ='DB/Participant_'+ str(ParticipantID)+'_EventsDB'
        db = shelve.open(self.filenameEvents)
        db.close()

    def insertEvent(self,EventID,WebSite,Username,Password):

        db = shelve.open(self.filenameEvents)

        if not str(EventID) in db:
            #Add Event#
            db[str(EventID)] = Event(EventID,WebSite,Username,Password)
            db.close()
            return True
        else:
            db.close()
            return False


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


    def setComputated(self,EventID,AlgName,Version):
        db =shelve.open(self.filenameEvents)

        if EventID in db:
            db[EventID]=db[EventID].setComputated(AlgName,Version)
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

    def deleteEvents(self):
        if os.path.dirname(os.path.abspath('DB'))+'/'+self.filenameEvents+'.db':
            os.remove(os.path.dirname(os.path.abspath('DB'))+'/'+self.filenameEvents+'.db')




