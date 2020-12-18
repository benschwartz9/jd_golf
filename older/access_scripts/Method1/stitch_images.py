from PIL import Image
import numpy as np
import cv2

# Method 1, stitch together jpg files to generate final image

def readImage(path):
    img = cv2.imread(path)   # reads an image in the BGR format
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # BGR -> RGB

def addImage(base, add, side):
    #Side 1: add to right, Side 0: add below
    if type(add) == str:
        return np.append(base, readImage(add), axis=side)
    else:
        return np.append(base, add, axis=side)


# Final Image Layout
#   Res1 Res2 Res3
#   Res4 Res5 Res6
row1 =      readImage("res1.jpg")
row1 = addImage(row1, "res2.jpg", 1)
row1 = addImage(row1, "res3.jpg", 1)

row2 =      readImage("res4.jpg")
row2 = addImage(row2, "res5.jpg", 1)
row2 = addImage(row2, "res6.jpg", 1)

final = addImage(row1, row2, 0)

img = Image.fromarray(final, 'RGB')
img.save(f'final_res.jpg')




# image_order = [
#                 ["res1.jpg", "res2.jpg", "res3.jpg"],
#                 ["res4.jpg", "res5.jpg", "res6.jpg"] 
#               ]

# for row in range(len(image_order)):
#     row_img = image_order[row][0]
#     for col in range(1, len(image_order[row])):
#         img = readImage(image_order[row][col])
#         row_img = np.append(row_img, img, axis=1) # side side
#     final = np.append(final, row_img, axis=0) #up down


# img = cv2.imread("res1.jpg")   # reads an image in the BGR format
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # BGR -> RGB

# print(img.dtype)

# img2 = cv2.imread("res2.jpg")   # reads an image in the BGR format
# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)   # BGR -> RGB

#final = np.concatenate((img, img2)) # Adds top to bottom (https://stackoverflow.com/questions/9775297/append-a-numpy-array-to-a-numpy-array)
#final = np.append(img, img2, axis=1)




