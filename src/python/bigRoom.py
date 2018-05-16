from room import Room
import math

class BigRoom(Room):
    
    tableWidth = 5.4
    tableHeight = 2.5
    
    def __init__(self, name, col, row, seatingOffs):
        super().__init__(name, col, row)
        self.seatingOffs = seatingOffs


    def getPaperSize(self):
        return('A3')

    def createSeating(self, students):
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
                if(col < numberOfDoubleCols or (col == numberOfDoubleCols and row < studentsInLastCol)):
                    tableCode += self.splitTable(row, col, students[currentStudent], students[currentStudent + 1])
                    currentStudent += 2
                else:
                    tableCode += self.wholeTable(row, col, students[currentStudent])
                    currentStudent += 1
                if(currentStudent == len(students)):
                    return tableCode
    
    def wholeTable(self, row, col, student):
        widthOffs = col * (self.tableWidth + 1) + (self.tableWidth/4) + self.seatingOffs #divide by 4, half of a half table
        heightOffs = row * (- self.tableHeight - 1) - self.seatingOffs
        return self.createTable(self.tableWidth, self.tableHeight, widthOffs, heightOffs, student.name)

    def splitTable(self, row, col, student1, student2):
        widthOffs = col * (self.tableWidth + 1) + self.seatingOffs 
        heightOffs = row * (- self.tableHeight - 1) - self.seatingOffs
        returnString = self.createTable(self.tableWidth/2, self.tableHeight, widthOffs, heightOffs, student1.name)
        returnString += self.createTable(self.tableWidth/2, self.tableHeight, widthOffs + self.tableWidth/2, heightOffs, student2.name)
        return returnString

    def createTable(self, width, height, widthOffs, heightOffs, name):
        return '\n\\node [draw, minimum width=' + str(width) + 'cm, minimum height='+ str(height) + 'cm, anchor=base] at(' + str(widthOffs) + ',' + str(heightOffs) + ') {\\begin{varwidth}{' + str(width-0.5) + 'cm}' + '\large ' + name + '\\end{varwidth}};'
    

    def latexHeader(self):
        with open ("src/latex/bigRoom/studentHeader.tex") as texFile:
            return texFile.read()

    def latexFooter(self):
        with open ("src/latex/bigRoom/studentFooter.tex") as texFile:
            return texFile.read()
