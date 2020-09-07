# jd_golf


### Install from requirements.txt
pip install -r requirements.txt

### Build requirements.txt
pip freeze > requirements.txt

### Venv
source /Users/ben/OneDrive/Projects/golf/venv/bin/activate

### Data Grab (manual): Method 1
Go to https://code.earthengine.google.com/
    - Paste codeearth_rbg.js in the code editor (middle box) and run  -> allows you to see the satellite view of the golf courses
    - Draw a bounding box around one/both of the golf courses and name it "myregion"
    - Paste codeearth_extract.js in the code editor in run
    - This saves a series of .tif files to your Google Drive
Download .tif files from your Google Drive to your local machine
Run tif2jpg.py on each .tif file to convert to jpg
Stitch together jpg files using stitch_images.py to 1 final image
    - code edits in stitch_images.py will probably be needed

### Data Grab (API): Method 2
Make sure you have "pip install earthengine-api"
Run "earthengine authenticate" to authenticate session with Google Account
Run download_image.py to download .tif file
    - This process saves each band over the same area as a separate .tif file (area.R.tif = red, area.B.tif = blue)
Use multitif2jpg.py to convert to JPG


### Notes
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
