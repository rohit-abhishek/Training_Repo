class Example: 
    def __init__(self, some_value) -> None:
        self.__x = some_value

    # notice the name of both methods are same, the property decorator has helped to create getter and setter methods and add distinct getter and setter to each of them
    @property
    def x(self):
        print ("In getter")
        return self.__x
    
    @x.setter
    def x(self, value):
        print ("In setter")
        self.__x = value 

ex = Example('myname')
print(ex.x)
print ()
ex.x = "Your name"
print(ex.x)