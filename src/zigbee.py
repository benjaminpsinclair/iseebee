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
        
class Packet:
    def __init__(self, data):
        self.data = data
        # Destination address
        self.dest = data[10:12]
        # Source address
        self.source = data[13:15]
        # Protocol 
        self.seqNum = data[16:17]
    
    def getInfo(self):
        info = []
        info.append(self.source)
        info.append(self.dest)
        info.append(self.seqNum)
        return info
    
    def getRaw(self):
        return str(self.data)
        
