class BuryhoNode():
    def __init__(self, data):
        self.payload = data
        self.pointer = None
        
class BuryhoLinkedList():
    def __init__(self):
        self.data = set()
    
    def append(self, node):
        if len(self.data):
            ...