#The Event class methods:

    parseJson(EventFile) [create Event from jsonFile]

    addData(Event) [create Event from json formatted data]

    getID [return the ID of the event]

    getDataFromKeys(keys) [get the Event data from given Keys]
        keys :{"Password","Hashpassword"}

    setComputed(AlgName, AlgVersion) [set the AlgName computed for this event]

    comparePassword(HashPassword) [compare tha hash given with the hash of event]

    getAlgVersion(AlgName) [get the version of the Algorithm computed with AlgName]


#The Algorithm class methods:

    getKeys() [return the keys of the algorithm]

    getVersion() [return the version of the algorithm]

    getPath() [return the path of the algorithm]


#The Participant class method:

    insertEvent(Eventdata,fileName=None) [insert a event for the current participant, if fileName given
                                            create the Event from that file]

    setComputed(EventID,AlgName,Version) [set the Algorithm AlgName computed for the Event (EventID)]

    getEvent(EventID) [get the event from EventID]

    getAllEvents() [return all the event for the current participant]

    deleteEvent(EventID) [delete the Event having EvenID]

    deleteEventFromPassword(Password) [delete all the events having this Password]
