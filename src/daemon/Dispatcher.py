__author__ = 'Luigi'

import shelve
import os,sys
from Participant import Participant
from Algorithm import Algorithm
import json
from pydoc import locate
from multiprocessing import Process


############################################
#Class that dispatch all the events        #
#                                          #
############################################
class Dispatcher:

    def  __init__(self,ConfigPath):

        self.ConfigPath = ConfigPath
        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')
  
        sys.path.insert(1, self.ConfigPath['prefix']+self.ConfigPath['Algorithms'])
         
        #print(sys.path)
       
    ############################################
    #Method for loading the Algorithms from a  #
    #configuration file                        #
    ############################################
    def loadAlgorithms(self,filename):

        listalg = open(filename,'r')

        if os.path.dirname(os.path.abspath(self.ConfigPath['DB']))+'/AlgorithmsDB':
            os.remove(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/AlgorithmsDB')
            self.algorithm= shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/AlgorithmsDB')

        alg=None

        self.algorithm = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/AlgorithmsDB')

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




    ############################################
    #Method for loading the Commands for the   #
    #dispatcher from a configuration file      #
    ############################################
    def loadCommands(self,filename):


        if os.path.dirname(os.path.abspath('DB'))+self.ConfigPath['DB']+'/CommandsDB':
            os.remove(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/CommandsDB')
            self.commands= shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/CommandsDB')

        with open(filename,'r') as listcommand:
            data = json.load(listcommand)

            #print(data['Commands'])

        self.commands = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/CommandsDB')

        for key in data['Commands']:

            #print (key)

            for tkey in key:
                self.commands[tkey] = key[tkey]

        self.commands.close()


    def getCommand(self,Command):

        self.commands= shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/CommandsDB')
        if Command in self.commands:
            return self.commands[Command]
        else:
            return False


    def getAlgorithm(self,Name):

        self.algorithm = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/AlgorithmsDB')

        if str(Name) in self.algorithm:
            self.algorithm.close()
            return self.algorithm[Name]
        else:
            self.algorithm.close()
            return False


    def addParticipant(self,ParticipantID):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if not str(ParticipantID) in self.participant:
            self.participant[str(ParticipantID)] = Participant(str(ParticipantID),self.ConfigPath)
            self.participant.close()
            return True
        else:
            self.participant.close()
            return False

    def insertEvent(self,ParticipandID,Event,Test=None):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if ParticipandID not in self.participant:
            self.addParticipant(ParticipandID)
            self.participant.close()
            self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')
        if Test:
            toret=self.participant[ParticipandID].insertEvent(None,Event)
        else:
            toret=self.participant[ParticipandID].insertEvent(Event)
        self.participant.close()
        return toret

    def setComputed(self,ParticipantID,EventID,AlgName,Version):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if ParticipantID in self.participant:
            toreturn = self.participant[ParticipantID].setComputed(EventID,AlgName,Version)
            self.participant.close()
            return toreturn
        else:
            self.participant.close()
            return False

    def getEventFromParticipant(self, ParticipantID, EventID):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if str(ParticipantID) in self.participant:
            Event = self.participant[str(ParticipantID)].getEvent(str(EventID))
            return Event
        else:
            return False

    def getAllEventFromParticipant(self,ParticipantID):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if str(ParticipantID) in self.participant:
            return self.participant[str(ParticipantID)].getAllEvents()

    ############################################
    #Method for computing algorithm            #
    ############################################
    def compute(self,ParticipantID,Event):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')
        self.algorithm = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/AlgorithmsDB')

        mainevent = self.getEventFromParticipant(ParticipantID,str(Event[0]))

        #print(mainevent.data)

        for algorithmID in self.algorithm:

            version = self.algorithm[algorithmID].getVersion()

            flag = True
            
            for event in self.getAllEventFromParticipant(ParticipantID):

                keys = self.algorithm[algorithmID].getKeys()
                wkeys = list(keys)

                if "Password" in wkeys:
                    wkeys.remove("Password")
                    if "HashPassword" not in wkeys:
                        wkeys.append("HashPassword")

                DataKey = event.getDataFromKeys(wkeys)
                mainDataKey = mainevent.getDataFromKeys(wkeys)

                if event.getID() == mainevent.getID():
                    continue

                #print("Iter:"+str(DataKey))
                #print("Event:"+str(mainDataKey))

                #Controll if this algorithm already been launched with this parameters and the same version of it
                if DataKey == mainDataKey and version == event.getAlgVersion(algorithmID):
                    flag = False
                    break

            #if not calculate
            if flag:
                self.setComputed(ParticipantID,str(Event[0]),algorithmID,version)
                print("Compute: "+ self.algorithm[algorithmID].Name)
                directory=self.ConfigPath['prefix']+self.ConfigPath['local']+'/'+self.ConfigPath['projectname']+'/'+ParticipantID
                if not os.path.exists(directory):
                    os.makedirs(directory)

                p=self.algorithm[algorithmID].getPath()
                #ALWAYS append the Event's directory first
                #Directory where we are going to write to write the output file
                subdirectory=[]
                if p:
                    subdirectory.append(directory+'/Event_'+mainevent.getID())
                    subdirectory.append(directory+p+'/')
                else:
                    subdirectory.append(directory+'/Event_'+mainevent.getID())


                for dir in subdirectory:
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                        os.makedirs(dir+'/DATA')

                subdirectory[0] = subdirectory[0]+'/'
                param = []
                for x in keys:
                    #if one of param is password in plain text we pass Event[1] instead of mainevent.data[x]
                    #because we never save plaintext password.
                    if x=="Password":
                        param.append(Event[1])
                    else:
                        param.append(mainevent.data[x])

                #using locate for dynamic loading class (the class MUST be like Algorithms/Test/Test.py(class: Test))
                loadedclass  = locate(algorithmID+'.'+algorithmID+'.'+algorithmID)
                #print(type(loadedclass))
                for s in subdirectory:
                    s=s+'DATA'
                    param.append(s)
                    #print(s)
                proc=Process(target=loadedclass,args=param)
                proc.start()
                param=[]
            else:
                print("Already computed: "+self.algorithm[algorithmID].Name)


        self.participant.close()
        self.algorithm.close()


    def deleteParticipant(self,ParticipantID):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if ParticipantID in self.participant:
            self.participant[ParticipantID].deleteEvents()
            self.participant[ParticipantID]=None
            del(self.participant[ParticipantID])
            self.participant.close()
            return True
        else:
            return False

    def deleteEvent(self,ParticipantID,EventID):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if ParticipantID in self.participant:

            toreturn =self.participant[ParticipantID].deleteEvent(EventID)
            self.participant.close()
            return toreturn

        return False


    def deletePassword(self,ParticipantID,Password):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if ParticipantID in self.participant:

            toreturn= self.participant[ParticipantID].deleteEventFromPassword(Password)
            self.participant.close()
            return toreturn

        return False

    def deleteWebsite(self,ParticipantID,Website):

        self.participant = shelve.open(self.ConfigPath['prefix']+self.ConfigPath['DB']+'/ParticipantDB')

        if ParticipantID in self.participant:

            toreturn= self.participant[ParticipantID].deleteEventFromWebsite(Website)
            self.participant.close()
            return toreturn

        return False





def main():
    Menu()


def Menu():

    disp=Dispatcher(paths)
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
        eve=disp.insertEvent(id,path,Test=True)
        print(eve)
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
