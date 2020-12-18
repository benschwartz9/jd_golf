import datacollector

class DownloadImageryParameters:
    def __init__(self):
        # Google Earth Engine
        self.ImageCollection = 'USDA/NAIP/DOQQ'
        self.Coordinates = '[[-86.93206344262272,40.43042934882771], \
                            [-86.92794356957585,40.43154001432582], \
                            [-86.91652808800846,40.43127868291773], \
                            [-86.91682849541813,40.43879155578067], \
                            [-86.93802867547184,40.43872623006948], \
                            [-86.93206344262272,40.43042934882771]]'
        self.Band1 = 'R'
        self.Band2 = 'G'
        self.Band3 = 'B'
        self.Scale = 1

        # Google Drive
        self.Folder = 'Google Earth'
        self.FileName = 'Main_Ackerman'


def unpack(file):
    filename = file.readline()
    coords = []
    while True:
        line = file.readline()
        if not line or line == "\n":
            yield filename[:-1], "[[" + "],[".join(coords) + "]]"
            if not line:
                break
            filename = file.readline()
            coords = []
        else:
            coords.append(line[:-1])


# Main
param = DownloadImageryParameters()

with open("courses.txt", "r") as file:
    for filename, coords in unpack(file):
        # Reconfigure
        param.FileName = filename
        param.Coordinates = coords

        # Run collection process
        img = datacollector.getImage(param)
        datacollector.exportToDrive(param, img, printSubmission=True)