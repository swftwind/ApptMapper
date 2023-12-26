from PIL import Image, ImageTk
import csv
import json

# function to be called in main to determine which pixels are 'floor' and which are 'wall'
def getImageCSV(filename: str):
    
    img = Image.open(filename)
    img = img.convert("RGB")

    # get image dimensions
    width, height = img.size

    # initiate variable conditions (the origin for the getpixel((x, y)) function is the top left corner)
    xPos, yPos = 0
    pixelValue = (0, 0, 0)
    floorThresh = 100
    pixelType = 'F' # temporary storage for whether a particular pixel (x, y) is a 'floor' pixel or 'wall' pixel
    posDict = {} # dictionary where keys are position tuples of the form (x, y), and values are strings 'F' for floor or 'W' for wall

    # Outer for loop
    for yPos in range(height + 1):
        for xPos in range(width + 1):
            pixelValue = filename.getpixel((xPos, yPos))

            # 
            if ((pixelValue[0] > floorThresh) or (pixelValue[1] > floorThresh) or (pixelValue[2] > floorThresh)):
                pixelType = 'W'
            else:
                pixelType = 'F'
        
            #
            posDict[(xPos, yPos)] = pixelType
        
            xPos += 1
        
        yPos += 1
    
    return posDict