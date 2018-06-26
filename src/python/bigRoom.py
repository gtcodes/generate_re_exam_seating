from room import Room
from person import Person
from printerInfoWriter import PrinterInfoWriter
import math

class BigRoom(Room):
    
    tableWidth = 5.4
    tableHeight = 2.5
    tableSpacing = 1

    def __init__(self, name, col, row, seatingOffs):
        super().__init__(name, col, row)
        self.seatingOffs = seatingOffs
        self.printerInfoWriter=PrinterInfoWriter()

    def getPaperSize(self):
        return('A3')

    def createSeating(self, students, planName):
        self.printerInfoWriter.displayInfo(planName + ";" + self.getPaperSize() + ";" + "adminPlan")
        return(self.generateLatexCodeForSeating(students, False))

    def createAdminPlan(self, students, planName):
        self.printerInfoWriter.displayInfo(planName + ";" + self.getPaperSize() + ";" + "studentPlan")
        return(self.generateLatexCodeForSeating(students, True))

    def generateLatexCodeForSeating(self, students, includeTimes):
        print("Room " + self.name + " has " + str(len(students)) + " students")
        colsNeeded = math.floor(len(students) / self.rows)
        if(colsNeeded > 2 * self.cols):
            raise ValueError('Too many students assigned to room ' + self.name)
        numberOfDoubleCols = 0
        studentsInLastCol = 0
        if(colsNeeded > self.cols):
            numberOfDoubleCols = colsNeeded % self.cols
            studentsInLastCol = len(students) % self.rows
        currentStudent = 0
        tableCode = ''
        for col in range(0,self.cols):
            for row in range(0,self.rows):
                if(currentStudent == len(students)):
                    tableCode += self.drawBlankTable(row,col)
                    continue
                if(col < numberOfDoubleCols or (col == numberOfDoubleCols and row < studentsInLastCol)):
                    tableCode += self.splitTable(row, col, students[currentStudent], students[currentStudent + 1])
                    currentStudent += 2
                    if(includeTimes):
                        tableCode += self.timeUnderSplitTable(row, col, students[currentStudent], students[currentStudent + 1])
                else:
                    tableCode += self.wholeTable(row, col, students[currentStudent])
                    if(includeTimes):
                        tableCode += self.timeUnderWholeTable(row, col, students[currentStudent])
                    currentStudent += 1
        return tableCode

    def drawBlankTable(self, row, col):
        return(self.wholeTable(row,col,Person("","",False)))
    
    def getWidthOffs(self, col):
        return col * (self.tableWidth + self.tableSpacing) + self.seatingOffs

    def getHeightOffs(self, row):
        return row * (- self.tableHeight - self.tableSpacing) - self.seatingOffs

    def wholeTable(self, row, col, student):
        widthOffs = self.getWidthOffs(col) + self.tableWidth/4 #divide by 4, half of a half table
        heightOffs = self.getHeightOffs(row)
        return self.createTable(self.tableWidth, self.tableHeight, widthOffs, heightOffs, student.name)
    
    def timeUnderWholeTable(self,row,col,student1):
        widthOffs = self.getWidthOffs(col) + self.tableHeight/2
        heightOffs = self.getHeightOffs(row) - self.tableHeight/2 - 0.2
        return self.createTimeNode(widthOffs, heightOffs, student1.testTime)

    def splitTable(self, row, col, student1, student2):
        widthOffs = self.getWidthOffs(col)
        heightOffs = self.getHeightOffs(row)
        returnString = self.createTable(self.tableWidth/2, self.tableHeight, widthOffs, heightOffs, student1.name)
        returnString += self.createTable(self.tableWidth/2, self.tableHeight, widthOffs + self.tableWidth/2, heightOffs, student2.name)
        return returnString
    
    def timeUnderSplitTable(self, row, col, student1, student2):
        widthOffs = self.getWidthOffs(col)
        heightOffs = self.getHeightOffs(row) - self.tableHeight/2 - 0.2
        returnString = self.createTimeNode(widthOffs, heightOffs, student1.testTime)
        returnString += self.createTimeNode(widthOffs + self.tableWidth/2, heightOffs, student2.testTime)
        return returnString
    
    def createTimeNode(self, widthOffs, heightOffs, time):
        return '\n\\node[ anchor=base] at(' + str(widthOffs)+ ',' + str(heightOffs) + ') {'+ str(time) + '};'

    def createTable(self, width, height, widthOffs, heightOffs, name):
        return '\n\\node [draw, minimum width=' + str(width) + 'cm, minimum height='+ str(height) + 'cm, anchor=base] at(' + str(widthOffs) + ',' + str(heightOffs) + ') {\\begin{varwidth}{' + str(width-0.5) + 'cm}' + '\large ' + name + '\\end{varwidth}};'
    
    def latexHeader(self):
        with open ("src/latex/bigRoom/studentHeader.tex") as texFile:
            return texFile.read()

    def latexFooter(self):
        with open ("src/latex/bigRoom/studentFooter.tex") as texFile:
            return texFile.read()
    
    def adminLatexHeader(self):
        with open ("src/latex/bigRoom/adminHeader.tex") as texFile:
            return texFile.read()

    def adminLatexFooter(self):
        with open ("src/latex/bigRoom/adminFooter.tex") as texFile:
            return texFile.read()
