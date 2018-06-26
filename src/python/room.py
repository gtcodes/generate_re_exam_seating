from abc import ABC, abstractmethod
import math

class Room(ABC):
        

    def __init__(self, name, col, row):
        self.name=name
        self.cols=col
        self.rows=row
        self.students = []
    
    @abstractmethod
    def getPaperSize(self):
        return NotImplemented
    
    def optNumberOfPeople(self):
        return self.rows*self.cols

    def maxNumberOfPeople(self):
        return (2*self.optNumberOfPeople())

    @abstractmethod
    def createSeating(self, students, planName):
        return NotImplemented

    @abstractmethod
    def createAdminPlan(self, students, planName):
        return NotImplemented

    @abstractmethod
    def latexHeader(self):
        return NotImplemented

    @abstractmethod
    def latexFooter(self):
        return NotImplemented

    @abstractmethod
    def adminLatexHeader(self):
        return NotImplemented

    @abstractmethod
    def adminLatexFooter(self):
        return NotImplemented
