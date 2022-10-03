# Import dependancies
from killerbee import *
import os

# Inspired by code in zbwireshark

class Sniffer: 
    def __init__(self):
        # Store latest message to pass on
        self.message = ""
        with KillerBee() as self.kb:
            try: 
                self.kb.set_channel(11,)
            except:
                print("Error setting channel")
                sys.exit(1)
        self.kb.sniffer_on()

    def readPacket(self):
        packet = self.kb.pnext()
        if packet != None:
            self.message = str(packet['bytes'])
            return packet['bytes'] 
        else:
            self.message = ""
               
    def getMessage(self):
        return self.message 
        
class Transmitter:
    def __init__(self):
        self.message = ""
        
    def sendPacket(self, data):
        return data
        
    def getMessage(self):
        return self.message
        