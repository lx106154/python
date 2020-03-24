'''
Software Carpentry - Grayscale function
'''
from PIL import Image
import numpy as np


def grayscale(fptr):
    '''
    Convert an image to grayscale.

    **Parameters**

        fptr: *str*
            The name of the image to be read in.

    **Returns**

        None
    '''
    # Open image and retrieve width and height (make sure pixel values are
    # converted to RGB)
    img = Image.open(fptr).convert("RGB")
    width, height = img.size
    # Use double for loop to iterate through all the pixels in the image
    for x in range(width):
        for y in range(height):
            # Get average pixel value and replace it
            pixel_value = img.getpixel((x, y))
            avg_pixel = int(np.mean(pixel_value))
            img.putpixel((x, y), (avg_pixel, avg_pixel, avg_pixel))
    # Take the original filename, remove the original file extension and add
    # the appropriate extension
    filename = '.'.join(fptr.split('.')[0:-1]) + "_grayscale.png"
    img.save(filename)


if __name__ == '__main__':
    # Input filename here
    grayscale("dog.jpg")
