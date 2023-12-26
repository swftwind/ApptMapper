import tkinter as tk
import image_processing
from PIL import Image, ImageTk
from image_processing import getImageCSV

def move_up(event):
    canvas.move(object_id, 0, -1)  # Move object up

def move_down(event):
    canvas.move(object_id, 0, 1)  # Move object down

def move_left(event):
    canvas.move(object_id, -1, 0)  # Move object left

def move_right(event):
    canvas.move(object_id, 1, 0)  # Move object right

pathPrefix = 'floorplans/'
pathSuffix = '.png'
floorplan = input("Floorplan filename:")
floorplanPath = pathPrefix + floorplan + pathSuffix

# Load your apartment layout image
layout_image = Image.open(floorplanPath)

# Create a basic GUI window using Tkinter
window = tk.Tk()
canvas = tk.Canvas(window, width=layout_image.width, height=layout_image.height)
canvas.pack()

# Display the image in the GUI
tk_image = ImageTk.PhotoImage(layout_image)
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

# Create a movable object, e.g., a rectangle
object_id = canvas.create_oval(20, 20, 10, 10, fill="blue")  # Adjust size and color as needed

# Load collisions dictionary from image_processing.py
collisionsDict = getImageCSV(floorplanPath)

# Bind keys to the movement functions
window.bind("<Up>", move_up)
window.bind("<Down>", move_down)
window.bind("<Left>", move_left)
window.bind("<Right>", move_right)

# Set focus on the window to receive key events
window.focus_set()

# Main loop
window.mainloop()