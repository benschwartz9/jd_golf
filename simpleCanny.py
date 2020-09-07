import numpy as np
import canny as cn
import cv2
from PIL import Image

# img = cv2.imread('data/person.jpg')
# edges = cv2.Canny(img,50,200)

# im = Image.fromarray(edges)
# im.save("temp.jpg")

img = cv2.imread('data/kampen.jpg')
edges = cv2.Canny(img,40,80)

im = Image.fromarray(edges)
im.save("temp.jpg")