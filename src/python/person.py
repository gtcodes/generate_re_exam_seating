class Person:
    
    def __init__(self, name, testTimes, hasComputer):
        self.name = name
        self.numberOfTests = 1
        self.testTime = []
        self.testTime.append(testTimes)
        self.hasComputer = hasComputer

    def merge(self, other):
        for times in other.testTime:
            self.testTime.append(times)
        self.hasComputer = self.hasComputer or other.hasComputer
        self.numberOfTests += other.numberOfTests

    def getTestTime(self):
        result = self.testTime[0]
        if(len(self.testTime)>1):
            for time in self.testTime[1:]:
                result= result + " och " + time
        return(result)

    def __str__(self):
        return "Name = %s, number of tests = %s, has computer = %s, TestTimes = %s\n" % (self.name, self.numberOfTests, self.hasComputer, self.testTime)
