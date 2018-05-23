
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PrinterInfoWriter(metaclass=Singleton):
    logFile = "output/printInfo.txt"
    
    #this should not open and close the file handle each time. Instead do so when you create and delete the file. The __del__ method seemed sort of shady in python. You also do not want a stateful singleton so it cannot be opended or closed by some other method than delete and create.
    def __init__(self):
        with open(self.logFile, 'w') as f:
            #clear the log file on creation
            pass

    def displayInfo(self, text):
        with open(self.logFile, 'a') as f:
            f.write(text + '\n')
