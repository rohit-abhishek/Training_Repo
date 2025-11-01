# using property to indicrectly access data in an object 

class Student:
    def __init__(self, name, starting_grade=0) -> None:
        self.__name = name 

        # the below assignement will call setter method to assign the value to __grade private variable; this is considered as property by python interpreter 
        # very advantegeous when we want to validate the data before the assignment
        self.grade = starting_grade

    @property
    def grade(self):
        print ("In Getter")
        return self.__grade 

    @grade.setter
    def grade(self, new_grade):
        print ("In Setter")
        try:
            new_grade = int(new_grade)
        except (TypeError, ValueError) as e: 
            raise type(e) ('New grade: ' + str(new_grade) + ', is invalid type')
        if (new_grade < 0) or (new_grade > 100):
            raise ValueError ('New grade: ' + str(new_grade) + ', must be between 0 and 100')

        self.__grade = new_grade

    def show(self):
        print ()
        print ("Student name: ", self.__name)
        print ("Student grade: ", self.grade)

    def _private_show(self):
        print ()
        print ("This is private show")
        print ("Student name: ", self.__name)
        print ("Student grade: ", self.grade)

        self.__very_private_show()

    def __very_private_show(self):
        print ()
        print ("This is very private show")
        print ("Student name: ", self.__name)
        print ("Student grade: ", self.grade)              


s1 = Student("Rohit Abhishek")
print ("This is details for student 1")
print(s1.grade)

# set the grade property
s1.grade = 95
print(s1.grade)

# call show method 
s1.show() 
s1._private_show() 
# s1.__very_private_show()                    # cannot access this method outside the class body


s2 = Student("Someone", 55)
print ("This is details for student 2")
print(s2.grade)

# call show method 
s2.show() 
s2._private_show() 