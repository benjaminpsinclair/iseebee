# Gui for iseebee prototype
# TODO migrate to wxPython for accessibility functions

import tkinter as tk
from tkinter import scrolledtext, Menu, ttk
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
        # Create pop up menu manager
        self.pop = popManager(self.window, menuFunctions["send"])
        # Add main messagebox
        self.messageLabel = self.addMessageBox(30, 32)
        # Add raw messagebox
        self.messageRaw = scrolledtext.ScrolledText(self.window, width = 69, height = 11)
        #TODO replace place with pack
        self.messageRaw.place(x=865,y=385)
        # TODO setup widget function?
        # Create tree list
        self.packetList = listBox(packet_header, self.window)
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
        
        #TEMP
        #self.sendingPacket = bytes.fromhex('418865b478ffff7a970912fcff7a971ebfb608d1010188170028323d1200b608d1010188170000bfaa80ea88291fe6f0be58948f82d907ac6fea37')
        self.sendingPacket = bytes.fromhex('6188a0b4787b047a9748027b047a971eab286d411200b608d1010188170000d20e5947175c868c2cb3f7d50f70ac46c07bec')
        
    def displayMessage(self, message):
        # Make sure we're at the bottom before inserting
        self.messageLabel.see(tk.END)
        self.messageLabel.configure(state='normal')
        self.messageLabel.insert(tk.INSERT, message)
        self.messageLabel.configure(state='disabled')
        
    def displayPacket(self, packet):
        self.packetList._buildTree(packet)
    
    def displayRawMessage(self):
        raw = self.packetList.getRawMessage()
        if raw != '':
            self.messageRaw.configure(state='normal')
            self.messageRaw.delete('1.0', tk.END)
            self.messageRaw.insert(tk.INSERT, raw)
            self.messageRaw.configure(state='disabled')
            
    def getSendingPacket(self):
        return self.sendingPacket
   
    # Function to draw network on window
    def drawNodes(self, network):
        # Remove existing labels
        for label in self.labels:
            label.destroy() 
        # Redraw new labels
        for node in network:
            ID = str(node.getID())
            # Create node label
            label = tk.Label(self.window, text=ID, bg="red")
            # Add drag and drop function
            self.drag.addDragable(label, node)
            # Add popup menu
            self.pop.addPop(label, node)
            # Add to label list
            self.labels.append(label)
            # Place label on window
            xPos=node.getPosx()
            yPos=node.getPosy()
            #print(xPos)
            label.place(x = xPos, y = yPos)
            #label.place(x=150, y=350)
    
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
    def addDragable(self, widget, node):
        self.node = node
        widget.bind("<ButtonPress-1>", self.onStart)
        widget.bind("<B1-Motion>", self.onDrag)
        widget.bind("<ButtonRelease-1>", self.onDrop)
        widget.configure(cursor="hand2")
    
    def onStart(self, event):
        global originalX, originalY
        originalX, originalY = event.widget.winfo_pointerxy()
        
    def onDrag(self, event):
        pass
    
    #TODO keep object within viewport
    def onDrop(self, event):
        target = event.widget.winfo_containing(originalX, originalY)
        newX = event.x + event.widget.winfo_x()
        newY = event.y + event.widget.winfo_y()
        try:
            target.place(x = newX, y = newY)
            node.setPos(newX, newY)
        except:
            pass    

class popManager:
    #TODO pass functions for menu
    def __init__(self, window, sendFunc):
        # Create right click menu
        self.clickMenu = Menu(window,  tearoff = False)
        self.clickMenu.add_command(label = "Send", command=sendFunc)

    def addPop(self, widget, node):
        widget.bind("<Button-3>", self.popMenu)
        #widget.bind("<Button-1>", self.closeMenu)
    
    def popMenu(self, event):
        try:
            self.clickMenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.clickMenu.grab_release()
    
    def closeMenu(self, event):
        #TODO close menu if user clicks elsewhere
        pass
        
    def testSend(self):
        print("testsend")

# List class using treeview, based on stackexchange 5286093
class listBox:
    def __init__(self, header, window):
        # Initialise variables
        self.tree = None
        # Packet dictionary
        self.packets = {}
        # Packet contents
        self.updated = False
        self.rawMessage = ''
        
        self._setup(header, window)
        packet = None
        self._buildTree(packet)
        
    def _setup(self, header, window):
        self.tree = ttk.Treeview(window, columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        # TODO replace place with pack - remove magic numbers
        self.tree.place(x=260,y=375)
        # Bind click function
        self.tree.bind("<<TreeviewSelect>>", self.getPacket)
    
    def _buildTree(self, packet):
        for col in packet_header:
            self.tree.heading(col, text=col.title())
        if packet != None:
            item = packet.getInfo()
            ID = self.tree.insert('', 'end', values=item)
            #print(ID)
            self.packets[ID] = packet
    
    def getPacket(self, event):
        for item in self.tree.selection():
            self.updated = True
            #print(item)
            self.messageRaw = self.packets[item].getRaw()

    def getRawMessage(self):
        if self.updated == True:
            self.updated = False
            #print(self.messageRaw)
            return self.messageRaw
        else:
            return ''
        
            
    # TODO clickable and change packet contents to display in other widget
        
        
# Header for packet list tree
packet_header = ['Source', 'Destination', 'Sequence Number']
        

