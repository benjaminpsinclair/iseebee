import tkinter as tk
from tkinter import scrolledtext, Menu
import objects

# Window class
class Window:
    def __init__(self, title, geometry, menuFunctions):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(geometry) 
        self.window.resizable(False, False)
        # Create drag manager
        self.drag = dragManager()
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
        self.fileMenu.add_command(label='Open', command=menuFunctions["openNetwork"])
        self.fileMenu.add_command(label='Save', command=menuFunctions["saveNetwork"])
        self.fileMenu.add_command(label='Exit', command=self.window.destroy)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        # Create edit menu
        self.editMenu = Menu(self.menubar, tearoff=False)
        self.editMenu.add_command(label='Preferences')
        self.menubar.add_cascade(label="Edit", menu=self.editMenu)
        # Create view menu
        self.viewMenu = Menu(self.menubar, tearoff=False)
        # Create scan menu
        self.scanMenu = Menu(self.menubar, tearoff=False)
        self.scanMenu.add_command(label='Scan Network')
        self.menubar.add_cascade(label="Scan", menu=self.scanMenu)
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
                # Add drag and drop function
                self.drag.addDragable(label)
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

# Class to provide drag and drop functionality to labels
# Code based on stackoverflow 44887576           
class dragManager:
    def addDragable(self, widget):
        widget.bind("<ButtonPress-1>", self.onStart)
        widget.bind("<B1-Motion>", self.onDrag)
        widget.bind("<ButtonRelease-1>", self.onDrop)
        widget.configure(cursor="hand2")
    
    def onStart(self, event):
        global originalX, originalY
        originalX, originalY = event.widget.winfo_pointerxy()
        
    def onDrag(self, event):
        pass
        
    def onDrop(self, event):
        target = event.widget.winfo_containing(originalX, originalY)
        newX = event.x + event.widget.winfo_x()
        newY = event.y + event.widget.winfo_y()
        try:
            target.place(x = newX, y = newY)
            print("Release")
            print(newX)
            print(newY)
        except:
            pass    

        
#TODO update text box function 
