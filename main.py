from PIL import Image, ImageTk
import tkinter as tk
import image_processing
from PIL import Image, ImageTk
from image_processing import getImageCSV
import math

# Get floorplan Image
floorplan = input("Floorplan filename:") # IMPORTANT DO NOT DELETE
floorplanPath = 'floorplans/' + floorplan + '.png'

global roombaRotation
roombaRotation = 0

def update_roomba_rotation(angle_degrees):
    global roombaRotation
    roombaRotation += angle_degrees
    roombaRotation %= 360  # Ensure the angle stays within 0 to 359 degrees

def create_movable_object(x, y):
    # Create an image on the canvas
    roomba_id = canvas.create_image(x, y, anchor=tk.NW, image=tk_roomba_image)
    # Attach the PhotoImage to the canvas to prevent garbage collection
    canvas.itemconfig(roomba_id, image=tk_roomba_image)
    return roomba_id

# Movement/Rotations START
def move(event, dx, dy):
    canvas.move(object_id, dx, dy)

def rotate_image(angle_degrees):
    update_roomba_rotation(angle_degrees)
    global roomba_image, tk_roomba_image  # Declare these as global to modify them
    roomba_image = roomba_image.rotate(angle_degrees)
    tk_roomba_image = ImageTk.PhotoImage(roomba_image)
    canvas.itemconfig(object_id, image=tk_roomba_image)

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
object_id = create_movable_object(20, 20)

# Load collisions dictionary from image_processing.py
collisionsDict = getImageCSV(floorplanPath)

# Bind keys to the movement functions
window.bind("<Up>", move_forward)
window.bind("<Down>", move_back)
window.bind("<Left>", rotate_left)
window.bind("<Right>", rotate_right)

# Set focus on the window to receive key events
window.focus_set()

# Main loop
window.mainloop()