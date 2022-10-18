#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Author: Benjamin Sinclair
# Revision Date: 12/10/2022
# Name: objects.py
# 
# Contains object definitions used by iseebee
# ---------------------------------------------------------------------------

# Network class, contains list of node objects

class Network:
    def __init__(self, ID):
        # Initialise empty list of nodes 
        self.nodes = []
        self.ID =ID

    def __iter__(self):
        yield from self.nodes

    # Function to add node to list
    def addNode(self, node):
        self.nodes.append(node)
    
    # Return network ID
    def getID(self):
        return ID
    
    # Search for node by its ID
    def searchNode(self, ID):
        for node in self:
            if node.getID() == ID:
                return True
        return False

# Node class, for each source address
class Node:
    def __init__(self, ID, x, y):
        self.ID = ID
        self.x = x
        self.y = y
        
    def getID(self):
        return self.ID
        
    def setPos(self, x, y):
        pass
        self.x = x
        self.y = y
    
    def getPosx(self):
        return self.x
    
    def getPosy(self):
        return self.y
        

