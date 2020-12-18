import ee
import time 

ee.Initialize()
# https://colab.research.google.com/github/csaybar/EEwPython/blob/dev/10_Export.ipynb#scrollTo=Mzu9gkJiK0K7

#Bottom
area_site = [
                (-86.93544046924065, 40.438993721744694),
                (-86.93544046924065, 40.43102354043904),
                (-86.9154419188256, 40.43102354043904),
                (-86.9154419188256, 40.438993721744694) 
            ]
area_site = ee.Geometry.Polygon(area_site)
time_range = ['2015-08-12', '2020-08-12']
collection_site = ("USDA/NAIP/DOQQ")#("COPERNICUS/S2_SR")

def getData(collection, time_range, area):
    collection = ee.ImageCollection(collection)

    ## Filter by time range and location
    collection_time = collection.filterDate(time_range[0], time_range[1])
    image_area = collection_time.filterBounds(area)
    #true_color = image_area.select(['R', 'G', 'B'])        #choose which bands you want to return
    return image_area.first() #true_color.median()

image = getData(collection_site, time_range, area_site)
print("here")

#landsat = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_123032_20140515').select(['B4', 'B3', 'B2'])
# image = ee.ImageCollection(collection_site).filterDate(time_range[0], time_range[1])
# im2 = image.filterBounds(polygon.getInfo()["coordinates"])#.median()

# Create a geometry representing an export region.
# geometry = ee.Geometry.Rectangle([116.2621, 39.8412, 116.4849, 40.01236])
# center = geometry.centroid().getInfo()['coordinates']

# Export the image, specifying scale and region.
task = ee.batch.Export.image.toDrive(**{
    'image': image,
    'description': 'imageToDriveExample3',
    'folder':'Google Earth',
    'scale': 1,
    'region': area_site.getInfo()['coordinates']
})
task.start()


while task.active():
  print('Polling for task (id: {}).'.format(task.id))
  time.sleep(5)

print("done")