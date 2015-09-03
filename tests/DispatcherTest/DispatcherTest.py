__author__ = 'Luigi'

from src.daemon import Dispatcher

ds = Dispatcher()
ds.addParticipant('11')
ds.inserEvent('11','Event1.json')
ds.getAllEventFromParticipant('11')