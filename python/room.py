from abc import ABC, abstractmethod
import math

class Room(ABC):
        

    def __init__(self, name, col, row):
        self.name=name
        self.cols=col
        self.rows=row
        self.students = []
    
    def optNumberOfPeople(self):
        return self.rows*self.cols

    def maxNumberOfPeople(self):
        return (2*self.optNumberOfPeople())

    @abstractmethod
    def createSeating(self, students):
        return NotImplemented

    @abstractmethod
    def latexHeader(self):
        return NotImplemented

    @abstractmethod
    def latexFooter(self):
        return NotImplemented
