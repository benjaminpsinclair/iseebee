import tkinter as tk
from tkinter import scrolledtext
import objects

# Window class
class Window:
    def __init__(self, title, geometry):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(geometry) 
        # Add main messagebox
        self.messageLabel = self.addMessageBox(25, 30)
        # Add bottom label
        self.packetLabel = self.addMessageBox(20, 20)

    def displayMessage(self, message):
        # Make sure we're at the bottom before inserting
        self.messageLabel.see(tk.END)
        self.messageLabel.configure(state='normal')
        self.messageLabel.insert(tk.INSERT, message)
        self.messageLabel.configure(state='disabled')
        # Scroll to the bottom
        self.messageLabel.see(tk.END)
   
    # Function to draw network  
    def drawNodes(self, network):
        # Check if the network has changed since last drawing
        if network.pendingUpdate() == True:
            network.setUpdated()
            i = 1
            for node in network:
                ID = str(node.getID())
                # Create node label
                label = tk.Label(self.window, text=ID, bg="red")
                # Add to list of labels
                self.ldabels.append(label)
                # Place label on window
                label.place(x=(i*350), y=20)
                i = i + 1
                
    def addMessageBox(self, x, y):
        label = scrolledtext.ScrolledText(self.window, width = x, height = y)
        return label
    
    def drawMessageBoxes(self):
        self.messageLabel.grid(row=0, column=0)
        self.messageLabel.pack(side=tk.LEFT)
        
    def update(self):
        self.drawMessageBoxes()
        self.window.update_idletasks()
        #self.window.update()

#class MessageBox:
#    def ___init___(self, window):
#        window.messageLabel = scrolledtext.ScrolledText(self.window, width = 25, height = 30)
#        window.messageLabel.grid(row=0, column=0)
#        window.messageLabel.pack(side=tk.LEFT)
#        # Disable input
#        window.messageLabel.configure(state='disabled')
        # TODO make text unclickable 
        
        
#TODO update text box function 
