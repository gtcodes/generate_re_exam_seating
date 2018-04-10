from room import Room
from person import Person

a = Room("testRoom",6,6)
studentNames = ["Adam","Bertil"] * 18
students = [Person(x, "someTime", "") for x in studentNames]
print(a.createSeating(students))
