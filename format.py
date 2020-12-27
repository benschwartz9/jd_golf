import re

long_radius = 0.02
lat_radius = 0.01

def filterTitle(title):
    return "".join(x for x in title if x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:_- ")[:100]


# with open("courses.txt", "w") as outfile:
#     with open("Golf Courses-USA.csv", "r") as infile:
        
#         for line in infile.readlines():
#         #for i in range(20):
#         #    line = infile.readline()

#             ind1 = line.index(",")
#             ind2 = line.index(",", ind1 + 1)

#             long = float(line[:ind1])
#             lat = float(line[ind1+1:ind2])
#             title = filterTitle(line[ind2+2:line.index('"',ind2+2)])

#             downlat = lat - lat_radius
#             uplat = lat + lat_radius
#             rightlong = long + long_radius
#             leftlong = long - long_radius

#             #print(long, lat, title)
#             outfile.write(title + "\n")
#             outfile.write(f"{long},{lat}\n") #Center
#             outfile.write(f"{leftlong},{uplat}\n") # Square
#             outfile.write(f"{rightlong},{uplat}\n")
#             outfile.write(f"{rightlong},{downlat}\n")
#             outfile.write(f"{leftlong},{downlat}\n")
#             outfile.write(f"{leftlong},{uplat}\n") # Repeat
#             outfile.write("\n")



# Ackerman-Allen
# -86.93206344262272,40.43042934882771
# -86.92794356957585,40.43154001432582
# -86.91652808800846,40.43127868291773
# -86.91682849541813,40.43879155578067
# -86.93802867547184,40.43872623006948
# -86.93206344262272,40.43042934882771

# Kampen
# -86.93544046924065,40.43876508216534
# -86.9154419188256,40.43876508216534
# -86.9154419188256,40.45192692311046
# -86.93544046924065,40.45192692311046
# -86.93544046924065,40.43876508216534



# Getting the names & coordinates of the keep files that weren't in new_courses_backup.txt
from pathlib import Path
import os

keep_files = []

with open("annotations/new_courses_backup.txt", "r") as f:
    extracted = f.read()
    for filename in os.listdir("annotations/keep"):
        filename = filename[:-4]
        if filename not in extracted:
            keep_files.append(filename)
        # else:
        #     print(filename)


writeLeft = 0
ignore = False

with open("base_courses.txt", "r") as infile:
    with open("keep_courses_restof.txt", "w") as outfile:
        for line in infile.readlines():            
            # if ignore:
            #     continue
            # ignore = not ignore

            if writeLeft > 0:
                outfile.write(line)
                writeLeft -= 1
            elif line[:-1] in keep_files:
                outfile.write(line)
                writeLeft = 7        



        # line = infile.readline()
        
        # while line:
        #     print(line)
        #     if line[:-1] in keep_files:
        #         print(3)
        #         outfile.write(line)
        #         for _ in range(7):
        #             line = infile.readline()
        #             outfile.write(line)
        #         outfile.flush()

