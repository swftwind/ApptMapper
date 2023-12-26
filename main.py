import math
import tkinter as tk
import image_processing
from PIL import Image, ImageTk
from PIL import Image, ImageTk
from image_processing import getImageJSON

#Floorplan START
floorplan = input("Floorplan filename:") # IMPORTANT DO NOT DELETE
floorplanPath = 'floorplans/' + floorplan + '.png'
floorJSON = getImageJSON(floorplanPath)
#Floorplan END

global roombaRotation
# degrees of rotation based on the roomba starting out facing north/up.
# #left is positive and right is negative, but the number is always calculated to be between 0 and 359 degrees.
roombaRotation = 0

def check_for_wall(dx, dy):
    # check if the pixel at the position i want to move to contains a wall, by checking floorJSON with the given coordinates.
    # #currently centered on the top left of the roomba and does not account for height/width of the image.
    x, y = canvas.coords(roombaObj)
    x, y = map(int, (x + dx, y + dy)) # adds the future/requested coordinates to the current coordinates
    if floorJSON.get(f"({x}, {y})") == "W": # checks if the new coordinates contain a wall
        return True
    else:
        return False

def update_roomba_rotation(angle_degrees):
    global roombaRotation
    roombaRotation += angle_degrees
    roombaRotation %= 360 # Ensure the angle stays within 0 to 359 degrees

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
    #print(dx, dy)
    if not check_for_wall(dx, dy):
        canvas.move(roombaObj, dx, dy)

def rotate_image(angle_degrees):
    update_roomba_rotation(angle_degrees)
    global roomba_image, tk_roomba_image  # Declare these as global to modify them
    roomba_image = roomba_image.rotate(angle_degrees)
    tk_roomba_image = ImageTk.PhotoImage(roomba_image)
    canvas.itemconfig(roombaObj, image=tk_roomba_image)

def move_forward(event):
    angle_rad = math.radians(roombaRotation)
    move(event, -1 * math.sin(angle_rad), -1 * math.cos(angle_rad))

def move_back(event):
    angle_rad = math.radians(roombaRotation)
    move(event, math.sin(angle_rad), math.cos(angle_rad))

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
roombaObj = create_movable_object(200, 200)

# Bind keys to the movement functions
window.bind("<Up>", move_forward)
window.bind("<Down>", move_back)
window.bind("<Left>", rotate_left)
window.bind("<Right>", rotate_right)

# Set focus on the window to receive key events
window.focus_set()

# Main loop
window.mainloop()