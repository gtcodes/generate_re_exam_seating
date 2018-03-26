import codecs
import operator
from room import Room
from person import Person

#T26 - 15 bord, 2 med 3 platser
T13 = Room("T13",6,6)
T14 = Room("T14",5,5)
T3 = Room("T3",4,8)
T4 = Room("T4",4,8)
T26 = Room("T26",6,5)

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
    #TODO markera om test är i två delar
    #TODO sortera först sedan ta bort dups, sedan splitta i två listor.
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
    
    for student in uniqueStudents:
        print(student)
    
    #TODO update to pick indecies and send people to createSeating
    
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

def divideNonComputerPeople(noComputer, computerNeeded, roomsToUse, allowNonComputerFolksInT26):
    totalNumberOfStudents = len(noComputer) + len(computerNeeded)
    if(len(computerNeeded) > 32):
        print("WARNING! More than 32 people need computer.")
    
    numberOfRooms = len(roomsToUse)
    numberOfOptPlaces = 0
    
    for room in roomsToUse:
        numberOfOptPlaces += room.optNumberOfPeople()
    '''
    if(noComputer <= 36):
        createSeatingT13(noComputer)
    else if(noComputer <= 61):
        createSeatingT13(36)
        createSeatingT14(noComputer-36)
    else if(noComputer <= 97):
        createSeatingT14(25)
        createSeatingT13(noComputer-25)
    else if(noComputer <= 122):
        createSeatingT13(72)
        createSeatingT14(noComputer-72)
    else if(noComputer <= 154)
    '''

#These functions could be placed inside the room class, with each room extending the base room class
#unsure if that really helps however.
def createSeatingT13(people):
    #TODO
    return 0

def createSeatingT14(people):
    #TODO
    return 0
def createSeatingTX(people):
    #TODO
    return 0


main()
