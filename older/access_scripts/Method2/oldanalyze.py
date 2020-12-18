import os
import rasterio as rio
import numpy as np

tif_filename = 'golf/golf.B' #'dresden/dresden.B3'

# Old write to file (for method 2)

with rio.open(tif_filename + '.tif') as infile:
    print(infile.bounds)
    print(infile.res)
    print(infile.count)

    profile=infile.profile
    #
    # change the driver name from GTiff to PNG
    #
    profile['driver']='PNG'
    #
    # pathlib makes it easy to add a new suffix to a
    # filename
    #    
    png_filename=tif_filename + '.png'#tif_filename.with_suffix('.png')
    raster=infile.read()
    with rio.open(png_filename, 'w', **profile) as dst:
        dst.write(raster)