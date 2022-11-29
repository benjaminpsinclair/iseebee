#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Author: Benjamin Sinclair
# Revision Date: 17/10/2022
# Name: iseebee.py
#
# ---------------------------------------------------------------------------
# The main file for the iseebee application. This uses the zigbee.py file to
# create a sniffer and gui.py for the window.
#
# This is the file to run using 'python3 iseebee.py'

import zigbee
import gui
import objects
import time
import sys

def main():
    # Declare global variables
    global window, sniff, network, packets, key, channel
    key = "ab99c8ef8cfcd001eb7ab4abfdca014e"
    channel = 11
    # Create sniffer object
    try:
        sniff = zigbee.Sniffer(channel)
    except Exception as e:
        # Print exception and exit with error
        print(e)
        sys.exit(1)
    # Create empty packet list
    packets = []
    # Create window
    window = gui.Window('iseebee', '1440x600')
    # Start gui thread
    window.updateChannelKey(channel, key)
    window.start(mainLoop)


def mainLoop():
    global key, channel
    # Try to read packets
    try:
        data = sniff.readPacket()
    except Exception as e:
        window.displayMessage("Error: " + str(e) + '\n')
        window.displayMessage("Resetting USB device\n")
        time.sleep(5)
        sniff.reset()
        data = None
    if data != None:
        # Add data to packet
        packet = zigbee.Packet(data, key)
        # Add packet to window
        window.displayPacket(packet)
        packets.append(packet)
        info = packet.getInfo()
        window.displayMessage("Packet received, Source: " + "0x" + info['source'] + '\n')
        # Add node for non empty sources
        if info['source'] != "":
            window.addNode(info['source'])
        # Add message from the sniffer to the window
        window.displayMessage(sniff.getMessage())
        if packet.checkValid():
            window.displayMessage("Packet is valid\n")
        else:
            windows.displayMessage("Packet invalid\n")
    # Check for messages to send
    while window.sendingPackets.empty() != True:
        #Convert hex string to bytes
        try:
            packetBytes = bytes.fromhex(window.sendingPackets.get())
            window.displayMessage("Sending message: " + str(packetBytes.hex()) + '\n')
            sniff.sendPacket(packetBytes)

        except Exception as e:
            window.displayMessage("Error: " + str(e) + '\n')
    while window.key.empty() != True:
        key = window.key.get()
        window.updateChannelKey(channel,key)
    while window.channel.empty() != True:
        channel = window.channel.get()
        window.updateChannelKey(channel, key)
    while window.events.empty() != True:
        event = window.events.get()
        if event.name == "scanning":
            sniff.channelScan()
if __name__ == '__main__':
    main()
