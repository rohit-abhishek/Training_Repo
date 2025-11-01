import math

class Vector:
    def __init__(self, x, y) -> None:
        self.x = x 
        self.y = y

    def __add__(self, oOther):
        return Vector (self.x + oOther.x, self.y + oOther.y)
    
    def __sub__(self, oOther):
        return Vector (self.x - oOther.x, self.y - oOther.y)
    
    def __mul__(self, oOther):
        if isinstance(oOther, Vector):
            return Vector ((self.x * oOther.x), (self.y * oOther.y))
        elif isinstance(oOther, (int, float)):
            return Vector ((self.x * oOther), (self.y * oOther))
        else: 
            raise TypeError("Second Value must be a vector or scalar")
        
    def __abs__(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2))
    
    def __eq__(self, oOther):
        return (self.x == oOther.x) and (self.y == oOther.y)
    
    def __ne__(self, oOther):
        return not (self == oOther)
    
    def __lt__(self, oOther):
        if abs(self) < abs(oOther):
            return True
        
        return False 
    
    def __gt__(self, oOther):
        if abs(self) > abs(oOther):
            return True
        
        return False
    
    def __str__(self):
        return "This vector has the value (" + str(self.x) + ", " + str(self.y) + ")"
    

