import csv
import json
from PIL import Image, ImageTk

# function to be called in main to determine which pixels are 'floor' and which are 'wall'
def getImageJSON(filename: str):
    
    img = Image.open(filename)
    img = img.convert("RGB")

    # get image dimensions
    imageWidth, imageHeight = img.size

    # initiate variable conditions (the origin for the getpixel((x, y)) function is the top left corner)
    # xPos, yPos = 0
    pixelValue = (0, 0, 0)
    floorThresh = 50 # if a pixel has one of its RGB tuple values > this threshold, it will be considered white
    pixelType = 'F' # temporary storage for whether a particular pixel (x, y) is a 'floor' pixel or 'wall' pixel
    posDict = {} # dictionary where keys are position strings of the form '(x, y)', and values are strings 'F' for floor or 'W' for wall

    # outer for loop iterates over yPos, for each iteration of outer loop a row of pixels is processed by inner for loop
    for yPos in range(imageHeight):
        for xPos in range(imageWidth):
            pixelValue = img.getpixel((xPos, yPos))

            # each pixel RGB tuple is checked compared to the threshold value to determine whether it is a 'floor' or 'wall' pixel.
            if ((pixelValue[0] < floorThresh) or (pixelValue[1] < floorThresh) or (pixelValue[2] < floorThresh)):
                pixelType = 'W'
            else:
                pixelType = 'F'

            # adds each pixel position and value into dict
            posDict['(' + str(xPos) + ', ' + str(yPos) + ')'] = pixelType
        
            xPos += 1
        
        yPos += 1
    
    # creating a json of the dictionary, mostly for diagnostic purposes
    with open('collisionsDict.json', 'w') as json_file:
        json.dump(posDict, json_file, indent=4)
    
    return posDict