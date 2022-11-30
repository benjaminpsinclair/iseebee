#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Author: Benjamin Sinclair
# Revision Date: 17/10/2022
# Name: gui.py
#
# ---------------------------------------------------------------------------
# Gui for iseebee prototype, using wxPython library for compatibility with
# screen reader tools for visual accessibility

import wx
import threading
import queue
import objects

# Window class
class Window:
    def __init__(self, title, geometry):
        # Convert geometry in format 'axb' to size tuple (a, b)
        size = tuple(map(int, geometry.split('x')))

        # Create window
        self.app = wx.App(False)
        self.window = wx.Frame(None, wx.ID_ANY, title=title, size=size)
        # Create panel
        self.panel = wx.Panel(self.window)

        # Add main messagebox
        self.messageLabel = wx.TextCtrl(self.panel, size=(300, 600), style=wx.TE_MULTILINE| wx.TE_READONLY, name="Message Box")

        # Add raw messagebox
        self.messageRaw = wx.TextCtrl(self.panel, size=(1440, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Add label for channel and packetBytes
        self.channelKeyLabel = wx.StaticText(self.panel, size=(100, 100), label="Channel: Key: ", pos=(0, 0))
        self.channelKeyLabel.SetForegroundColour((255,0,0))

        # Create tree list
        self.packetList = listBox(("Source", "Destination", "PAN"), self.panel, self.displayRawMessage)

        # Horizontal sizer for widgets
        horzSizer = wx.BoxSizer(wx.HORIZONTAL)
        horzSizer.Add(self.packetList.getWidget(), 0, wx.EXPAND)
        horzSizer.Add(self.messageRaw, 0, wx.EXPAND)

        # Vertical sizer for widgets
        vertSizer = wx.BoxSizer(wx.VERTICAL)
        vertSizer.Add(self.channelKeyLabel, 0, wx.EXPAND)
        vertSizer.Add(horzSizer, 0, wx.ALIGN_BOTTOM)


        # Horizontal sizer for widgets
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.messageLabel, 0, wx.ALIGN_BOTTOM)
        sizer.Add(vertSizer, 0, wx.ALIGN_BOTTOM)

        self.panel.SetSizer(sizer)
        self.panel.Layout()

        # Create list of labels for network and nodes
        self.labels = {}
        # Create network
        self.network = objects.Network("1")
        # Set variable for object being dragged currently
        self.dragged = None
        # Set variable for selected label
        self.selectedLabel = None
        # Queue for packets to be sent
        self.sendingPackets = queue.Queue()
        # Queue for Key
        self.key = queue.Queue()
        # Queue for channels
        self.channel = queue.Queue()
        # Queue for events
        self.events = queue.Queue()

        # Create file menu
        self.fileMenu = wx.Menu()
        menuNewNetwork = self.fileMenu.Append(wx.ID_ANY, "&New Network", " Create new network diagram")
        menuOpen = self.fileMenu.Append(wx.ID_OPEN, "&Open", " Open a network diagram")
        menuExit = self.fileMenu.Append(wx.ID_EXIT, "&Exit", " Exit the application")
        # Create edit menu
        self.editMenu = wx.Menu()
        menuKey = self.editMenu.Append(wx.ID_ANY, "&Key", "Edit key")
        menuChannel = self.editMenu.Append(wx.ID_ANY, "&Channel", "Set Channel")
        menuPreferences = self.editMenu.Append(wx.ID_PREFERENCES, "&Preferences", "Edit preferences")

        # Create view menu
        #self.viewMenu = Menu(self.menubar, tearoff=False)
        # Create scan menu
        self.scanMenu = wx.Menu()
        menuScanChannels = self.scanMenu.Append(wx.ID_ANY, "&Scan Channels", "Scan for channels")
        # Create menubar
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.fileMenu, "&File")
        self.menubar.Append(self.editMenu, "&Edit")
        self.menubar.Append(self.scanMenu, "&Scan")
        self.window.SetMenuBar(self.menubar)
        # Create right click menu
        self.clickMenu = wx.Menu()
        sendMenu = self.clickMenu.Append(-1, "Send Raw Data")
        sendEncMenu = self.clickMenu.Append(-1, "Send Encrypted Packet")
        renameMenu = self.clickMenu.Append(-1, "Rename")

        # Bindings for window
        self.window.Bind(wx.EVT_MENU, self.newNetwork, menuNewNetwork)
        self.window.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.window.Bind(wx.EVT_MENU, self.scanChannels, menuScanChannels)
        self.window.Bind(wx.EVT_MENU, self.editKey, menuKey)
        self.window.Bind(wx.EVT_MENU, self.setChannel, menuChannel)

        # Bindings for panel
        self.panel.Bind(wx.EVT_MOTION, self.onMove)
        # Bindings for popup menu
        self.clickMenu.Bind(wx.EVT_MENU, self.onSend, sendMenu)
        self.clickMenu.Bind(wx.EVT_MENU, self.onSendEnc, sendEncMenu)
        self.clickMenu.Bind(wx.EVT_MENU, self.onRename, renameMenu)

        self.window.Show(True)

    # Function to display message in message box
    def displayMessage(self, message):
        # Use threadsafe wx.CallAfter() to append text to message label
        wx.CallAfter(self.messageLabel.AppendText, message)

    # Threadsafe function for displaying packet
    def displayPacket(self, packet):
        wx.CallAfter(self.packetList._buildTree, packet)

    # Threadsafe function for displaying the raw packet data
    def displayRawMessage(self, message):
        wx.CallAfter(self.messageRaw.SetValue, message)

    # Threadsafe function for adding a node
    def addNode(self, node):
        wx.CallAfter(self.drawNode, node)

    # Threadsafe function for displaying channel and Key
    def updateChannelKey(self, channel, key):
        wx.CallAfter(self.channelKeyLabel.SetLabel,"Channel: " + str(channel) + "\nKey: " + key)

    # Threadsafe function for drawing line
    def connection(self, source, dest):
        wx.CallAfter(self.drawLine, source, dest)

    def drawLine(self, source, dest):
        # Check if nodes exist
        if self.network.searchNode(source) == True:
            if self.network.searchNode(dest) == True:
                dc = wx.PaintDC(self.window)
                dc.DrawLine(0, 0, labels[source], labels[dest])
    # Function to draw network on panel
    def drawNode(self, source):
        if self.network.searchNode(source) == False:
            node = objects.Node(source, 700, 150)
            # Add node to network
            self.network.addNode(node)
            # Set node name to address
            name = "0x" + str(node.getID())
            # Get x and y position
            xPos = node.getPosx()
            yPos = node.getPosy()
            # Create node label
            label = wx.StaticText(self.panel, label=name, pos=(xPos, yPos))
            # Attach node
            label.node = node
            # Add drag and drop function
            label.Bind(wx.EVT_LEFT_DOWN, self.onClick)
            # Add right click menu
            label.Bind(wx.EVT_RIGHT_DOWN, self.popMenu)
            # Add to label list
            self.labels[source] = label

    # Function for starting gui and mainloop function on separate threads
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

    # Function called when exit is clicked
    def onExit(self, event):
        # Set running as false
        self.running.clear()
        # Close window
        self.window.Close(True)

    # Function called when scan channels is clicked
    def scanChannels(self, event):
        event.name = "scanning"
        self.events.put(event)

    # Function to edit Key
    def editKey(self, event):
        w,h = self.window.GetSize()
        # Create dialog box
        popup = wx.PopupTransientWindow(self.panel, flags=wx.BORDER_DOUBLE)
        popup.Position((100,100), (0,0))
        popup.SetSize((450,150))
        # Create textbox
        textBox = wx.TextCtrl(popup, size=(250, 100), style=wx.TE_MULTILINE)
        # Create OK button
        buttonOK = wx.Button(popup, size=(100,100), label = "OK")
        buttonOK.text = textBox
        buttonOK.Bind(wx.EVT_BUTTON, self.changeKey)
        # Create cancel button
        buttonCancel = wx.Button(popup, size=(100,100), label = "Cancel")
        buttonCancel.Bind(wx.EVT_BUTTON, self.onCancel)
        # Sizer to arrange elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(textBox, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonOK, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonCancel, 0, wx.ALIGN_BOTTOM)
        popup.SetSizer(sizer)
        popup.Layout()
        # Create popup
        popup.Popup(focus=None)

    # Function to set channel
    def setChannel(self, event):
        # Channel list
        channels = [str(x) for x in range(11,26)]
        # Create dialog box
        popup = wx.PopupTransientWindow(self.panel, flags=wx.BORDER_DOUBLE)
        popup.Position((100,100), (0,0))
        popup.SetSize((450,40))
        # Create textbox
        comboBox = wx.ComboBox(popup, size=(250, 100), choices = channels, value = "11", style=wx.CB_READONLY)
        # Create OK button
        buttonOK = wx.Button(popup, size=(100,100), label = "OK")
        buttonOK.text = comboBox
        print(buttonOK.text)
        buttonOK.Bind(wx.EVT_BUTTON, self.changeChannel)
        # Create cancel button
        buttonCancel = wx.Button(popup, size=(100,100), label = "Cancel")
        buttonCancel.Bind(wx.EVT_BUTTON, self.onCancel)
        # Sizer to arrange elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(comboBox, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonOK, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonCancel, 0, wx.ALIGN_BOTTOM)
        popup.SetSizer(sizer)
        popup.Layout()
        # Create popup
        popup.Popup(focus=None)

    def changeKey(self, event):
        self.key.put(event.GetEventObject().text.GetValue())
        self.onCancel(event)

    def changeChannel(self, event):
        self.newNetwork(event)
        self.channel.put(int(event.GetEventObject().text.GetValue()))
        self.onCancel(event)

    # Function called when mouse is moved
    def onMove(self, event):
        x = event.GetX()
        y = event.GetY()
        if self.dragged != None and event.LeftIsDown():
            self.dragged.SetPosition(wx.Point(x,y))
        else:
            self.dragged = None

    # Function to initiate dragging of object
    def onClick(self, event):
        self.dragged = event.GetEventObject()

    # Function to create pop up menu on right click
    def popMenu(self, event):
        self.selectedLabel = event.GetEventObject()
        x = event.GetX()
        y = event.GetY()
        event.GetEventObject().PopupMenu(self.clickMenu, wx.Point(x,y))

    # Function to create new network
    def newNetwork(self, event):
        # Reset network list
        self.network = objects.Network("1")
        # Destroy labels
        for label in self.labels.values():
            label.Destroy()
        self.labels = {}

    # Function to save network
    def saveNetwork():
        print("Not yet implemented")

    # Function to open network
    def openNetwork():
        print("Not yet implemented")

    # Take send message input
    # TODO refactor to transientwindow class rather than in function
    def onSend(self, event):
        # Get position and width,height
        x,y = self.selectedLabel.Position
        w,h = self.selectedLabel.GetSize()
        # Create sending dialog box
        popup = wx.PopupTransientWindow(self.panel, flags=wx.BORDER_DOUBLE)
        popup.Position((x,y), (w,h))
        popup.SetSize((450,150))
        # Create textbox
        textBox = wx.TextCtrl(popup, size=(250, 100), style=wx.TE_MULTILINE)
        # Create send button
        buttonSend = wx.Button(popup, size=(100,100), label = "Send")
        buttonSend.text = textBox
        buttonSend.encrypt = False
        buttonSend.label = self.selectedLabel
        buttonSend.Bind(wx.EVT_BUTTON, self.send)
        # Create cancel button
        buttonCancel = wx.Button(popup, size=(100,100), label = "Cancel")
        buttonCancel.Bind(wx.EVT_BUTTON, self.onCancel)
        # Sizer to arrange elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(textBox, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonSend, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonCancel, 0, wx.ALIGN_BOTTOM)
        popup.SetSizer(sizer)
        popup.Layout()
        # Create popup
        popup.Popup(focus=None)
        self.selectedLabel = None

    # Add sending packet to threadsafe queue
    def send(self, event):
        self.sendingPackets.put(event.GetEventObject().text.GetValue())
        self.onCancel(event)

    def onSendEnc(self, event):
        # Get position and width,height
        x,y = self.selectedLabel.Position
        w,h = self.selectedLabel.GetSize()
        # Create sending dialog box
        popup = wx.PopupTransientWindow(self.panel, flags=wx.BORDER_DOUBLE)
        popup.Position((x,y), (w,h))
        popup.SetSize((450,150))
        # Create textbox
        textBox = wx.TextCtrl(popup, size=(250, 100), style=wx.TE_MULTILINE)
        # Create send button
        buttonSend = wx.Button(popup, size=(100,100), label = "Send")
        buttonSend.text = textBox
        buttonSend.encrypt = True
        buttonSend.label = self.selectedLabel
        buttonSend.Bind(wx.EVT_BUTTON, self.send)
        # Create cancel button
        buttonCancel = wx.Button(popup, size=(100,100), label = "Cancel")
        buttonCancel.Bind(wx.EVT_BUTTON, self.onCancel)
        # Sizer to arrange elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(textBox, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonSend, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonCancel, 0, wx.ALIGN_BOTTOM)
        popup.SetSizer(sizer)
        popup.Layout()
        # Create popup
        popup.Popup(focus=None)
        self.selectedLabel = None

    # Add sending packet to threadsafe queue
    def send(self, event):
        self.sendingPackets.put(event.GetEventObject())
        self.onCancel(event)

    # Function When cancel button is clicked
    def onCancel(self, event):
        # Get button that called, get parent window and dismiss
        event.GetEventObject().GetParent().Dismiss()

    # Rename node label dialogue box
    def onRename(self, event):
        # Get position and width,height
        x,y = self.selectedLabel.Position
        w,h = self.selectedLabel.GetSize()
        # Create sending dialog box
        popup = wx.PopupTransientWindow(self.panel, flags=wx.BORDER_DOUBLE)
        popup.Position((x,y), (w,h))
        popup.SetSize((450,150))
        # Create textbox
        textBox = wx.TextCtrl(popup, size=(250, 100), style=wx.TE_MULTILINE)
        # Create send button
        buttonRename = wx.Button(popup, size=(100,100), label = "Rename")
        buttonRename.label = self.selectedLabel
        buttonRename.text = textBox
        buttonRename.Bind(wx.EVT_BUTTON, self.rename)
        # Create cancel button
        buttonCancel = wx.Button(popup, size=(100,100), label = "Cancel")
        buttonCancel.Bind(wx.EVT_BUTTON, self.onCancel)
        # Sizer to arrange elements
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(textBox, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonRename, 0, wx.ALIGN_BOTTOM)
        sizer.Add(buttonCancel, 0, wx.ALIGN_BOTTOM)
        popup.SetSizer(sizer)
        popup.Layout()
        # Create popup
        popup.Popup(focus=None)
        self.selectedLabel = None

    # Rename label
    def rename(self, event):
        event.GetEventObject().label.SetLabel(event.GetEventObject().text.GetValue())
        self.onCancel(event)

# List class using treeview, based on stackexchange 5286093
class listBox:
    def __init__(self, header, panel, displayFunction):
        # Initialise variables
        self.tree = None
        # Packet list
        self.packets = []
        # Packet contents
        self.updated = False
        self.messageRaw = ''
        self.displayFunction  = displayFunction
        # Create tree
        self.tree = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
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

    # Build the columns for the list
    def _buildTree(self, packet):
        if packet != None:
            item = packet.getInfo()
            ID = self.tree.InsertItem(0, "0x" + str(item['source']))
            self.tree.SetItem(ID, 1, "0x" + str(item['dest']))
            self.tree.SetItem(ID, 2, "0x" + str(item['pan']))
            self.packets.insert(0, packet)

    # Function to get the packet that has been clicked on
    def getPacket(self):
        item = self.tree.GetFocusedItem()
        if item != -1:
            self.updated = True
            self.messageRaw = self.packets[item].getRaw()

    # Function to get the text from the packet that was clicked on
    def getRawMessage(self):
        if self.updated == True:
            self.updated = False
            return self.messageRaw
        else:
            return ''

    # Function to get the widget
    def getWidget(self):
        return self.tree

    # Function to call when user clicks on packet entry
    def onClick(self, event):
        self.getPacket()
        self.displayFunction(self.messageRaw)
