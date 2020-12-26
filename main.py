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
        self.Scale = 10
        self.CenterX = -86.93206344262272
        self.CenterY = 40.43042934882771

        # Google Drive
        self.Folder = 'Google Earth'
        self.FileName = 'Main_Ackerman'


def unpack(file):
    filename = file.readline()
    coords = []
    while True:
        line = file.readline()
        if not line or line == "\n":
            centerX, centerY = float(coords[0][:coords[0].index(",")]), float(coords[0][coords[0].index(",") + 1:])
            yield filename[:-1], centerX, centerY, "[[" + "],[".join(coords[1:]) + "]]"
            if not line:
                break
            filename = file.readline()
            coords = []
        else:
            coords.append(line[:-1])


# Main
param = DownloadImageryParameters()

i = 0

with open("courses.txt", "r") as file:
    for filename, centerX, centerY, coords in unpack(file):
        
        i += 1
        if i <= 2625+3000+3000+3000+3000:
            continue

        # Reconfigure
        param.FileName = filename
        param.CenterX = centerX
        param.CenterY = centerY
        param.Coordinates = coords

        # Run collection process
        img = datacollector.getImage(param, False)
        #datacollector.printDownloadURL(param, img)
        datacollector.exportToDrive(param, img, printSubmission=True)

# earthengine task cancel all
# earthengine task list

# Took 9 hrs to do ~2k at scale of 10
# Set-ExecutionPolicy Unrestricted -Scope Process