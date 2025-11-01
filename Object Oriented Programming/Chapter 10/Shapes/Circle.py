import pygame 
import random 
import math 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Circle:
    def __init__(self, window, maxWidth, maxHeight) -> None:
        self.window = window
        self.color = random.choice((RED, GREEN, BLUE))
        self.x = random.randrange(1, maxWidth-100)
        self.y = random.randrange(25, maxHeight-100)
        self.radius = random.randrange(10, 50)
        self.centerx = self.x + self.radius
        self.centery = self.y + self.radius

        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.shapeType = "Circle"

    def clickedInside(self, mousePoint):
        distance = math.sqrt(((mousePoint[0] - self.centerx) ** 2) + ((mousePoint[1] - self.centery) ** 2))
        if distance <= self.radius:
            return True
        return False
    
    def getArea(self):
        theArea = math.pi * (self.radius ** 2) 
        return theArea
    
    def getType(self):
        return self.shapeType
    
    def draw(self):
        pygame.draw.circle(self.window, self.color, (self.centerx, self.centery), self.radius, 0)
