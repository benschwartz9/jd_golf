import os
import rasterio as rio
import numpy as np
import cv2

from PIL import Image

# Method 1, convert tif to JPG

with rio.open('testExport2.tif') as infile:
    red = infile.read(1)
    red = red.astype(np.uint8)
    green = infile.read(2)
    green = green.astype(np.uint8)
    blue = infile.read(3)
    blue = blue.astype(np.uint8)
    print(f"Count: {infile.count}")


rgb = np.dstack((red,green,blue))

#cv2.imwrite('testExportAnalyzed.jpg', rgb)
img = Image.fromarray(rgb, 'RGB')
img.save('testExportAnalyzed.jpg')
