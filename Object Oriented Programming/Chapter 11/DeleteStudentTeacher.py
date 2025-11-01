class Student:
    def __init__(self, name) -> None:
        self.name = name 
        print ("Creating student object", self.name)

    def __del__(self):
        print ("In __del__ method for Student", self.name)

class Teacher:
    def __init__(self, name) -> None:
        self.name = name
        self.oStudent1 = Student("Joe")
        self.oStudent2 = Student("Chris")
        self.oStudent3 = Student("Robert")

        print ("Creating Teacher Object", self.name)

    def __del__(self):
        print ("In __del__ method for Teacher", self.name)

oTeacher = Teacher("Kevin")

del oTeacher