class Person:
    
    def __init__(self, name, testTimes, hasComputer):
        self.name = name
        self.numberOfTests = 1
        self.testTime = []
        self.testTime.append(testTimes)
        self.hasComputer = hasComputer

    def __str__(self):
        return "Name = %s, number of tests = %s, has computer = %s, TestTimes = %s\n" % (self.name, self.numberOfTests, self.hasComputer, self.testTime)
