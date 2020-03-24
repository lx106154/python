'''
EN.640.635 Software Carpentry
Lab 2 - PIL Image Blurring and Luminance
Completed by: Zhezhi Chen
In this lab assignment, we want to write two functions that can manipulate
images: one to blur the image and one to set the luminance (or brightness) of
the image.
'''
from PIL import Image
import numpy as np

def blur(fptr, mask=3):
    '''
    Apply a blur to an image. Saves both the original image and the
    newly-blurred image.

    **Parameters**

        fptr: *str*
            The name of an image file, with its extension
            (ex. spring.jpg, cat.png).
        mask: *int, optional*
            The size of our kernel mask.

    **Returns**

        None

    For extra info:

        *https://www.youtube.com/watch?v=C_zFhWdM4ic
    '''

    # We can open two images seperately, and only change img (thus, keeping
    # the original image unchanged for calculation purposes).
    # Note - we convert to RGB to circumvent some issues with different
    # file formats.
    original_img = Image.open(fptr).convert("RGB")
    img = Image.open(fptr).convert("RGB")

    width, height = img.size

    for x in range(width):
        for y in range(height):

            pxl = img.getpixel((x, y))
            lst = []
            # Setup the range limit for mask
            xi_lowest = max(0, x - mask)
            xi_highest = min(x + mask, width - 1)
            yi_lowest = max(0, y - mask)
            yi_highest = min(y + mask, height - 1)

            for xi in range(xi_lowest, xi_highest):
                for yi in range(yi_lowest, yi_highest):
                    lst.append(img.getpixel((xi, yi)))

            lst_np = np.array(lst)

            blur = tuple(sum(lst_np) // len(lst))

            img.putpixel((x, y), blur)

    # Save both images so we can verify if we changed the correct one.
    base_name = '.'.join(fptr.split(".")[0:-1])
    fptr_2 = base_name + "_blurred.png"
    img.save(fptr_2)
    fptr_2 = base_name + "_original.png"
    original_img.save(fptr_2)


def set_luminance(fptr, l_val):
    '''
    Luminance is a method of determining how "bright" the image is. It can
    be easily calculated per pixel with the following formula:

        l_pxl = 0.299 * R + 0.587 * G + 0.114 * B

    Now, for an entire image we can calculate either the total luminance, or
    the average luminance over the whole image:

        l_avg = sum(l_pxl) / N_pxl

    We want to set the luminance of an image to a user specified value,
    allowing us to essentially set how bright our image is. We can use the
    get_pxl_luminance() and get_luminance() functions below to help us.

    **Parameters**

        fptr: *str*
            The name of an image file, with its extension
            (ex. spring.jpg, cat.png).
        l_val: *float*
            The desired luminance to set the image to.

    **Returns**

        None
    '''
    img = Image.open(fptr).convert("RGB")
    # Calculate the total luminace of the image
    total_lum = get_luminance(img)

    # Calculate the multiplier
    multiplier = l_val / total_lum

    # Reset the RGB value for each pixel
    width, height = img.size
    for x in range(width):
        for y in range(height):
            pxl = img.getpixel((x, y))
            red = min(255, round(pxl[0] * multiplier))
            green = min(255, round(pxl[1] * multiplier))
            blue = min(255, round(pxl[2] * multiplier))
            pxl_lum = (red, green, blue)
            img.putpixel((x, y), pxl_lum)

    # Save the new image
    base_name = '.'.join(fptr.split(".")[0:-1])
    fptr_2 = base_name + "_luminated.png"
    img.save(fptr_2)


def get_pxl_luminance(pxl):
    '''
    Given a pixel, this function will calculate its luminance.

    **Parameters**

        pxl: *tuple, int*
            A tuple of integers holding RGB values.

    **Returns**

        l_val: *float*
            The pixel luminance.
    '''
    l_pxl = 0.299 * pxl[0] + 0.587 * pxl[1] + 0.114 * pxl[2]
    return l_pxl



def get_luminance(img):
    '''
    Returns the average luminance of an image.

    **Parameters**

        img: *PIL.Image*
            A PIL image object.

    **Returns**

        l_val: *float*
            The image luminance.
    '''

    width, height = img.size
    pxl_lst = []
    for x in range(width):
        for y in range(height):
            pxl_lst.append(get_pxl_luminance(img.getpixel((x, y))))

    l_val = sum(pxl_lst) / len(pxl_lst)
    return l_val

if __name__ == "__main__":
    fptr = "dog.jpg"
    blur(fptr)
    set_luminance(fptr, 150.0)
