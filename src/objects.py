class Network:
    def __init__(self, ID):
        self.nodes = []
        self.ID =ID
        #self.index = 0
        self.updated = True

    def __iter__(self):
        yield from self.nodes

    def addNode(self, node):
        print("Node added:" + str(node.getID()))
        self.nodes.append(node)
        self.updated = True
        
    def getID(self):
        return ID
        
    def searchNode(self, ID):
        for node in self:
            if node.getID() == ID:
                return True
        return False
    
    def pendingUpdate(self):
        return self.updated

    def setUpdated(self):
        self.updated =  False

class Node:
    def __init__(self, ID):
        self.ID = ID

    def getID(self):
        return self.ID

