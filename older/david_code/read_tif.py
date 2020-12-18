import numpy as np
import matplotlib.pyplot as plt
import rasterio as rio
import cv2

with rio.open('/Users/ben/Downloads/sentiR.tif') as infile:
    mask = infile.read(1)
    red = mask.astype(np.uint16)

with rio.open('/Users/ben/Downloads/sentiB.tif') as infile:
    mask = infile.read(1)
    blue = mask.astype(np.uint16)

with rio.open('/Users/ben/Downloads/sentiG.tif') as infile:
    mask = infile.read(1)
    green = mask.astype(np.uint16)

rgb = np.dstack((red,green,blue))
print(rgb[20,0])

cv2.imwrite('test.jpg', rgb)

# Single channel
# with rio.open('/Users/ben/Downloads/senti.tif') as infile:
#     print(infile)
#     data = infile.read(1)
#     height, width = data.shape
#     # for y in 
#     print(data[1, 0])
#     for y in range(height):
#         print(data[y])
#     print(f"Count: {infile.count}")
