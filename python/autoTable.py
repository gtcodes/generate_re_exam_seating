import codecs
import operator
from room import Room
from person import Person

#T26 - 15 bord, 2 med 3 platser
T13 = Room("T13",6,6)
T14 = Room("T14",5,5)
T3 = Room("T3",4,4)
T4 = Room("T4",4,4)
T26 = Room("T26",3,5)

inputFile = "../newexcelldata.xls"

def readGTCCsv(inputFile, delim = '\t', hasComputerCol = 8, nameCol = 1, timeCol = 5):
    returnList = []
    with codecs.open(inputFile, mode='r', encoding='iso-8859-1') as csvFile:
        csvFile.readline() #skips first line
        for lines in csvFile:
            personRow = [x.strip() for x in lines.split(delim)]
            hasComputer = (personRow[hasComputerCol] != '')
            p = Person(personRow[nameCol], personRow[timeCol], hasComputer)
            returnList.append(p)
    return returnList

def main():
    #TODO markera om test är i två delar?
    allStudents = readGTCCsv(inputFile, hasComputerCol = 8, delim=';')
    try:
        import operator
    except ImportError:
        keyfun = lambda x: x.name
    else:
        keyfun = operator.attrgetter("name")

    allStudents.sort(key = keyfun, reverse = False)
    uniqueStudents = mergeDuplicates(allStudents)
    (computerNeeded, noComputer) = splitStudents(uniqueStudents)
    plans = createSeatingPlan(noComputer, computerNeeded)

    for plan in plans:
        with open(plan[0]+'.tex','w') as f:
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
    
    T26Plan = createRoomSeating(T26, computerNeeded)

    numberOfNoComputer = len(noComputer)
    T13Plan = ''
    T14Plan = ''
    T3Plan = ''
    if(numberOfNoComputer <= 36):
        T13Plan = createRoomSeating(T13, noComputer)
    elif(numberOfNoComputer <= 61):
        T13Plan = createRoomSeating(T13, noComputer[0:35])
        T14Plan = createRoomSeating(T14, noComputer[36:])
    elif(numberOfNoComputer <= 97):
        T14Plan = createRoomSeating(T14, noComputer[0:24])
        T13Plan = createRoomSeating(T13, noComputer[25:])
    elif(noComputer <= 129):
        T13Plan = createRoomSeating(T13, noComputer[0:71])
        T14Plan = createRoomSeating(T14, noComputer[72:96])
        T3Plan = createRoomSeating(T3, noComputer[97:])

    return(('T26',T26Plan), ('T13', T13Plan),('T14',T14Plan),('T3',T3Plan))

def createRoomSeating(room, students):
    seating = createLatexHeader()
    seating += room.createSeating(students)
    seating += createLatexFooter()
    return seating

def createLatexHeader():
    return( '\\documentclass{article}\n' +
            '\\usepackage[utf8]{inputenc}\n' +
            '\\usepackage{adjustbox}\n' +
            '\\usepackage{tikz}\n' +
            '\\usepackage{varwidth}\n' +
            '\\usepackage{pdflscape}\n' +
            '\\usepackage{fancyhdr}\n' +
            '\\setlength{\\topmargin}{-.3 in}\n' +
            '\\setlength{\\oddsidemargin}{0in}\n' +
            '\\setlength{\\evensidemargin}{0in}\n' +
            '\\setlength{\\textheight}{9.5in}\n' +
            '\\setlength{\\textwidth}{6.5in}\n' +
            '\n' +
            '\\begin{document}\n' +
            '\\begin{landscape}\n' +
            '{\\centering\n' +
            '\\section*{Scen}\\vspace{0.5cm}\n' +
            '}\n' +
            '\n' +
            '\\thispagestyle{fancy}\n' +
            '\\renewcommand{\\headrulewidth}{0.4pt} %sets size of header bar\n' +
            '\n' +
            '\\begin{tikzpicture}\n'
            )

def createLatexFooter():
    return( '\\end{tikzpicture}\n' +
            '\\pagenumbering{gobble}\n' +
            '\\chead{\\large Resterande del av skolan}\n' +
            '\\end{landscape}\n' +
            '\\end{document}\n'
            )

main()
