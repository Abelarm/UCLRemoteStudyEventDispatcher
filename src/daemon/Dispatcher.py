__author__ = 'Luigi'

import shelve
import os
from Participant import Participant
from Algorithm import Algorithm
import json
from pydoc import locate

class Dispatcher:


    def  __init__(self):

        self.participant = shelve.open('DB/ParticipantDB')

    def loadAlgorithms(self,filename):

        listalg = open(filename,'r')

        if os.path.dirname(os.path.abspath('DB'))+'/DB/AlgorithmDB':
            os.remove(os.path.dirname(os.path.abspath('DB'))+'/DB/AlgorithmDB')
            self.algorithm= shelve.open('DB/AlgorithmDB')

        alg=None

        self.algorithm = shelve.open('DB/AlgorithmDB')

        for line in  listalg:
            line= line.strip()
            line= line.strip('\n')
            line= line.strip(' ')
            line= line.replace('"','')
            line= line.replace(' ','')

            data=line.split(':')[0]

            if (data=='algorithms'):
                flag=True
                continue

            if line == '':
                continue

            if (line == (data+':')):
                if (flag):
                    flag=False
                    alg=Algorithm(data)
                    continue
                self.algorithm[alg.Name]=alg
                alg = Algorithm(data)
                continue
            else:
                if(data=='keys'):
                    for keys in line.split(':')[1].split(','):
                        alg.properties[data].append(keys)
                else:
                    alg.properties[data] = str(line.split(':')[1])

        self.algorithm[alg.Name]=alg
        self.algorithm.close()

    def loadCommands(self,filename):


        if os.path.dirname(os.path.abspath('DB'))+'/DB/CommandsDB':
            os.remove(os.path.dirname(os.path.abspath('DB'))+'/DB/CommandsDB')
            self.commands= shelve.open('DB/CommandsDB')

        with open(filename,'r') as listcommand:
            data = json.load(listcommand)

            #print(data['Commands'])

        self.commands = shelve.open('DB/CommandsDB')

        for key in data['Commands']:

            #print (key)

            for tkey in key:

                self.commands[tkey] = key[tkey]


        self.commands.close()


    def getCommand(self,Command):

        self.commands= shelve.open('DB/CommandsDB')
        if Command in self.commands:
            return self.commands[Command]
        else:
            return False


    def getAlgorithm(self,Name):

        self.algorithm = shelve.open('DB/AlgorithmDB')

        if str(Name) in self.algorithm:
            self.algorithm.close()
            return self.algorithm[Name]
        else:
            self.algorithm.close()
            return False

    def addParticipant(self,ParticipantID):

        self.participant = shelve.open('DB/ParticipantDB')

        if not str(ParticipantID) in self.participant:
            self.participant[str(ParticipantID)] = Participant(str(ParticipantID))
            self.participant.close()
            return True
        else:
            self.participant.close()
            return False

    def inserEvent(self,ParticipandID,Event):

        self.participant = shelve.open('DB/ParticipantDB')

        if ParticipandID not in self.participant:
            return False
        toret=self.participant[ParticipandID].insertEvent(Event)
        self.participant.close()
        return toret

    def setComputed(self,ParticipantID,EventID,AlgName,Version):

        self.participant = shelve.open('DB/ParticipantDB')

        if ParticipantID in self.participant:

            toreturn = self.participant[ParticipantID].setComputated(EventID,AlgName,Version)
            self.participant.close()
            return toreturn
        else:
            self.participant.close()
            return False

    def getEventFromParticipant(self, ParticipantID, EventID):

        self.participant = shelve.open('DB/ParticipantDB')

        if str(ParticipantID) in self.participant:
            Event = self.participant[str(ParticipantID)].getEvent(str(EventID))
            return Event
        else:
            return False

    def getAllEventFromParticipant(self,ParticipantID):

        self.participant = shelve.open('DB/ParticipantDB')

        if str(ParticipantID) in self.participant:
            return self.participant[str(ParticipantID)].getAllEvents()


    def compute(self,ParticipantID,Event):

        self.participant = shelve.open('DB/ParticipantDB')
        self.algorithm = shelve.open('DB/AlgorithmDB')

        mainevent = self.getEventFromParticipant(ParticipantID,str(Event[0]))

        #print(mainevent.data)

        for algorithmID in self.algorithm:

            version = self.algorithm[algorithmID].getVersion()

            flag = True
            
            for event in self.getAllEventFromParticipant(ParticipantID):

                keys = self.algorithm[algorithmID].getKeys()
                DataKey = event.getDataFromKeys(keys)
                mainDataKey = mainevent.getDataFromKeys(keys)

                if event.getID() == mainevent.getID():
                    continue

                #print("Iter:"+str(DataKey))
                #print("Event:"+str(mainDataKey))

                if DataKey == mainDataKey and version == event.getAlgVersion(algorithmID):
                    flag = False
                    break

            if flag:
                self.setComputed(ParticipantID,str(Event[0]),algorithmID,version)
                print("Compute: "+ self.algorithm[algorithmID].Name)
                directory='Participant_'+ParticipantID
                if not os.path.exists(directory):
                    os.makedirs(directory)

                p=self.algorithm[algorithmID].getPath()
                if p:
                    subdirectory=directory+p
                else:
                    subdirectory=directory+'/Event_'+mainevent.getID()

                if not os.path.exists(subdirectory):
                    os.makedirs(subdirectory)

                #f.write('DONE\n')
                param = []
                for x in keys:
                    if x=="Password":
                        #f.write(Event[1]+'\n')
                        param.append(Event[1])
                    else:
                        #f.write(mainevent.data[x]+'\n')
                        param.append(mainevent.data[x])

                #print(algorithmID)
                #print(param)
                loadedclass  = locate('Algorithms.'+algorithmID+'.'+algorithmID+'.'+algorithmID)
                param.append(subdirectory+'/')
                loadedclass(*param)
                param=[]


                #time.sleep(3)
            else:
                print("Already computed: "+self.algorithm[algorithmID].Name)


        self.participant.close()
        self.algorithm.close()


    def deleteParticipant(self,ParticipantID):

        self.participant = shelve.open('DB/ParticipantDB')

        if ParticipantID in self.participant:
            self.participant[ParticipantID].deleteEvents()
            self.participant[ParticipantID]=None
            del(self.participant[ParticipantID])
            self.participant.close()
            return True
        else:
            return False

    def deleteEvent(self,ParticipantID,EventID):

        self.participant = shelve.open('DB/ParticipantDB')

        if ParticipantID in self.participant:

            toreturn =self.participant[ParticipantID].deleteEvent(EventID)
            self.participant.close()
            return toreturn

        return False


    def deletePassword(self,ParticipantID,Password):

        self.participant = shelve.open('DB/ParticipantDB')

        if ParticipantID in self.participant:

            toreturn= self.participant[ParticipantID].deleteEventFromPassword(Password)
            self.participant.close()
            return toreturn

        return False





def main():
    #Listner(None,None,None,None,None)
    Menu()


def Menu():

    disp=Dispatcher()
    disp.loadAlgorithms('Configurations/Algorithms.yml')
    disp.loadCommands('Configurations/Commands.json')

    commands= "1)insert participant:\n" \
              "2)load event(after insertion will be some computing)\n" \
              "3)Get all Event from participant\n" \
              "4)Delete participant\n" \
              "5)Delete Event\n" \
              "6)Delete Password\n" \
              "0)EXIT"
    prompt="\n>>"

    def insert():
        id = input("Give ID of user:"+prompt)
        if not disp.addParticipant(id):
            print("Somenthing wrong!!")

    def loadEvent():
        id = input("Give ID of which user create event:"+prompt)
        path = input("Give path of event:"+prompt)
        eve=disp.inserEvent(id,path)
        if not eve:
            print("Somenthing wrong!!")
            return False
        print("EventID:"+ eve[0])
        disp.compute(id,eve)

    def getAllEvent():
        id = input("Give ID of user:"+prompt)
        for x in disp.getAllEventFromParticipant(id):
            if not x == None:
                print(x)

    def ext():
        print("Have a nice day")


    def deleteParticipant():
        id = input("Give ID of which user want to delete:"+prompt)
        disp.deleteParticipant(id)

    def deleteEvent():
        idp = input("Give ID of which user want to deletes event:"+prompt)
        ide = input("Give ID of the event:"+prompt)

        if not idp or not ide:
            print("Somenthing wrong!!")
        if not disp.deleteEvent(idp,ide):
            print("Somenthing wrong!!")


    def deletePassword():
        idp = input("Give ID of which user want to delete password:"+prompt)
        passw= input("Give password:"+prompt)

        disp.deletePassword(idp,passw)


    options={1:insert,
            2:loadEvent,
            3:getAllEvent,
            4:deleteParticipant,
            5:deleteEvent,
            6:deletePassword,
            0:ext}

    while True:

        command = input("What you wanna do:\n"+commands+prompt)
        options[int(command)]()
        if int(command)==0:
            break


if __name__ == "__main__":
    main()
