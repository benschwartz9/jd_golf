# Lauren Trinks, ltrinks@purdue.edu | DMJohnDeere

import ee
from datetime import datetime


# Constellation = 'USDA/NAIP/DOQQ'
# Constellation_Short = 'NAIP'

# Region = '[[-86.93206344262272,40.43042934882771], \
#         [-86.92794356957585,40.43154001432582], \
#         [-86.91652808800846,40.43127868291773], \
#         [-86.91682849541813,40.43879155578067], \
#         [-86.93802867547184,40.43872623006948], \
#         [-86.93206344262272,40.43042934882771]]'

# Region_Name = 'Ackerman'

# Band1 = 'R'
# Band2 = 'G'
# Band3 = 'B'

# cordsWestLafayette: -86.92698233071188, 40.43624080792704
# cordsAckerman: -86.92731360218038, 40.43057783316105

###############################################################################################################

# ee.Authenticate()
ee.Initialize()

def getImage(parameters, printInfo=False):
    img_set = ee.ImageCollection(parameters.ImageCollection)\
        .filterDate('2014-07-03', '2020-01-01')\
        .filterBounds(ee.Geometry.Point(-86.92731360218038, 40.43057783316105))\
        .sort('CLOUD_COVER')
        

    if printInfo:
        print("The image collection is: " + parameters.ImageCollection)
        print("There are {} images from this point".format(img_set.size().getInfo()))
        print("The selected bands are: " + parameters.Band1 + ', ' + parameters.Band2 + ', ' + parameters.Band3)
        print("The selected region is called: " + parameters.FileName)
        print("Its points are: " + parameters.Coordinates)

    single_image = ee.Image(img_set.first()).select(parameters.Band1, parameters.Band2, parameters.Band3)
    return single_image


def printParameters(parameters):
    print("Parameters")
    print(f"ImageCollection: {parameters.ImageCollection}")
    print(f"Coordinates: {parameters.Coordinates}")
    print(f"Bands: {parameters.Band1}, {parameters.Band2}, {parameters.Band3}")
    print(f"Google Drive Folder: {parameters.Folder}")
    print(f"File Name: {parameters.FileName}")


def getDownloadURL(parameters, single_image):
    url = single_image.getDownloadURL({
        'name': (parameters.FileName + str(datetime.utcnow())),
        'scale': parameters.Scale,
        'crs': 'EPSG:3857',
        'region': parameters.Coordinates
    })

    return url


def exportToDrive(parameters, single_image, printSubmission=False):
    DriveTask = ee.batch.Export.image.toDrive(**{
            'image': single_image,
            'description': parameters.FileName + "_" + str(datetime.utcnow()),
            'scale': parameters.Scale,
            'crs': 'EPSG:3857',
            'region': parameters.Coordinates,
            'folder': parameters.Folder
        })
    
    DriveTask.start()

    if printSubmission:
        print(f"Submitted exportToDrive task: {parameters.FileName}, {parameters.Coordinates}")
    
