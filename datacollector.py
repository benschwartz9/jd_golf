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
        .filterBounds(ee.Geometry.Point(parameters.CenterX, parameters.CenterY))\
        .sort('CLOUD_COVER')
        #.filterBounds(ee.Geometry.Point(-86.92731360218038, 40.43057783316105))\

    if printInfo:
        print("The image collection is: " + parameters.ImageCollection)
        print("Center: " + str(parameters.CenterX) + ", " + str(parameters.CenterY))
        print("There are {} images from this point".format(img_set.size().getInfo()))
        print("The selected bands are: " + parameters.Band1 + ', ' + parameters.Band2 + ', ' + parameters.Band3)
        print("The selected region is called: " + parameters.FileName)
        print("Its points are: " + parameters.Coordinates)

    if img_set.size().getInfo() == 0:
        return None

    single_image = ee.Image(img_set.first()).select(parameters.Band1, parameters.Band2, parameters.Band3)

    return single_image


def printParameters(parameters):
    print("Parameters")
    print(f"ImageCollection: {parameters.ImageCollection}")
    print(f"Coordinates: {parameters.Coordinates}")
    print(f"Bands: {parameters.Band1}, {parameters.Band2}, {parameters.Band3}")
    print(f"Google Drive Folder: {parameters.Folder}")
    print(f"File Name: {parameters.FileName}")


def printDownloadURL(parameters, single_image):
    if not single_image:
        print(f"Unable to find image for {parameters.FileName}, {parameters.Coordinates}")
        return

    url = single_image.getDownloadURL({
        'name': (parameters.FileName + str(datetime.utcnow())),
        'scale': parameters.Scale,
        'crs': 'EPSG:3857',
        'region': parameters.Coordinates
    })

    print(url)


def exportToDrive(parameters, single_image, printSubmission=False):
    if not single_image:
        if printSubmission:
            print(f"Unable to find image for {parameters.FileName}, {parameters.Coordinates}")
        return

    DriveTask = ee.batch.Export.image.toDrive(**{
            'image': single_image,
            'description': parameters.FileName + "_" + str(datetime.utcnow()),
            'scale': parameters.Scale,
            'crs': 'EPSG:3857',
            'region': parameters.Coordinates, #single_image.geometry().bounds().getInfo()['coordinates'],
            'folder': parameters.Folder
        })
    
    DriveTask.start()

    if printSubmission:
        print(f"Submitted exportToDrive task: {parameters.FileName}, {parameters.Coordinates}")
    


