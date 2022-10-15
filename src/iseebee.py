import zigbee
#import gui_old as gui
import gui
import objects
#import hue
import time

def main():
    # Declare global variables
    global window, sniff, network, packets
    # Create sniffer object
    sniff = zigbee.Sniffer()
    # Create network
    network = objects.Network("1")
    # Create empty packet list
    packets = []
    # Create window
    # Add menufunctions into dictionary
    menuFunctions = {
        "newNetwork": newNetwork,
        "openNetwork": openNetwork,
        "saveNetwork": saveNetwork,
        "send": send
    }
    window = gui.Window('iseebee', '1440x600', menuFunctions)
    # Start gui thread
    window.start(mainLoop)
        
def mainLoop():
    # Try to read packets
    try:
        data = sniff.readPacket()
    except Exception as e:
        print("Error: ", e)
        time.sleep(5)
        sniff.reset()
        data = None
    if data != None:
        # Add data to packet
        packet = zigbee.Packet(data)
        # Add packet to window
        window.displayPacket(packet)
        packets.append(packet)
        window.displayMessage("Packet received, Source: " + str(data[13:15]) + '\n')
        if network.searchNode(data[13:15]) == False: 
            node = objects.Node(data[13:15], 700, 150)
            network.addNode(node)
            window.drawNodes(network) 
    # Add message from the sniffer to the window
    window.displayMessage(sniff.getMessage())
    # Set mainLoop to run again
    window.after(mainLoop)

# Wrapper for send function
def send():
    # Retrieve sending packet from gui
    packet = window.getSendingPacket()
    # Check packet is not empty
    if packet != '':
        sniff.sendPacket(window.getSendingPacket())

# Function to create new network
def newNetwork():
    global network
    network = objects.Network("1")
    window.drawNodes(network)
    
# Function to save network
def saveNetwork():
    print("Not yet implemented")
    
# Function to open network
def openNetwork():
    print("Not yet implemented")

if __name__ == '__main__':
    main()
