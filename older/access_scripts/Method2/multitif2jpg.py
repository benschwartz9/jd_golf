import os
import rasterio as rio
import numpy as np
import cv2

# Method 2, takes multiple tiff files and converts to a single JPG

file_name = "/Users/ben/Downloads/JD_TEMP/image_grab/image_grab"#"bottom_golf_0.6"


def saveAsSimpleImage(infile):
    # Read in as numpy array
    mask = infile.read(1) # Read first band
    #print(f"Count: {infile.count}")
    #print(f"Test: {type(mask)}")

    #Simplifies Float64 data to uint16 so it can be saved as a PNG
    mask2 = mask.astype(np.uint16)

    #cv2.imwrite('test.jpg', mask2)




with rio.open(f'{file_name}.R.tif') as infile:
    mask = infile.read(1)
    red = mask.astype(np.uint16)

with rio.open(f'{file_name}.B.tif') as infile:
    mask = infile.read(1)
    blue = mask.astype(np.uint16)

with rio.open(f'{file_name}.G.tif') as infile:
    mask = infile.read(1)
    green = mask.astype(np.uint16)

rgb = np.dstack((red,green,blue))

cv2.imwrite('test.jpg', rgb)