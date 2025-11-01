import sys 
class Square:
    def __init__(self, width, color) -> None:
        self.width = width 
        self.color = color 

oSquare1 = Square(5, "red")
print (sys.getrefcount(oSquare1))

# oSquare1 and 2 are both same object
oSquare2 = oSquare1 
print (oSquare2, sys.getrefcount(oSquare1))

oSquare3 = oSquare2
print (sys.getrefcount(oSquare1))