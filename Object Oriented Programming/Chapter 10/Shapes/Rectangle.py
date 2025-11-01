import pygame 
from Shape import * 

class Rectangle(Shape):

    def __init__(self, window, maxWidth, maxHeight) -> None:
        super().__init__(window, "Rectangle", maxWidth, maxHeight)
        self.width = random.randrange(10, 100)
        self.height = random.randrange(10, 100)
        self.rect = pygame.rect(self.x, self.y, self.width, self.height)

    def clickedInside(self, mousePoint):
        clicked = self.rect.collidepoint(mousePoint)
        return clicked
    
    def getArea(self):
        theArea = self.width * self.height
        return theArea