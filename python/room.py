from abc import ABC, abstractmethod
import math

class Room():
        
    tableWidth = 3
    tableHeight = 1.5

    def __init__(self, name, col, row):
        self.name=name
        self.cols=col
        self.rows=row
        self.students=[]
    
    def optNumberOfPeople(self):
        return self.rows*self.cols

    def maxNumberOfPeople(self):
        return (2*self.optNumberOfPeople())

    def createSeating(self, students):
        colsNeeded = math.floor(len(students) / self.rows)
        if(colsNeeded > 2 * self.cols):
            raise ValueError('Too many students assigned to room ' + self.name)
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
    
    def wholeTable(self, row, col, name):
        widthOffs = col * (self.tableWidth + 1) + (self.tableWidth/4) #divide by 4, half of a half table
        heightOffs = row * (- self.tableHeight - 1)
        return self.createTable(self.tableWidth, self.tableHeight, widthOffs, heightOffs, name)

    def splitTable(self, row, col, name1, name2):
        widthOffs = col * (self.tableWidth + 1) #dup
        heightOffs = row * (- self.tableHeight - 1) #dup
        returnString = self.createTable(self.tableWidth/2, self.tableHeight, widthOffs, heightOffs, name1)
        returnString += self.createTable(self.tableWidth/2, self.tableHeight, widthOffs + self.tableWidth/2, heightOffs, name2)
        return returnString

    def createTable(self, width, height, widthOffs, heightOffs, name):
        return '\n\\node [draw, minimum width=' + str(width) + 'cm, minimum height='+ str(height) + 'cm, anchor=base] at(' + str(widthOffs) + ',' + str(heightOffs) + ') {\\begin{varwidth}{1.5cm}' + name + '\\end{varwidth}};'
