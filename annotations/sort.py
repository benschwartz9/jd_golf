# import cv2

# im = cv2.imread('testExportAnalyzed.jpg')
# cv2.imshow('tet', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import PySimpleGUI as sg

# layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

# # Create the window
# window = sg.Window("Demo", layout, margins=(450,300))

# # Create an event loop
# while True:
#     event, values = window.read()
#     # End program if user closes window or
#     # presses the OK button
#     if event == "OK" or event == sg.WIN_CLOSED:
#         break

# window.close()




# img_viewer.py

import PySimpleGUI as sg
import os.path
from pathlib import Path
from PIL import Image
import base64
import io


orig_lat_radius = 0.01 # from format.py, to keep the original image
orig_long_radius = 0.02 



def getResizedImage(filename):
    global curWidth, curHeight
    # with open(filename, 'rb') as binary_file:
    #     data = binary_file.read()
    
    # return base64.b64encode(data)
    im = Image.open(filename)
    width, height = im.size
    ratio = int(1000 / max(width, height))
    im = im.resize((width*ratio, height*ratio), Image.ANTIALIAS)
    curWidth, curHeight = width, height
    buf = io.BytesIO() #https://jdhao.github.io/2019/07/06/python_opencv_pil_image_to_bytes/
    im.save(buf, format='PNG')
    data = buf.getvalue()

    return base64.b64encode(data)


def genNextFile():
    for file_dir in os.listdir("to_sort"):
        yield file_dir

def genDatabase(filename):
    db = {}
    name = None
    coords = None
    with open(filename, "r") as file:
        for line in file.readlines():
            if line == "\n":
                name, coords = None, None
                continue

            if not name:
                name = line[:-1]
                continue

            if not coords:
                comma = line.index(",")
                coords = (float(line[:comma]), float(line[comma+1:-1]))
                db[name] = coords
    
    return db

coord_database = genDatabase("../courses.txt")

gen = genNextFile()
curFile = next(gen)
prevFiles = []
prevWrites = []
curWidth, curHeight = None, None

# ----- Full layout -----
image_viewer_column = [
        [sg.Text("Image Reader", key='-LABEL-', justification='center', size=(100,1))],
        #[sg.Image(key="-IMAGE-", filename="to_sort/"+curFile)],
        [sg.Graph(canvas_size=(800, 600), graph_bottom_left=(0, 250), graph_top_right=(450, 0), key='-GRAPH-',
              change_submits=True, drag_submits=True, enable_events=True)],
        [sg.Button("Undo", key='-UNDO-', size=(100,1))]
]

image_history_column = [
    [sg.Text("Previous Images", justification='center', size=(40,1))],
    [
            sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-PREVIOUS-"
        )
    ]
]

layout = [
    [
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(image_history_column),
    ]
]

window = sg.Window("Image Viewer", layout, margins=(0,0), resizable=True, return_keyboard_events=True)

window.Finalize()

graph = window.Element("-GRAPH-")
label = window.Element("-LABEL-")
history = window.Element("-PREVIOUS-")
#graph.DrawImage(filename="to_sort/"+curFile, location=(0,0))
drawn_image = graph.DrawImage(data=getResizedImage("to_sort/"+curFile), location=(0,0))
label.Update(curFile)

startDrag = None
endDrag = None
rectangle = None

prevEvent = None


with open("new_courses.txt", "a") as outfile:
    with open("new_courses_backup.txt", "a") as outfile2:
        while True:
            event, values = window.read()

        #     # End program if user closes window or
        #     # presses the OK button
            if event == sg.WIN_CLOSED:
                break

            if startDrag and endDrag:
                if rectangle:
                    graph.DeleteFigure(rectangle)
                rectangle = graph.DrawRectangle(startDrag, endDrag, line_color="red")

            if event in ("1"): # Keep
                Path("to_sort/"+curFile).rename("keep/"+curFile)
                prevFiles = [curFile] + prevFiles[0:9]
                history.Update(values=prevFiles)

                # Submission
                clong, clat = coord_database[curFile[:-4]]
                if clong and clat:
                    if startDrag and endDrag:
                        downlat = clat + 0.00008968609 * (max(startDrag[1], endDrag[1]) - curHeight/2)
                        uplat = clat + 0.00008968609 * (min(startDrag[1], endDrag[1]) - curHeight/2)
                        leftlong = clong + 0.00008968609 * (min(startDrag[0], endDrag[0]) - curWidth/2)
                        rightlong = clong + 0.00008968609 * (max(startDrag[0], endDrag[0]) - curWidth/2)
                        
                        # Extra buffer
                        downlat -= 0.005
                        uplat += 0.005
                        leftlong -= 0.005
                        rightlong += 0.005
                    else:
                        # Use backup if box not selected
                        downlat = clat - orig_lat_radius
                        uplat = clat + orig_lat_radius
                        rightlong = clong + orig_long_radius
                        leftlong = clong - orig_long_radius

                    write1 = curFile + "\n"
                    write1 += f"{clong},{clat}\n"
                    write1 += f"{leftlong},{uplat}\n"
                    write1 += f"{rightlong},{uplat}\n"
                    write1 += f"{rightlong},{downlat}\n"
                    write1 += f"{leftlong},{downlat}\n"
                    write1 += f"{leftlong},{uplat}\n"
                    write1 +="\n"

                    downlat = clat - orig_lat_radius
                    uplat = clat + orig_lat_radius
                    rightlong = clong + orig_long_radius
                    leftlong = clong - orig_long_radius

                    write2 = curFile+"\n"
                    write2 += f"{clong},{clat}\n"
                    write2 += f"{leftlong},{uplat}\n"
                    write2 += f"{rightlong},{uplat}\n"
                    write2 += f"{rightlong},{downlat}\n"
                    write2 += f"{leftlong},{downlat}\n"
                    write2 += f"{leftlong},{uplat}\n"
                    write2 += "\n"

                    if len(prevWrites) >= 10 and prevWrites[9]:
                        outfile.write(prevWrites[9][0])
                        outfile2.write(prevWrites[9][1])
                    prevWrites = [(write1, write2)] + prevWrites[0:9]
                #

                startDrag, endDrag = None, None
                graph.DeleteFigure(rectangle)
                graph.DeleteFigure(drawn_image)

                curFile = next(gen)
                
                drawn_image = graph.DrawImage(data=getResizedImage("to_sort/"+curFile), location=(0,0))
                label.Update(curFile)
                
                #drawn_image = graph.DrawImage(filename="to_sort/"+curFile, location=(0,0))
                #window["-IMAGE-"].update(filename="to_sort/"+curFile)

            if event in ("0"): # Remove
                Path("to_sort/"+curFile).rename("delete/"+curFile)
                prevFiles = [curFile] + prevFiles[0:9]
                prevWrites = [None] + prevWrites[0:9]
                history.Update(values=prevFiles)

                startDrag, endDrag = None, None
                graph.DeleteFigure(rectangle)
                graph.DeleteFigure(drawn_image)

                curFile = next(gen)
                drawn_image = graph.DrawImage(data=getResizedImage("to_sort/"+curFile), location=(0,0))
                label.Update(curFile)
                
                #drawn_image = graph.DrawImage(filename="to_sort/"+curFile, location=(0,0))
                #window["-IMAGE-"].update(filename="to_sort/"+curFile)

            if event in ("9", "-UNDO-"):
                if len(prevFiles) > 0:
                    curFile = prevFiles[0]
                    prevFiles.pop(0)
                    prevWrites.pop(0)
                    history.Update(values=prevFiles)

                    if curFile in os.listdir("keep"):
                        Path("keep/"+curFile).rename("to_sort/"+curFile)
                    else:
                        Path("delete/"+curFile).rename("to_sort/"+curFile)

                    graph.DeleteFigure(drawn_image)
                    drawn_image = graph.DrawImage(data=getResizedImage("to_sort/"+curFile), location=(0,0))
                    label.Update(curFile)
            
            if event in ("-GRAPH-"):
                if not startDrag:
                    startDrag = values['-GRAPH-']
                else:
                    endDrag = values['-GRAPH-']
            
            if event in ("-GRAPH-+UP") and prevEvent == "-GRAPH-+UP": # Reset drag
                startDrag = None
                endDrag = None
            
            prevEvent = event

        for info in prevWrites:
            if info:
                outfile.write(info[0])
                outfile2.write(info[1])
    

window.close()


# Run the Event Loop
# while True:
#     event, values = window.read()
#     if event == "Exit" or event == sg.WIN_CLOSED:
#         break
#     # Folder name was filled in, make a list of files in the folder
#     if event == "-FOLDER-":
#         folder = values["-FOLDER-"]
#         try:
#             # Get list of files in folder
#             file_list = os.listdir(folder)
#         except:
#             file_list = []

#         fnames = [
#             f
#             for f in file_list
#             if os.path.isfile(os.path.join(folder, f))
#             and f.lower().endswith((".png", ".gif"))
#         ]
#         window["-FILE LIST-"].update(fnames)
#     elif event == "-FILE LIST-":  # A file was chosen from the listbox
#         try:
#             filename = os.path.join(
#                 values["-FOLDER-"], values["-FILE LIST-"][0]
#             )
#             window["-TOUT-"].update(filename)
#             window["-IMAGE-"].update(filename=filename)

#         except:
#             pass

# window.close()
