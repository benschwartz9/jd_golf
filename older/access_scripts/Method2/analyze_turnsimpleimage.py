# Old, method 2, test writing to a jpg file with TIF info

import os
import rasterio as rio
import numpy as np
import cv2

tif_filename = 'golf/golf.B' #'dresden/dresden.B3'


def saveAsSimpleImage(infile):
    # Read in as numpy array
    print(f"Count: {infile.count}")
    mask = infile.read(1) # Read first band
    print(f"Test: {type(mask)}")

    print(mask[0,0])

    #Simplifies Float64 data to uint16 so it can be saved as a PNG
    mask2 = mask.astype(np.uint16)

    cv2.imwrite('test.jpg', mask2)





with rio.open(tif_filename + '.tif') as infile:
    print(infile.bounds)
    print(infile.res)
    print(infile.count)

    profile=infile.profile
    #
    # change the driver name from GTiff to PNG
    #
    profile['driver']='PNG'
    profile['dtype'] = 'uint16'
    print(profile)

    mask = infile.dataset_mask()
    mask2 = mask.astype(np.uint16)

    saveAsSimpleImage(infile)
    #
    # pathlib makes it easy to add a new suffix to a
    # filename
    #    
    # png_filename=tif_filename + '.png'#tif_filename.with_suffix('.png')
    # raster=infile.read()
    # with rio.open(png_filename, 'w', **profile) as dst:
    #     dst.write(mask)

