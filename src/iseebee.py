import zigbee
import gui
import objects
from threading import Thread
#import hue

def main():
    # Declare global variables
    global window, sniff, network
    # Create sniffer object
    sniff = zigbee.Sniffer()
    # Create network
    network = objects.Network("1")
    # Create window
    # Add menufunctions into dictionary
    menuFunctions = {
        "newNetwork": newNetwork,
        "openNetwork": openNetwork,
        "saveNetwork": saveNetwork
    }
    window = gui.Window('iseebee', '800x600', menuFunctions)
    # Start gui thread
    window.start(mainLoop)
        
def mainLoop():
    # Read packets
    data = sniff.readPacket()
    if data != None:
        # Extract source
        window.displayMessage("Source: " + str(data[13:15]) + "\n")
        if network.searchNode(data[13:15]) == False: 
            network.addNode(objects.Node(data[13:15]))
    # Add message from the sniffer to the windows)
    window.displayMessage(sniff.getMessage())
    window.drawNodes(network)   
    # Set mainLoop to run again
    window.after(mainLoop)

# Function to create new network
def newNetwork():
    global network
    network = objects.Network("1")
    
# Function to save network
def saveNetwork():
    print("Not yet implemented")
    
# Function to open network
def openNetwork():
    print("Not yet implemented")

if __name__ == '__main__':
    main()
