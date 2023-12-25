from PIL import Image, ImageTk

def getImageCSV(filename: str):
    img = Image.open(filename)
    img = img.convert("RGB")

    width, height = img.size

    # for 