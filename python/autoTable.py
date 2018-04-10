import codecs
import operator
from room import Room
from person import Person

#T26 - 15 bord, 2 med 3 platser
T13 = Room("T13",6,6,0)
T14 = Room("T14",5,5,4)
T3 = Room("T3",4,4,0)
T4 = Room("T4",4,4,0)
T26 = Room("T26",3,5,0)

inputFile = "../2018-04-03.xls"

def readGTCCsv(inputFile, delim = '\t', hasComputerCol = 6, nameCol = 1, timeCol = 5):
    returnList = []
    with codecs.open(inputFile, mode='r', encoding='iso-8859-1') as csvFile:
        csvFile.readline() #skips first line
        for lines in csvFile:
            personRow = [x.strip() for x in lines.split(delim)]
            hasComputer = (personRow[hasComputerCol] == 'x')
            p = Person(personRow[nameCol], personRow[timeCol], hasComputer)
            returnList.append(p)
    return returnList

def main():
    #TODO markera om test är i två delar?
    allStudents = readGTCCsv(inputFile)
    try:
        import operator
    except ImportError:
        keyfun = lambda x: x.name
    else:
        keyfun = operator.attrgetter("name")

    allStudents.sort(key = keyfun, reverse = False)
    uniqueStudents = mergeDuplicates(allStudents)
    (computerNeeded, noComputer) = splitStudents(uniqueStudents)
    print(str(len(computerNeeded)) + "    " + str(len(noComputer)))
    plans = createSeatingPlan(noComputer, computerNeeded)
    for plan in plans:
        with open('../tex/'+plan[0]+'.tex','w') as f:
            f.write(plan[1])
    
# merge students that write multiple tests into one person
# with a list of times rather than just a single value
def mergeDuplicates(students):
    length = len(students)
    i = 0
    while i < length - 1:
        if(students[i].name == students[i+1].name):
            students[i+1].merge(students[i])
            length-=1
            del students[i]
        i += 1
    return students

def splitStudents(students):
    computerNeeded = []
    noComputer = []
    for student in students:
        if(student.hasComputer):
            computerNeeded.append(student)
        else:
            noComputer.append(student)
    return(computerNeeded, noComputer)

def createSeatingPlan(noComputer, computerNeeded, allowNonComputerFolksInT26 = True):
    totalNumberOfStudents = len(noComputer) + len(computerNeeded)
    if(len(computerNeeded) > 32):
        print("WARNING! More than 32 people need computer.")
    T26Plan = ''
    if(len(computerNeeded) > 0):
        T26Plan = createRoomSeating(T26, computerNeeded)
    
    numberOfNoComputer = len(noComputer)
    T13Plan = ''
    T14Plan = ''
    T3Plan = ''
    if(numberOfNoComputer <= 36):
        T13Plan = createRoomSeating(T13, noComputer)
    elif(numberOfNoComputer <= 61):
        T13Plan = createRoomSeating(T13, noComputer[0:36])
        T14Plan = createRoomSeating(T14, noComputer[36:])
    elif(numberOfNoComputer <= 97):
        T14Plan = createRoomSeating(T14, noComputer[0:25])
        T13Plan = createRoomSeating(T13, noComputer[25:])
    elif(noComputer <= 129):
        T13Plan = createRoomSeating(T13, noComputer[0:72])
        T14Plan = createRoomSeating(T14, noComputer[72:97])
        T3Plan = createRoomSeating(T3, noComputer[97:])

    return(('T26',T26Plan), ('T13', T13Plan),('T14',T14Plan),('T3',T3Plan))

def createRoomSeating(room, students):
    seating = createLatexHeader()
    seating += room.createSeating(students)
    seating += createLatexFooter()
    return seating

def createLatexHeader():
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

def createLatexFooter():
    return( '\n'
            '\\node[draw=none, rotate=90] at (38, -9) {\\Huge \\textbf{Resterande del av skolan}};\n'
            '\n'
            '\\end{tikzpicture}\n'
            '\n'
            '\\pagenumbering{gobble}\n'
            '\\end{landscape}\n'
            '\\end{document}\n'
)

main()
