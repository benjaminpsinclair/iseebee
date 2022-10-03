import tkinter as tk
from tkinter import scrolledtext, Menu
import objects

# Window class
class Window:
    def __init__(self, title, geometry, menuFunctions):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(geometry) 
        # Add main messagebox
        self.messageLabel = self.addMessageBox(25, 30)
        # Create list of labels for network and nodes
        self.labels = []
        # Create menubar
        self.menubar = Menu(self.window, tearoff=False)
        self.window.config(menu=self.menubar)
        # Create file menu
        self.fileMenu = Menu(self.menubar, tearoff=False)
        self.fileMenu.add_command(label='New Network', command=menuFunctions["newNetwork"])
        self.fileMenu.add_command(label='Exit', command=self.window.destroy)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        # Add bottom frame 
        #self.packetFrame = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=1)
        
    def displayMessage(self, message):
        # Make sure we're at the bottom before inserting
        self.messageLabel.see(tk.END)
        self.messageLabel.configure(state='normal')
        self.messageLabel.insert(tk.INSERT, message)
        self.messageLabel.configure(state='disabled')
   
    # Function to draw network  
    def drawNodes(self, network):
        # Check if the network has changed since last drawing
        if network.pendingUpdate() == True:
            print("Drawing update")
            # Remove labels
            for label in self.labels:
                label.destroy()
            network.setUpdated()
            i = 1
            for node in network:
                ID = str(node.getID())
                # Create node label
                label = tk.Label(self.window, text=ID, bg="red")
                # Add to label list
                self.labels.append(label)
                # Place label on window
                label.place(x=(i*350), y=20)
                i = i + 1
                
    def addMessageBox(self, x, y):
        label = scrolledtext.ScrolledText(self.window, width = x, height = y)
        label.pack(side=tk.LEFT)
        return label
        
    def start(self, function):
        self.window.after(1, function)
        self.window.mainloop()
        
    def after(self, function):
        self.window.after(1, function)
        
        
#TODO update text box function 
