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
from zigbee_crypt import *

# Sniffer class wrapper around killerbee functions
class Sniffer:
    def __init__(self):
        # Set default channel to 11
        self.channel = 11
        self.reset()
        #self.channelScan()

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

    # Scan for channels broadcasting
    def channelScan(self):
        # Beacon frame
        beacon = b"\x03\x08\x00\xff\xff\xff\xff\x07"
        # Split beacon around sequence number field
        beaconp1 = beacon[0:2]
        beaconp2 = beacon[3:]
        # Track sequence number
        seqNum = 0
        # Loop through each channel
        for c in range(11,26):
            # Iterations per channel
            for i in range(0,50):
                # Loop sequence number around if too height
                if seqNum > 255:
                    seqNum = 0
                # Try setting the channel
                try:
                    self.kb.set_channel(c)
                except Exception as e:
                    print("Error setting channel")
                    sys.exit(1)

                # Send beacon frame
                beacon = b''.join([beaconp1, b"%c" % seqNum, beaconp2])
                # Increment sequence number
                seqNum += 1
                self.sendPacket(beacon)

                # Receive packet
                if self.kb.pnext(2) != None:
                    channel = c
                    print("Channel found: ", c)
                    break


    def reset(self):
        # Store latest message to pass on
        self.message = ""
        with KillerBee() as self.kb:
            try:

                self.kb.set_channel(self.channel,)
            except:
                print("Error setting channel")
                sys.exit(1)
        self.kb.sniffer_on()

class Packet:
    def __init__(self, data):
        self.data = data
        self.rawBytes = data['bytes']
        self.hex = self.rawBytes.hex()
        self.key = bytes.fromhex("ab99c8ef8cfcd001eb7ab4abfdca014e")
        self.decoded = self.decode()

    # Check if packet is valid
    def checkValid(self):
        return self.data['validcrc']

    # Decode function
    def decode(self):
        d154 = Dot154PacketParser()
        # Chop the packet up
        pktdecode = d154.pktchop(self.data[0])
        # Reverse byte order
        source = pktdecode[5][::-1]
        dest = pktdecode[3][::-1]
        pan = pktdecode[2][::-1]
        payload = pktdecode[7][::-1]
        # Convert to hex
        self.source = source.hex()
        self.dest = dest.hex()
        self.pan = pan.hex()
        self.payload = payload.hex()

        # Use supplied key

        # Test frame 1
        #
        #key = bytes.fromhex("ab99c8ef8cfcd001eb7ab4abfdca014e")
        #rawData = bytes.fromhex("4188d4b478ffff7a970912fcff7a971eb6b608d1010188170028ef2b2c00b608d101018817000051c28d032b1816c7a997a3df77907bb84e0a8131")
        rawData = self.rawBytes
        print("Bytes " + rawData.hex())
        nwkHeader = rawData[9:17]
        print("Network Header " + nwkHeader.hex())
        auxHeader = bytes.fromhex("2d") + rawData[26:39]
        print("Aux Header " + auxHeader.hex())
        a = nwkHeader + auxHeader
        m = rawData[39:53]
        mic = rawData[53:57]
        print("a " + a.hex())
        print("m " + m.hex())
        print("mic " + mic.hex())
        # Nonce made of source address fields of aux header, security control and frame counter
        sourceAdd = rawData[30:38]
        frameCount = rawData[26:30]
        nonce = sourceAdd + frameCount + bytes.fromhex("2d")
        print(nonce.hex())
        #
        # Test frame 2
        #
        #key =   bytes([0xAD, 0x8E, 0xBB, 0xC4, 0xF9, 0x6A, 0xE7, 0x00, 0x05, 0x06, 0xD3, 0xFC, 0xD1, 0x62, 0x7F, 0xB8])
        #NwkHeader = bytes([0x48, 0x02, 0x00, 0x00, 0x8A, 0x5C, 0x1E, 0x5D])
        #AuxiliaryHeader = bytes([0x2D, 0xE1, 0x00, 0x00, 0x00, 0x01, 0x3C, 0xE8, 0x01, 0x00, 0x8D, 0x15, 0x00, 0x01])
        #nonce = bytes([0x01, 0x3C, 0xE8, 0x01, 0x00, 0x8D, 0x15, 0x00  ,  0xE1, 0x00, 0x00, 0x00  ,  0x2D])
        #a = NwkHeader + AuxiliaryHeader
        #m = bytes.fromhex("ea59de1f960eea8aee185a1189309641")
        #mic = bytes.fromhex("ac4c76af")
        decrypted, success = decrypt_ccm(self.key, nonce, mic, m, a)
        print(decrypted.hex())
        
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
