# class to have class vairable that keeps count of the instances created from the class 

class Sample:
    nObjects = 0 

    def __init__(self, name) -> None:
        self.name = name 
        Sample.nObjects += 1 

    def __del__ (self):
        Sample.nObjects -= 1


# create sample objects 
oSample1 = Sample("A")
oSample2 = Sample("B")
oSample3 = Sample("C")
oSample4 = Sample("D")
oSample5 = Sample("E")
oSample6 = Sample("F")

# delete one of the object 
del oSample2

# print the samples 
print ("There are", Sample.nObjects, "Sample Objects")