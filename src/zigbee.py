#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Author: Benjamin Sinclair
# Revision Date: 17/10/2022
# Name: zigbee.py
# 
# This file uses the killerbee library to create a packet sniffer and inject
# packets
# ---------------------------------------------------------------------------

from killerbee import *
import os
import zigbee_crypt

# Sniffer class wrapper around killerbee functions
class Sniffer: 
    def __init__(self):
        self.reset()
    
    # Function that reads packets from kb object
    def readPacket(self):
        packet = self.kb.pnext()
        if packet != None:
            #print(packet)
            self.message = "0x" + str(packet['bytes'].hex()) + "\n"
            return packet
        else:
            self.message = ""
               
    def getMessage(self):
        return self.message 
        
    def sendPacket(self, packet):
        return self.kb.inject(packet)
        
    def reset(self):
        # Store latest message to pass on
        self.message = ""
        with KillerBee() as self.kb:
            try: 
                self.kb.set_channel(11,)
            except:
                print("Error setting channel")
                sys.exit(1)
        self.kb.sniffer_on()
        
class Packet:
    def __init__(self, data):
        self.data = data
        self.bytes = data['bytes']
        self.hex = self.bytes.hex()
        # Destination address - reverse byte order
        self.dest = self.hex[12:14] + self.hex[10:12]
        # Source address - reverse byte order
        self.source = self.hex[16:18] + self.hex[14:16]
        # Packet sequence  - reverse byte order
        self.pan = self.hex[8:10] + self.hex[6:8]
        # Zigbee security header
        self.zigbeeSecHeader = self.hex[50:112]
        #print(self.zigbeeSecHeader)
        self.decrypted = self.decrypt(data)

    # Check if packet is valid
    def checkValid(self):
        return self.data['validcrc']
    
    # Decrypt function TODO complete
    def decrypt(self, data):
        enc=bytes.fromhex("0e7a7c0f5bea66001f3eca92a6b3")
        key=bytes.fromhex("ab99c8ef8cfcd001eb7ab4abfdca014e")
        scf=bytes.fromhex("28")
        mic=bytes.fromhex("e3a08643")
        source=0x977a
        # Get control byte
        ctrl_byte = 0x28
        fc = 1681115
        # Calculate nonce
        nonce = struct.pack('L',source) + struct.pack('I',fc)
        #decr = zigbee_crypt.decrypt_ccm(key, nonce, mic, enc, scf)
        #print(decr)
    
    # Return packet information
    def getInfo(self):
        info = {}
        info['source'] = self.source
        info['dest'] = self.dest
        info['pan'] = self.pan
        return info
    
    def getRaw(self):
        # Return raw packet in hex
        return "0x" + self.hex
        
