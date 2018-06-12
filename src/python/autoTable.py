import codecs
import operator
import sys
from listRoom import ListRoom
from bigRoom import BigRoom
from person import Person

#T26 - 15 bord, 2 med 3 platser
T13 = BigRoom("T13",6,6,0)
T14 = BigRoom("T14",5,5,4)
T26 = ListRoom("T26",3,5)
T3 = ListRoom("T3",4,4)

inputFile = sys.argv[1]
texDir = sys.argv[2]
delim = sys.argv[3]

def readGTCCsv(inputFile, delim = '\t', hasComputerCol = 8, nameCol = 1, timeCol = 5, acceptedCol = 6):
    returnList = []
    with codecs.open(inputFile, mode='r', encoding='iso-8859-1') as csvFile:
        csvFile.readline() #skips first line
        for lines in csvFile:
            personRow = [x.strip() for x in lines.split(delim)]
            if(personRow[acceptedCol] == "Ja"):
                hasComputer = (personRow[hasComputerCol] == 'x')
                p = Person(personRow[nameCol], personRow[timeCol], hasComputer)
                returnList.append(p)
    return returnList

def main():
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
    plans = createSeatingPlan(noComputer, computerNeeded)
    #clear the printer info file
    for plan in plans:
        if(plan[2]!=''):
            baseFileName = plan[1].name
            if(plan[0]):
                baseFileName+='Admin'
            fileName = baseFileName + '.tex'
            with open(texDir + '/' + fileName,'w') as f:
                print(fileName)
                f.write(plan[2])
    
# merge students that write multiple tests into one person
# with a list of times rather than just a single value
def mergeDuplicates(students):
    length = len(students)
    i = 0
    while i < length - 1:
        if(students[i].name == students[i+1].name):
            students[i+1].merge(students[i])
            length -= 1
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
        T26Admin = createAdminPlan(T26, computerNeeded)
    
    numberOfNoComputer = len(noComputer)
    T13Plan = ''
    T14Plan = ''
    T3Plan = ''
    T13Admin = ''
    T14Admin = ''
    if(numberOfNoComputer <= 36):
        T13Plan = createRoomSeating(T13, noComputer)
        T13Admin = createAdminPlan(T13, NoComputer)
    elif(numberOfNoComputer <= 61):
        T13Plan = createRoomSeating(T13, noComputer[0:36])
        T13Admin = createAdminPlan(T13, noComputer[0:36])
        T14Plan = createRoomSeating(T14, noComputer[36:])
        T14Admin = createAdminPlan(T14, noComputer[36:])
    elif(numberOfNoComputer <= 97):
        T14Plan = createRoomSeating(T14, noComputer[0:25])
        T14Admin = createAdminPlan(T14, noComputer[0:25])
        T13Plan = createRoomSeating(T13, noComputer[25:])
        T13Admin = createAdminPlan(T13, noComputer[25:])
    #elif(noComputer <= 129):
    #    T13Plan = createRoomSeating(T13, noComputer[0:72])
    #    T14Plan = createRoomSeating(T14, noComputer[72:97])
    #    T3Plan = createRoomSeating(T3, noComputer[97:])

    return((False,T26,T26Plan), (False,T13,T13Plan), (False, T14,T14Plan), (True, T26, T26Admin), (True,T13, T13Admin), (True,T14, T14Admin))

def createRoomSeating(room, students):
    seating = room.latexHeader()
    seating += room.createSeating(students)
    seating += room.latexFooter()
    return seating

def createAdminPlan(room, students):
    seating = room.adminLatexHeader()
    seating += room.createAdminPlan(students)
    seating += room.adminLatexFooter()
    #with open(texDir + '/' + "T26Admin.tex",'w') as file:
    #    file.write(seating)
    return seating

main()
