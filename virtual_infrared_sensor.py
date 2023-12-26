import math
import tkinter as tk

def getDistances(currentPos: list, facingAngle: int, posDict: dict):

    # initialize variables used later
    unitsToWallL = 0
    unitsToWallF = 0
    unitsToWallR = 0
    
    numDirs = 8
    distList = []

    for dir in range(numDirs):

        dist = 0
        xPos = int(currentPos[0])
        yPos = int(currentPos[1])
        wallOrFloor = posDict.get('(' + str(xPos) + ', ' + str(yPos) + ')')

        while (wallOrFloor != 'W'):
            dist += 1
            
            if (dir == 0): # N
                yPos -= 1

            if (dir == 1): # NW
                xPos -= 1
                yPos -= 1
            
            if (dir == 2): # W
                xPos -= 1
            
            if (dir == 3): # SW
                xPos -= 1
                yPos += 1
            
            if (dir == 4): # S
                yPos += 1

            if (dir == 5): # SE
                xPos += 1
                yPos += 1
            
            if (dir == 6): # E
                xPos += 1

            if (dir == 7): # NE
                xPos += 1
                yPos -= 1

            wallOrFloor = posDict.get('(' + str(xPos) + ', ' + str(yPos) + ')')

        distList.append(dist)

    # 
    if (facingAngle == 0):
        unitsToWallL = distList[2]
        unitsToWallF = distList[0]
        unitsToWallR = distList[6]

    if (facingAngle == 45):
        unitsToWallL = distList[3]
        unitsToWallF = distList[1]
        unitsToWallR = distList[7]

    if (facingAngle == 90):
        unitsToWallL = distList[4]
        unitsToWallF = distList[2]
        unitsToWallR = distList[0]

    if (facingAngle == 135):
        unitsToWallL = distList[5]
        unitsToWallF = distList[3]
        unitsToWallR = distList[1]
        
    if (facingAngle == 180):
        unitsToWallL = distList[6]
        unitsToWallF = distList[4]
        unitsToWallR = distList[2]

    if (facingAngle == 225):
        unitsToWallL = distList[7]
        unitsToWallF = distList[5]
        unitsToWallR = distList[3]

    if (facingAngle == 270):
        unitsToWallL = distList[0]
        unitsToWallF = distList[6]
        unitsToWallR = distList[4]

    if (facingAngle == 315):
        unitsToWallL = distList[1]
        unitsToWallF = distList[7]
        unitsToWallR = distList[5]
    
    distances = (unitsToWallL, unitsToWallF, unitsToWallR)

    # print(type(distances)) # DIAGNOSTIC
    print(distances) # DIAGNOSTIC
    return distances