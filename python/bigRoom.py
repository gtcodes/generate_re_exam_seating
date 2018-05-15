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
        return( '\\documentclass{article}\n'
            '\\usepackage[paperheight=420mm,paperwidth=297mm]{geometry}\n'
            '\\usepackage[utf8]{inputenc}\n'
            '\\usepackage{adjustbox}\n'
            '\\usepackage{tikz}\n'
            '\\usepackage{varwidth}\n'
            '\\usepackage{pdflscape}\n'
            '\n'
            '\\setlength{\\topmargin}{8mm}\n'
            '\\setlength{\\oddsidemargin}{0in}\n'
            '\\setlength{\\evensidemargin}{0in}\n'
            '\n'
            '\\setlength{\\textheight}{370mm}\n'
            '\\setlength{\\textwidth}{290mm}\n'
            '\n'
            '\\begin{document}\n'
            '\\begin{landscape}\n'
            '\n'
            '\\begin{centering}\n'
            '\\section*{\\Huge Fram mot tavla och scen} \\vspace{5mm}\n'
            '\\end{centering}\n'
            '\n'
            '\\begin{tikzpicture}\n'
            '\\node[draw=none]at(0,0){};\n'
            )

    def latexFooter(self):
        return( '\n'
            '\\node[draw=none, rotate=90] at (38, -9) {\\Huge \\textbf{Resterande del av skolan}};\n'
            '\n'
            '\\end{tikzpicture}\n'
            '\n'
            '\\pagenumbering{gobble}\n'
            '\\end{landscape}\n'
            '\\end{document}\n'
)
