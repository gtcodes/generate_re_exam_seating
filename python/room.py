#from abc import ABC, abstractmethod

class Room():
        
    tableWidth = 3
    tableHeight = 1

    def __init__(self, name, col, row):
        self.name=name
        self.cols=col
        self.rows=row
        self.students=[]
    
    def optNumberOfPeople(self):
        return self.rows*self.cols

    def maxNumberOfPeople(self):
        return (2*self.optNumberOfPeople())

    #@abstractmethod
    def createSeating(self):
        currentStudent = 0
        tableCode = ''
        for row in range(0,self.rows):
            for table in range(0,self.cols):
                if(row%2 == 0):
                    tableCode += self.splitTable(row, table)
                else:
                    tableCode += self.wholeTable(row, table)
        return tableCode

    def wholeTable(self, row, col):
        widthOffs = col * (self.tableWidth + 1) + (self.tableWidth/4) #divide by 4, half of a half table
        heightOffs = row * (- self.tableHeight - 1)
        return self.createTable(self.tableWidth, self.tableHeight, widthOffs, heightOffs, 'bertil')

    def splitTable(self, row, col):
        widthOffs = col * (self.tableWidth + 1) #dup
        heightOffs = row * (- self.tableHeight - 1) #dup
        returnString = self.createTable(self.tableWidth/2, self.tableHeight, widthOffs, heightOffs, 'adam')
        returnString += self.createTable(self.tableWidth/2, self.tableHeight, widthOffs + self.tableWidth/2, heightOffs, 'adam')
        return returnString

    def createTable(self, width, height, widthOffs, heightOffs, name):
         return '\n\\node [draw, minimum width=' + str(width) + 'cm, minimum height='+ str(height) + 'cm, anchor=base] at(' + str(widthOffs) + ',' + str(heightOffs) + ') {\\begin{varwidth}{1.5cm}' + name + '\\end{varwidth}};'
