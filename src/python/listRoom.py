from room import Room
from printerInfoWriter import PrinterInfoWriter
class ListRoom(Room):
    
    def __init__(self, name, col, row):
        super().__init__(name, col, row)
        self.texDir = "src/latex/listRoom/"
        self.printerInfoWriter = PrinterInfoWriter()

    def createSeating(self, students, planName):
        print("Room " + self.name + " has " + str(len(students)) + " students")
        seating = ''
        for s in students:
            seating += "\\item " + s.name + '\n'
        self.printerInfoWriter.displayInfo(planName + ";" + "A4" + ";" + "studentPlan")
        return(seating)

    def createAdminPlan(self, students, planName):
        seating=''
        for s in students:
            seating += s.name + "&" + s.getTestTime() + '\\\\\n'
        self.printerInfoWriter.displayInfo(planName + ";" + self.getPaperSize() + ";" + "teacherPlan")
        return(seating)
    
    def getPaperSize(self):
        return ('A4')
    
    def latexHeader(self):
        with open (self.texDir + "studentHeader.tex") as texFile:
            return texFile.read()

    def latexFooter(self):
        with open (self.texDir + "studentFooter.tex") as texFile:
            return texFile.read()
    
    def adminLatexHeader(self):
        with open (self.texDir + "adminHeader.tex") as texFile:
            return texFile.read()

    def adminLatexFooter(self):
        with open (self.texDir + "adminFooter.tex") as texFile:
            return texFile.read()
    
