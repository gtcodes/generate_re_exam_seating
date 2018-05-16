from room import Room

class ListRoom(Room):

    def __init__(self, name, col, row):
        super().__init__(name, col, row)

    def createSeating(self, students):
        print("Room " + self.name + " has " + str(len(students)) + " students")
        seating = ''
        for s in students:
            seating += "\\item " + s.name + '\n'
        return(seating)
    
    def getPaperSize(self):
        return ('A4')
    
    def latexHeader(self):
        
        with open ("src/latex/listRoom/studentHeader.tex") as texFile:
            return texFile.read()

    def latexFooter(self):
        with open ("src/latex/listRoom/studentFooter.tex") as texFile:
            return texFile.read()

