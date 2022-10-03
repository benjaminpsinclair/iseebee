import zigbee
import gui
import objects
#import hue

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
        "saveNetwork": saveNetwork
    }
    window = gui.Window('iseebee', '1440x600', menuFunctions)
    # Start gui thread
    window.start(mainLoop)
        
def mainLoop():
    # Read packets
    data = sniff.readPacket()
    if data != None:
        # Add data to packet
        packet = zigbee.Packet(data)
        # Add packet to window
        window.displayPacket(packet)
        packets.append(packet)
        window.displayMessage("Packet received, Source: " + str(data[13:15]) + '\n')
        if network.searchNode(data[13:15]) == False: 
            network.addNode(objects.Node(data[13:15]))
    # Add message from the sniffer to the window
    window.displayMessage(sniff.getMessage())
    # Display raw message box contents
    window.displayRawMessage()
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
