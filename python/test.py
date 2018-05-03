from listRoom import ListRoom
from person import Person

a = ListRoom("testRoom",6, 6)
studentNames = ["Adam","Bertil"] * 18
students = [Person(x, "someTime", "") for x in studentNames]
print(students[1].name)
print(a.cols)
print(a.createSeating(students))
