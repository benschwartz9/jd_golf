import ee
import webbrowser

ee.Initialize()

# Method 2 example

#Landsat_composite in Dresden area
area_dresden = list([(13.6, 50.96), (13.9, 50.96), (13.9, 51.12), (13.6, 51.12), (13.6, 50.96)])
area_dresden = ee.Geometry.Polygon(area_dresden)
time_range_dresden = ['2002-07-28', '2002-08-05']

collection_dresden = ('LANDSAT/LE07/C01/T1')
print(type(area_dresden))




def obtain_image_landsat_composite(collection, time_range, area):
    """ Selection of Landsat cloud-free composites in the Earth Engine library
    See also: https://developers.google.com/earth-engine/landsat

    Parameters:
        collection (): name of the collection
        time_range (['YYYY-MT-DY','YYYY-MT-DY']): must be inside the available data
        area (ee.geometry.Geometry): area of interest

    Returns:
        image_composite (ee.image.Image)
     """
    collection = ee.ImageCollection(collection)

    ## Filter by time range and location
    collection_time = collection.filterDate(time_range[0], time_range[1])
    image_area = collection_time.filterBounds(area)
    image_composite = ee.Algorithms.Landsat.simpleComposite(image_area, 75, 3)
    return image_composite

def obtain_image_median(collection, time_range, area):
    """ Selection of median from a collection of images in the Earth Engine library
    See also: https://developers.google.com/earth-engine/reducers_image_collection

    Parameters:
        collection (): name of the collection
        time_range (['YYYY-MT-DY','YYYY-MT-DY']): must be inside the available data
        area (ee.geometry.Geometry): area of interest

    Returns:
        image_median (ee.image.Image)
    """
    collection = ee.ImageCollection(collection)

    ## Filter by time range and location
    collection_time = collection.filterDate(time_range[0], time_range[1])
    image_area = collection_time.filterBounds(area)
    image_median = image_area.median()
    return image_median

def obtain_image_sentinel(collection, time_range, area):
    """ Selection of median, cloud-free image from a collection of images in the Sentinel 2 dataset
    See also: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2

    Parameters:
        collection (): name of the collection
        time_range (['YYYY-MT-DY','YYYY-MT-DY']): must be inside the available data
        area (ee.geometry.Geometry): area of interest

    Returns:
        sentinel_median (ee.image.Image)
     """
    #First, method to remove cloud from the image
    def maskclouds(image):
        band_qa = image.select('QA60')
        cloud_mask = ee.Number(2).pow(10).int()
        cirrus_mask = ee.Number(2).pow(11).int()
        mask = band_qa.bitwiseAnd(cloud_mask).eq(0) and(
            band_qa.bitwiseAnd(cirrus_mask).eq(0))
        return image.updateMask(mask).divide(10000)

    sentinel_filtered = (ee.ImageCollection(collection).
                            filterBounds(area).
                            filterDate(time_range[0], time_range[1]).
                            filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)).
                            map(maskclouds))

    sentinel_median = sentinel_filtered.median()
    return sentinel_median


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
composite_dresden = obtain_image_landsat_composite(collection_dresden, time_range_dresden, area_dresden)
print(1)
region_dresden = get_region(area_dresden)
print(2)
url_dresden = get_url('dresden', composite_dresden, 30, region_dresden)

print(url_dresden)