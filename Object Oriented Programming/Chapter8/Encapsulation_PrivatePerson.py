# using explict private for instance variables 

class PrivatePerson: 
    def __init__(self, name, some_data, private_data) -> None:
        self.name = name 
        # create implicit private data 
        self._somedata = some_data
        # create explicit private data 
        self.__private_data = private_data
    
    def get_name(self):
        return self.name 

    def set_name(self, name):
        self.name = name

# access public instance variable
p = PrivatePerson('Rohit', 'LNU','mypassword')

# you can still access instance varaible outside class body. This is dangerous 
print ('Public Variable Access')
print(p.name)
# you can change the value of this as well 
p.name = "Rohit Abhishek"
print(p.name)

# you can still access implicit private varaible outside class body. This is just a convention - this does not gurantee the privatization of variable has happened
print () 
print ('Implicit Private Variable Access')
print(p._somedata)
p._somedata = 'Abhishek'
print(p._somedata)

# you cannot access explicitly marked private variables 
print () 
print ('Explicit Private Variable Access')
print(p.__private_data)