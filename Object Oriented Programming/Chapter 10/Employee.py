class Employee:
    def __init__(self, name, title, ratePerHour=None) -> None:
        self.name = name 
        self.title = title 
        if ratePerHour is not None: 
            ratePerHour = float(ratePerHour)
        self.ratePerHour = ratePerHour

    def getName(self):
        return self.name 
    
    def getTitle(self):
        return self.title 
    
    def payPerYear(self):
        pay = 52 * 5 * 8 * self.ratePerHour
        return pay
    
class Manager(Employee):
    def __init__(self, name, title, salary, reportList=None) -> None:
        self.salary = float(salary)
        if reportList is None:
            reportList = []
        self.reportList = reportList
        super().__init__(name, title)

    def getReports(self):
        return self.reportList
    
    def payPerYear(self, giveBonus):
        pay = self.salary
        if giveBonus:
            pay=pay+(0.1*self.salary)
            print (self.name, 'gets a bonus for good work')
        return pay

def generate_employee():
    oEmployee1 = Employee("Joe Smith", "Pizza Maker", 16)    
    oEmployee2 = Employee("Chris Soe", "Cashier", 14)  
    oManager = Manager("Sue Jones", "Pizza Resturant Manager", 55000, [oEmployee1, oEmployee2])  

    print ("Employee Name: ", oEmployee1.getName())
    print ("Employee Salary: ", "{:,.2f}".format(oEmployee1.payPerYear()))
    print ("Employee Name: ", oEmployee2.getName())
    print ("Employee Salary: ", "{:,.2f}".format(oEmployee2.payPerYear()))
    print () 

    managerName = oManager.getName()
    print ("Manager Name: ", managerName)
    print ("Manager Salary: ", "{:,.2f}".format(oManager.payPerYear(True)))
    print (managerName, "(" + oManager.getTitle() + ")", "direct reports: ")
    reportList = oManager.getReports()
    for oEmployee in reportList:
        print ("    ", oEmployee.getName(), "(" + oEmployee.getTitle() + ")")

if __name__ == "__main__":
    generate_employee()