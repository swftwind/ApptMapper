def getDistances(currentPos: list, facingAngle: int, posDict: dict):
    unitsToWallL = 0
    unitsToWallF = 0
    unitsToWallR = 0
    
    # list of caridnal directions to iterate over
    cardinalDirections = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]
    # list of distances in each of said cardinal directions above
    distanceList = []
    # list of endpt pixels, distances above are the distances between endpt pixels and current position
    pxEndList = []
    
    for directon in cardinalDirections:

        # current position of roomba
        distanceToWall = 0
        xPos = int(currentPos[0] + 10)
        yPos = int(currentPos[1] + 10)

        # check dictionary to determine when distance counter must stop (tracer hit a wall)
        wallOrFloor = posDict.get('(' + str(xPos) + ', ' + str(yPos) + ')')

        # draw lines in each of the cardinal directions counting up pixels until the line hits a wall
        while (wallOrFloor != 'W'):
            distanceToWall += 1
            
            if (directon == "N"):
                yPos -= 1

            if (directon == "NW"):
                xPos -= 1
                yPos -= 1
            
            if (directon == "W"):
                xPos -= 1
            
            if (directon == "SW"):
                xPos -= 1
                yPos += 1
            
            if (directon == "S"):
                yPos += 1

            if (directon == "SE"):
                xPos += 1
                yPos += 1
            
            if (directon == "E"):
                xPos += 1

            if (directon == "NE"):
                xPos += 1
                yPos -= 1

            wallOrFloor = posDict.get('(' + str(xPos) + ', ' + str(yPos) + ')')

        # store relevant data to return for algorithm use later
        distanceList.append(distanceToWall)
        pxEndList.append((xPos, yPos))
    
    # we have measurements in each direction, but our robot is not necessarily facing any of these directions,
    # therefore we must set distances relative to direction robot is facing
    if (facingAngle == 0):
        unitsToWallL = distanceList[2]
        unitsToWallF = distanceList[0]
        unitsToWallR = distanceList[6]

    if (facingAngle == 45):
        unitsToWallL = distanceList[3]
        unitsToWallF = distanceList[1]
        unitsToWallR = distanceList[7]

    if (facingAngle == 90):
        unitsToWallL = distanceList[4]
        unitsToWallF = distanceList[2]
        unitsToWallR = distanceList[0]

    if (facingAngle == 135):
        unitsToWallL = distanceList[5]
        unitsToWallF = distanceList[3]
        unitsToWallR = distanceList[1]
        
    if (facingAngle == 180):
        unitsToWallL = distanceList[6]
        unitsToWallF = distanceList[4]
        unitsToWallR = distanceList[2]

    if (facingAngle == 225):
        unitsToWallL = distanceList[7]
        unitsToWallF = distanceList[5]
        unitsToWallR = distanceList[3]

    if (facingAngle == 270):
        unitsToWallL = distanceList[0]
        unitsToWallF = distanceList[6]
        unitsToWallR = distanceList[4]

    if (facingAngle == 315):
        unitsToWallL = distanceList[1]
        unitsToWallF = distanceList[7]
        unitsToWallR = distanceList[5]
    
    distances = (unitsToWallL, unitsToWallF, unitsToWallR)
    distData = (distances, distanceList, pxEndList)

    # print(distances) # DIAGNOSTIC

    # distData is a list 3 elements long which houses lists and tuples above w/ relevant data
    return distData