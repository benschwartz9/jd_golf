import ee
import webbrowser

ee.Initialize()


# Used to grab image through code and save as .tif to local computer, -> convert and combine to JPG (method 2)
# Different tiff file for each band, limit on quantity of data transmitted

#Overall
# area_site = [ 
            #     (-86.9370712523217, 40.45277598563428), #https://code.earthengine.google.com/#
            #     (-86.9370712523217, 40.42658073426636), #https://developers.google.com/earth-engine/geometries?hl=en
            #     (-86.91707270190666, 40.42658073426636),
            #     (-86.91707270190666, 40.45277598563428)
            # ]

# #Bottom
# area_site = [
#                 (-86.93544046924065, 40.438993721744694),
#                 (-86.93544046924065, 40.43102354043904),
#                 (-86.9154419188256, 40.43102354043904),
#                 (-86.9154419188256, 40.438993721744694) 
#             ]

#Top
# area_site = [
#                 (-86.93544046924065, 40.45192692311046),
#                 (-86.93544046924065, 40.43876508216534),
#                 (-86.9154419188256, 40.43876508216534),
#                 (-86.9154419188256, 40.45192692311046)
#             ]

#Small
area_site = [
                (-86.93544046924065, 40.438993721744694),
                (-86.93544046924065, 40.43102354043904),
                (-86.9154419188256, 40.43102354043904),
                (-86.9154419188256, 40.438993721744694) 
            ]


area_site = ee.Geometry.Polygon(area_site)
time_range_site = ['2015-08-12', '2020-08-12']

collection_site = ("USDA/NAIP/DOQQ")
print(type(area_site))



def get_region(geom):
    if isinstance(geom, ee.Geometry):
        region = geom.getInfo()["coordinates"]
    elif isinstance(geom, ee.Feature, ee.Image):
        region = geom.geometry().getInfo()["coordinates"]
    elif isinstance(geom, list):
        condition = all([isinstance(item) == list for item in geom])
        if condition:
            region = geom
    return region

def get_url(name, image, scale, region):
    path = image.getDownloadURL({
        'name':(name),
        'scale': scale,
        'region':(region)
        })

    webbrowser.open_new_tab(path)
    return path


#Application to examples
def sample(collection, time_range, area):
    collection = ee.ImageCollection(collection)

    ## Filter by time range and location

    collection_time = collection.filterDate(time_range[0], time_range[1])
    image_area = collection_time.filterBounds(area)

    #true_color = image_area.select(['R', 'G', 'B'])        #choose which bands you want to return
    return image_area.first() #true_color.median()



composite_site = sample(collection_site, time_range_site, area_site)
region_site = get_region(area_site)
url_site = get_url('bottom_golf_0.15', composite_site, 0.20, region_site)