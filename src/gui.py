# Gui for iseebee prototype
# TODO migrate to wxPython for accessibility functions

import tkinter as tk
from tkinter import scrolledtext, Menu, ttk
import wx
import threading
import objects

# Window class
class Window:
    def __init__(self, title, geometry, menuFunctions):
        # Convert geometry in format 'axb' to size tuple (a, b)
        size = tuple(map(int, geometry.split('x')))
        
        # Create window 
        self.app = wx.App(False)
        self.window = wx.Frame(None, wx.ID_ANY, title=title, size=size)
 
        #self.window.resizable(False, False)
        # Create drag manager
        #self.drag = dragManager()
        # Create pop up menu manager
        #self.pop = popManager(self.window, menuFunctions["send"])
        
        # Add main messagebox
        self.messageLabel = wx.TextCtrl(self.window, size=(300, 600), style=wx.TE_MULTILINE| wx.TE_READONLY)
        
        # Add raw messagebox
        self.messageRaw = wx.TextCtrl(self.window, size=(1440, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)
        
        # Create tree list
        #self.packetList = wx.ListCtrl(self.window, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.packetList = listBox(("Source", "Destination", "Sequence Number"), self.window, self.displayRawMessage)

        # Horizontal sizer for widgets
        horzSizer = wx.BoxSizer(wx.HORIZONTAL)
        horzSizer.Add(self.packetList.getWidget(), 0, wx.EXPAND)
        horzSizer.Add(self.messageRaw, 0, wx.EXPAND)
        
        # Vertical sizer for widgets
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.messageLabel, 0, wx.ALIGN_BOTTOM)
        sizer.Add(horzSizer, 0, wx.ALIGN_BOTTOM)        
 
        self.window.SetSizer(sizer)
        self.window.Layout()
        
        # Create list of labels for network and nodes
        self.labels = []

        # Create file menu
        self.fileMenu = wx.Menu()
        menuNewNetwork = self.fileMenu.Append(wx.ID_ANY, "&New Network", " Create new network diagram")
        menuOpen = self.fileMenu.Append(wx.ID_OPEN, "&Open", " Open a network diagram")
        menuExit = self.fileMenu.Append(wx.ID_EXIT, "&Exit", " Exit the application")
        # Create edit menu
        #self.editMenu = Menu(self.menubar, tearoff=False)
        #self.editMenu.add_command(label='Preferences')
        #self.menubar.add_cascade(label="Edit", menu=self.editMenu)
        # Create view menu
        #self.viewMenu = Menu(self.menubar, tearoff=False)
        # Create scan menu
        #self.scanMenu = Menu(self.menubar, tearoff=False)
        #self.scanMenu.add_command(label='Scan Network')
        #self.menubar.add_cascade(label="Scan", menu=self.scanMenu)
        # Create menubar
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.fileMenu, "&File")
        self.window.SetMenuBar(self.menubar)
        
        # Bindings
        self.window.Bind(wx.EVT_MENU, self.onExit, menuExit)

        self.window.Show(True)
        #TEMP
        #self.sendingPacket = bytes.fromhex('418865b478ffff7a970912fcff7a971ebfb608d1010188170028323d1200b608d1010188170000bfaa80ea88291fe6f0be58948f82d907ac6fea37')
        
        self.sendingPacket = bytes.fromhex('6188a0b4787b047a9748027b047a971eab286d411200b608d1010188170000d20e5947175c868c2cb3f7d50f70ac46c07bec')
    
    # Function to display message in message box
    def displayMessage(self, message):
        # Use threadsafe wx.CallAfter() to append text to message label
        wx.CallAfter(self.messageLabel.AppendText, message)
        
    def displayPacket(self, packet):
        wx.CallAfter(self.packetList._buildTree, packet)
    
    def displayRawMessage(self, message):
        wx.CallAfter(self.messageRaw.SetValue, message)
            
    def getSendingPacket(self):
        return self.sendingPacket
    
    def drawNodes(self, network):
        wx.CallAfter(self.drawNetwork, network)
   
    # Function to draw network on window
    def drawNetwork(self, network):
        # Remove existing labels
        for label in self.labels:
            label.Destroy()
        # Redraw new labels
        for node in network:
            ID = str(node.getID())
            # Place label on window
            xPos=node.getPosx()
            yPos=node.getPosy()
            # Create node label
            label = wx.StaticText(self.window, label=ID, pos=(xPos, yPos))
            # Add drag and drop function
            #self.drag.addDragable(label, node)
            # Add popup menu
            #self.pop.addPop(label, node)
            # Add to label list
            self.labels.append(label)
            #print(xPos)
        
    def start(self, function):
        # Track if application is still supposed to be running
        self.running = threading.Event()
        self.running.set()
        # Create thread for gui
        t = threading.Thread(target=self.app.MainLoop)
        t.start()
        # Run main function
        while(self.running.is_set()):
            function()

    # This is not required for wxPython implimentation
    def after(self, function):
        pass
        
    def onExit(self, event):
        # Set running as false
        self.running.clear()
        # Close window
        self.window.Close(True)
        
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
    def __init__(self, header, window, displayFunction):
        # Initialise variables
        self.tree = None
        # Packet list
        self.packets = []
        # Packet contents
        self.updated = False
        self.messageRaw = ''
        self.displayFunction  = displayFunction
        # Create tree
        self.tree = wx.ListCtrl(window, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        # Binding
        self.tree.Bind(wx.EVT_LEFT_UP, self.onClick)
        packet = None
        # Build Columns
        for idx, columnName in enumerate(header):
            self.tree.InsertColumn(idx, columnName)
        # Set column widths
        self.tree.SetColumnWidth(0, 100)
        self.tree.SetColumnWidth(1, 100)
        self.tree.SetColumnWidth(2, 150)
        # Bind click function
        #self.tree.bind("<<TreeviewSelect>>", self.getPacket)
        self._buildTree(packet)
    
    def _buildTree(self, packet):
        if packet != None:
            item = packet.getInfo()
            ID = self.tree.InsertItem(0, str(item[0]))
            self.tree.SetItem(ID, 1, str(item[1]))
            self.tree.SetItem(ID, 2, str(item[2]))
            self.packets.insert(0, packet)
    
    def getPacket(self):
        item = self.tree.GetFocusedItem()
        if item != -1:
            self.updated = True
            print(item)
            self.messageRaw = self.packets[item].getRaw()

    def getRawMessage(self):
        if self.updated == True:
            self.updated = False
            return self.messageRaw
        else:
            return ''
            
    def getWidget(self):
        return self.tree
            
    def onClick(self, event):
        self.getPacket()
        self.displayFunction(self.messageRaw)
        

