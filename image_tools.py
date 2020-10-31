import os
from PIL import Image
from numpy import asarray

# Loads image to numpy array from path
def load_image(path):
    image = Image.open(path).convert('L')
    return asarray(image).copy()

# Shows numpy array as image in system image viewer
def show_image(image_array):
    image = Image.fromarray(image_array)
    image.show()

# Resizes numpy array keeping its original aspect ratio
def resize_image(image_array, new_size):
    image = Image.fromarray(image_array)
    
    width = new_size[0]
    wpercent = (width/float(image.size[0]))
    hsize = int( ( float(image.size[1])*float(wpercent) ) )
    image = image.resize((width, hsize))

    return asarray(image).copy()