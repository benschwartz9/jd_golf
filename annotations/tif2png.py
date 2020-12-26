import os
import rasterio as rio
import numpy as np
import cv2

from PIL import Image

# for filename in os.listdir("tif_files"):
#     with rio.open('tif_files/'+filename) as infile:
#         red = infile.read(1)
#         red = red.astype(np.uint8)
#         green = infile.read(2)
#         green = green.astype(np.uint8)
#         blue = infile.read(3)
#         blue = blue.astype(np.uint8)
#         #print(f"Count: {infile.count}")


#     rgb = np.dstack((red,green,blue))

#     #cv2.imwrite('testExportAnalyzed.jpg', rgb)
#     img = Image.fromarray(rgb, 'RGB')
#     img.save('to_sort/'+filename[:-4]+'.png') # change to remove date


# Clean files by removing dates and duplicates
from pathlib import Path

for filename in os.listdir("to_sort"):
    dateIndex = filename.find("_")
    if dateIndex == -1:
        continue

    newname = filename[:dateIndex]+".png"

    if not newname in os.listdir("to_sort"):
        Path("to_sort/"+filename).rename("to_sort/"+newname)
    else:
        os.remove("to_sort/"+filename)