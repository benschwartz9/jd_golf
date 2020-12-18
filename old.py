import ee
from datetime import datetime

"""
Lauren Trinks, ltrinks@purdue.edu | DMJohnDeere
"""

PrintInfo = False  # True if you want to see some info about what is being collected
URL = True  # True if you want the images as a download link
Drive = True  # True if you want it to export to drive (should export as one rgb image because of EPSG:3857)

Constellation = 'USDA/NAIP/DOQQ'
Constellation_Short = 'NAIP'

Region = '[[-86.93206344262272,40.43042934882771], \
        [-86.92794356957585,40.43154001432582], \
        [-86.91652808800846,40.43127868291773], \
        [-86.91682849541813,40.43879155578067], \
        [-86.93802867547184,40.43872623006948], \
        [-86.93206344262272,40.43042934882771]]'

Region_Name = 'Ackerman'

Band1 = 'R'
Band2 = 'G'
Band3 = 'B'

# cordsWestLafayette: -86.92698233071188, 40.43624080792704
# cordsAckerman: -86.92731360218038, 40.43057783316105

###############################################################################################################

# ee.Authenticate()
ee.Initialize()

img_set = ee.ImageCollection(Constellation)\
    .filterBounds(ee.Geometry.Point(-86.92731360218038, 40.43057783316105))\
    .filterDate('2014-07-03', '2020-01-01')\
    .sort('CLOUD_COVER')

if PrintInfo:

    print("The constellation is: " + Constellation)
    print("There are {} images from this point".format(img_set.size().getInfo()))
    print("The selected bands are: " + Band1 + ', ' + Band2 + ', ' + Band3)
    print("The selected region is called: " + Region_Name)
    print("Its points are: " + Region)


single_image = ee.Image(img_set.first()).select(Band1, Band2, Band3)

path = single_image.getDownloadURL({
    'name': (Region_Name + Constellation_Short + str(datetime.utcnow())),
    'scale': 1,
    'crs': 'EPSG:3857',
    'region': Region
})

DriveTask = ee.batch.Export.image.toDrive(**{
        'image': single_image,
        'description': Region_Name + "_" + Constellation_Short + "_" + str(datetime.utcnow()),
        'scale': 10,
        'crs': 'EPSG:3857',
        'region': Region,
        'folder': 'Google Earth'
    })

if URL:

    print(path)

if Drive:

    DriveTask.start()
    print('Exported to Google Drive successfully, image(s) will appear in a few moments.')





