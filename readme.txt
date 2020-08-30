Dependencies
pip install earthengine-api --upgrade
pip install rasterio    (windows install from precompiled wheel)
pip install opencv-python
pip install Pillow

#Needed gdal and rasterio
https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal




Activate
Set-ExecutionPolicy Unrestricted -Scope Process
.\venv\Scripts\activate


Data Extract
Method 1: Used in website above to grab info to export to drive (multiple TIF files) -> download -> convert to multiple JPGs -> stitch to get final image
    https://code.earthengine.google.com/ 
Method 2: Used to grab image through code and save as .tif to local computer, -> convert and combine to JPG


(Method 2 info and TODO)
    Auth
    earthengine authenticate

    Tutorial
    https://climada-python.readthedocs.io/en/stable/tutorial/climada_util_earth_engine.html

    TODO
    getDownloadURL alternative
    return .median() instead of .first()
