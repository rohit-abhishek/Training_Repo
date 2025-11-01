import pygame
import sys
from pygame.locals import * 
from Rectangle import * 
from Circle import * 
from Triangle import * 
import pygwidgets

WHITE = (255, 255, 255)
WINDOW_WIDTH = 640 
WINDOW_HEIGHT = 480 
FRAMES_PER_SECOND = 30 
N_SHAPES = 10 

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
clock = pygame.time.Clock()

shapeList = [] 
shapeClassTuple = (Rectangle, Circle, Triangle)

for i in range(0, N_SHAPES):
    randomlyChosenClass = random.choice(shapeClassTuple)
    oShape = randomlyChosenClass(window, WINDOW_WIDTH, WINDOW_HEIGHT)
    shapeList.append(oShape)

oStatusLine = pygwidgets.DisplayText(window, (4,4), 'Click on shape', fontSize=28)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            for oShape in reversed(shapeList):
                if oShape.clickedInside(event.pos):
                    area = oShape.getArea()
                    area = str(area) 
                    theType = oShape.getType()
                    newText = "Clicked on a " + theType + " whose area is " + area 
                    oStatusLine.setValue(newText)
                    break 

    window.fill(WHITE)
    for oShape in shapeList:
        oShape.draw()
    oStatusLine.draw()

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)