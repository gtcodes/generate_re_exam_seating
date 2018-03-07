class Room:
        
    def __init__(self, name, col, row):
        self.name=name
        self.col=col
        self.row=row
    
    def optNumberOfPeople(self):
        return self.row*self.col

    def maxNumberOfPeople(self):
        return (2*self.optNumberOfPeople())
