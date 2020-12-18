import ee
import numpy as np
import matplotlib.pyplot as plt
import rasterio

### The authenticate step only needs to be run once. After that you can comment it out and only run the initialize step. 
### It does require that you authorize your Google account to use Earth Engine prior to running the authentication. 
# ee.Authenticate()
ee.Initialize()

### This snipped chooses an image collection for a specific point and date range and then sorts it by how cloudy the image may be. 
### NOTE: not all images have the same parameters for things like clouds. It's a good idea to check the image set parameters to make sure you're passing the correct argument. 
points = [[-86.94031926563204,40.42723436032728],
[-86.91182347705782,40.42723436032728],
[-86.91182347705782,40.451861863876644],
[-86.94031926563204,40.451861863876644],
[-86.94031926563204,40.42723436032728]]

img_set = ee.ImageCollection('COPERNICUS/S2_SR')\
    .filterBounds(ee.Geometry.Polygon(points))\
    .filterDate('2014-07-03', '2020-01-01')\
    .sort('CLOUD_COVER')



### Prints the number of available images from the image set code above. 
print("We have {} images for this point.".format(img_set.size().getInfo()))

### Prints the bands that are available for the images. This will change based on the image types. 
print(img_set.first().bandNames().getInfo())

### If the image has information on clouds this will print how cloudy the least cloud image is (we sorted based on clouds above).
### NOTE: if you expect this to return a value and it returns None check to make sure you passed the correct parameter for clouds. 
print(img_set.first().get('CLOUD_COVER').getInfo())

### This code is primarily just for reference. It prints out the different keys that are available for each data set and then specifically the parameters that are available. 
### The parameter information can also be found in the online documentation, but sometimes it can be helpful to get to it programatically. 
print(img_set.first().getInfo().keys())
print(img_set.first().getInfo()['properties'].keys())

### Selecting the least cloudy image and the associated bands that we would like for the image set. 
### NOTE: bands also change based on the image set that you are using. Make sure to update them as needed. 
im_obj = ee.Image(img_set.first())
# print(im_obj)
print("\n---\n\n\n\n\n\n\n")
print(im_obj.bandNames().getInfo())
single_image = im_obj.select(['B2', 'B3', 'B4'])

print("\n\nnext\n")

### Get a URL to download the set of images specified in the previous line above. You don't need to worry too much about the coordinate reference system (CRS), but the region can be updated as needed. 
### NOTE: This will still give you a full satellite image. You will need to clip the image to your area of interest (aoi) for analysis. 
### NOTE2: As mentioned this method also has a limit based on the amount you are trying to download. The toDrive() funtionality may be easier to use for larger data sets. 
path = single_image.getDownloadURL({
    'scale': 20,
    'crs': 'EPSG:4326',
    'region': '[[-70.9282, 41.6151], [-70.9018, 41.6172], [-70.8958, 41.5915], [-70.9233, 41.5896], [-70.9282, 41.6151]]'
})
print(path)