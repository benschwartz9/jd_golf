# https://towardsdatascience.com/canny-edge-detection-step-by-step-in-python-computer-vision-b49c3a2d8123ß

import numpy as np
import cv2

def apply_filter(filter_func):
    def wrapper(img): 
        height, width, channels = img.shape

        for x in range(width):
            for y in range(height):
                img[y, x] = filter_func(img, x, y)
        return img

    return wrapper


# # Greyscale Image
# def to_greyscale(img): # Numpy Array
#     height, width, channels = img.shape

#     for x in range(width):
#         for y in range(height):
#             r, g, b = img[y, x]
#             img[y, x] = 0.2126 * r + 0.7152 * g + 0.0722 * b
#             # ITU-R Recommendation BT.709

#     return img

@apply_filter
def to_greyscale(img, x, y): # Numpy Array
    r, g, b = img[y, x]

    # ITU-R Recommendation BT.709
    return 0.2126 * r + 0.7152 * g + 0.0722 * b




# Gaussian Blur
def gaussian_kernel(size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return g

