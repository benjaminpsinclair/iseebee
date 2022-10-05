class Network:
    def __init__(self, ID):
        self.nodes = []
        self.ID =ID

    def __iter__(self):
        yield from self.nodes

    def addNode(self, node):
        print("Node added:" + str(node.getID()))
        self.nodes.append(node)
        
    def getID(self):
        return ID
        
    def searchNode(self, ID):
        for node in self:
            if node.getID() == ID:
                return True
        return False
        
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
        

