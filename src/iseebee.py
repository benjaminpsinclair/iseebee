import zigbee
import gui
import objects
#import hue

def main():
    # Create gui window
    window = gui.Window('iseebee', '800x600')
    # Create sniffer object
    sniff = zigbee.Sniffer()
    # Create network
    network = objects.Network("1")
    while (True):
        # Read packets
        data = sniff.readPacket()
        if data != None:
            # Extract source
            window.displayMessage("Source: " + str(data[13:15]) + "\n")
            if network.searchNode(data[13:15]) == False: 
                network.addNode(objects.Node(data[13:15]))
        # Add message from the sniffer to the windows)
        #window.displayMessage(sniff.getMessage())
        # Update window
        window.drawNodes(network)
        window.update()
if __name__ == '__main__':
    main()
