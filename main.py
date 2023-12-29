import math
import tkinter as tk
from PIL import Image, ImageTk
from image_processing import getImageJSON
from virtual_infrared_sensor import getDistances

# Floorplan START
floorplan = input("Input floorplan filename: ")
floorplanPath = 'floorplans/' + floorplan + '.png'
floorJSON = getImageJSON(floorplanPath)
# Floorplan END

# roomba input 'spawnpoint'
startPosX = input("Input starting x-coord: ")
startPosY = input("Input starting y-coord: ")
# check if there is a wall at the starting coordinates
while floorJSON.get(f"({startPosX}, {startPosY})") == "W":
    print("Those starting coordinates will place you into a wall.\nPlease select different starting coordinates.")
    startPosX = input("Input starting x-coord: ")
    startPosY = input("Input starting y-coord: ")

# contains the toggle value of whether the user wants to see coordinates visible next to the arrow endpoints
global showDistanceNumbers
showDistanceNumbers = True

# list to keep track of coordinate boxes
global distanceTextList
distanceTextList = []

# list to keep track of line ids to delete to clear canvas
global lineList
lineList = []

# posXY is updated by movement functions throughout program and is needed as a parameter by other functions
global posXY

# degrees of rotation based on the roomba starting out facing north/up.
# #left is positive and right is negative, but the number is always calculated to be between 0 and 359 degrees.
global roombaRotation
roombaRotation = 0

def check_for_wall(dx, dy):
    # check if the pixel at the position i want to move to contains a wall, by checking floorJSON with the given coordinates.
    x, y = canvas.coords(roombaObj)
    x, y = map(int, (x + dx + 10, y + dy + 10))  # adds the future/requested coordinates to the current coordinates

    '''
    note:   the + 10 is to account for the fact that the origin of the image is the top left, and the image is 21x21, 
            so we move an extra 10 units to shift the 'effective center' according to the collisions that we've set up

            the origin (0,0) is top left, and the positive x-dir is to the right whereas the POSITIVE y-dir is DOWN
    '''

    if floorJSON.get(f"({x}, {y})") == "W":  # checks if the new coordinates contain a wall
        return True
    else:
        return False

def update_roomba_rotation(angle_degrees):
    global roombaRotation
    roombaRotation += angle_degrees
    roombaRotation %= 360  # Ensure the angle stays within 0 to 359 degrees

def create_movable_object(x, y):
    # Create an image on the canvas
    roomba_id = canvas.create_image(x, y, anchor=tk.NW, image=tk_roomba_image)
    # Attach the image to the canvas to prevent garbage collection
    canvas.itemconfig(roomba_id, image=tk_roomba_image)
    return roomba_id

# Movement/Rotations START
def move(event, dx, dy):
    dx = round(dx)
    dy = round(dy)
    if not check_for_wall(dx, dy):
        canvas.move(roombaObj, dx, dy)

def rotate_image(angle_degrees):
    global roomba_image, tk_roomba_image  # Declare these as global to modify them
    update_roomba_rotation(angle_degrees)
    roomba_image = roomba_image.rotate(angle_degrees)
    tk_roomba_image = ImageTk.PhotoImage(roomba_image)
    canvas.itemconfig(roombaObj, image=tk_roomba_image)

def move_forward(event):
    global posXY
    angle_rad = math.radians(roombaRotation)
    move(event, -1 * math.sin(angle_rad), -1 * math.cos(angle_rad))
    clearTracers()
    clearDistanceText()
    posXY = canvas.coords(roombaObj)
    # print(getDistances(posXY, roombaRotation, floorJSON)) # DIAGNOSTIC

def move_back(event):
    global posXY
    angle_rad = math.radians(roombaRotation)
    move(event, math.sin(angle_rad), math.cos(angle_rad))
    clearTracers()
    clearDistanceText()
    posXY = canvas.coords(roombaObj)

def rotate_left(event):
    rotate_image(45)  # Rotate 45 degrees to the left

def rotate_right(event):
    rotate_image(-45)  # Rotate 45 degrees to the right

# Movement/Rotations END

# Load your apartment layout image
layout_image = Image.open(floorplanPath)

# Create a basic GUI window using Tkinter
window = tk.Tk()

# Load the roomba image after the Tk instance is created
roomba_image = Image.open("roomba.png")
tk_roomba_image = ImageTk.PhotoImage(roomba_image)

canvas = tk.Canvas(window, width=layout_image.width, height=layout_image.height)
canvas.pack()

# Display the image in the GUI
tk_image = ImageTk.PhotoImage(layout_image)
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

# Create a movable object (roomba image) at an initial position
roombaObj = create_movable_object(startPosX, startPosY)

# Bind keys to the movement functions
window.bind("<Up>", move_forward)
window.bind("<Down>", move_back)
window.bind("<Left>", rotate_left)
window.bind("<Right>", rotate_right)

'''
lambda is required below because in order to use tkinter's 'bind' method, there must be a single parameter 'event',
so we use lambda to combine the 3 required parameters for getDistances() into one lamba function with the 'event'
parameter while still handing off currentPos, facingAngle, and posDict to getDistances(), which are the parameters
it needs as can be seen in virtual_infrared_sensor.py
'''  # this was changed after using a wrapper function, now lambda is just there for funsies, can remove if/when optimizing

# ensure parameters are correct for getDistances()
posXY = canvas.coords(roombaObj)

# wrapper function to get distances using virtual_infrared_sensor.py
def wrapperFunction():
    global distanceData
    distanceData = getDistances(posXY, roombaRotation, floorJSON)
    # distanceData is a list with 3 elements, the first is the tuple of lengths from the 3 sensors (left, front, right, in that order),
    # the second is a list (inside the first list) with all lengths from walls in the 8 cardinal directions, the third and last elements
    # is the coords of each of the 8 endpt pixels to where lines will be drawn

    drawTracers()

# switch distances labels on/off
global distLabelsOn
global actualDistancesOn
distLabelsOn: int = 0
actualDistancesOn = False

# flipflop function for toggling between lines or lines + label values or lines + human-observed label values
def distLabelsToggle():
    global distLabelsOn
    global actualDistancesOn

    distLabelsOn += 1

    if (distLabelsOn >= 3):
        distLabelsOn = 0

    if (distLabelsOn == 2):
        actualDistancesOn = True
    else:
        actualDistancesOn = False

def clearDistanceText():
    for coordText in distanceTextList:
        canvas.delete(coordText)

def drawDistanceText():
    cardinalDirections = ["n", "nw", "w", "sw", "s", "se", "e", "ne"]
    distList = distanceData[1]
    xyList = distanceData[2]

    if (actualDistancesOn):
        i = 0
        for length in distList:
            if ((i % 2) == 1):
                distList[i] = int(length * 1.414)
            i += 1

    clearDistanceText()
    for index in range(0, 8):  # both distList and cardinalDirections have a length of 8
        x, y = xyList[index][0], xyList[index][1]  # Ending point (x, y)
        dist = distList[index]
        boxAnchor = cardinalDirections[index]
        # add distance text for each tracer
        coordText = canvas.create_text(x, y, text=dist, anchor=boxAnchor, fill = 'purple')
        distanceTextList.append(coordText)

# clears ANY and ALL existing lines/tracers
def clearTracers():
    for line in lineList:
        canvas.delete(line)

def drawTracers():
    clearTracers()
    clearDistanceText()
    # uses pixel endpts to draw lines to visualize the lengths each number represents
    global distLabelsOn
    global lineList
    global actualDistancesOn

    for i in range(0, 8):
        lineEndPts = distanceData[2][i]
        # Coordinates of the line's start and end points
        x1, y1 = (int(posXY[0]) + 10), (int(posXY[1]) + 10)  # Starting point (x1, y1)
        x2, y2 = lineEndPts[0], lineEndPts[1]  # Ending point (x2, y2)

        delta = 25
        if ((distLabelsOn != 0) and (((distanceData[1])[i]) > 25)):
            if (x2 > x1):
                x2 -= delta
            elif (x2 < x1):
                x2 += delta
            if (y2 > y1):
                y2 -= delta
            elif (y2 < y1):
                y2 += delta

            # if lines are of sufficient length, display arrow heads and full line lengths
            if (((distanceData[1])[i]) > 50):
                # Draw a line from (x1, y1) to (x2, y2)
                arrowVar = tk.LAST
            # if lines are NOT of sufficient length to display arrows, but long enough to be displayed, show points instead of arrows
            # for the sake of visual clarity
            else:
                point_radius = 2
                arrowVar = None
                ptID = canvas.create_oval(x2 - point_radius, y2 - point_radius, x2 + point_radius, y2 + point_radius, fill="grey", outline="grey")
                lineList.append(ptID)
            # if lines are too short (< 25 units), do not display them at all to make space for length labels in the 'h'-key toggled mode
            lineID = canvas.create_line(x1, y1, x2, y2, fill="blue", width=1, dash=(4, 2), arrow=arrowVar)
            lineList.append(lineID)

        # if not in toggled mode, display arrows to edge of wall as normal as distance labels are not displayed in this mode
        if (distLabelsOn == 0):
            # Draw a line from (x1, y1) to (x2, y2)
            lineID = canvas.create_line(x1, y1, x2, y2, fill="blue", width=1, dash=(4, 2), arrow=tk.LAST)
            lineList.append(lineID)
    
    if (distLabelsOn != 0):
        drawDistanceText()

# Bind the 'g' key using lambda to get distances anytime g is pressed
# tuple printed in terminal is in the order of (distance between left sensor and left wall,
# distance from front sensor and front wall, distance from right sensor to right wall)
window.bind('g', lambda event: wrapperFunction())

# When 'h' is pressed toggles on/off showing distance labels.
window.bind('h', lambda event: distLabelsToggle())

# Set focus on the window to receive key events
window.focus_set()

# Main loop
window.mainloop()