import numpy as np
import canny as cn
import cv2
import math
from PIL import Image

# img = cv2.imread('data/ackerman.jpg')
# edges = cv2.Canny(img,20,100)

# im = Image.fromarray(edges)
# im.save("temp.jpg")

base_img = cv2.imread('data/ackerman.jpg')

def saveImage(image_save, name):
    im = Image.fromarray(image_save)
    im.save(name)

#https://www.geeksforgeeks.org/filter-color-with-opencv/
#https://docs.opencv.org/master/df/d9d/tutorial_py_colorspaces.html
def removeGreen(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    lower_green = np.array([30,50,50]) # define range of green color in HSV
    upper_green = np.array([140,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green) # Threshold the HSV image to get only green colors
    saveImage(mask, "mask.jpg")
    res = cv2.bitwise_and(img,img, mask= mask) # Bitwise-AND mask and original image
    return res

#https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
def increaseContrast(img):
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # hsv = np.multiply(hsv, 1.2).astype(np.uint8)
    # hsv[:,:,0] = np.clip(hsv[:,:,0], 0, 179)
    # hsv[hsv > 255] = 255 #OpenCV uses H: 0-179, S: 0-255, V: 0-255
    # return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    contrast = 1.4
    brightness = -0.1
    out = cv2.addWeighted(img, contrast, img, 0, brightness)
    return out

def filterByGreyscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    saveImage(gray, "gray.jpg")
    _, mask = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
    cv2.imwrite("mask2.jpg", mask)
    res = cv2.bitwise_and(base_img,base_img, mask=mask)
    return res

def calcCurvature(contour):     
    vecCurve = []

    prevOlderX, prevOlderY = contour[0][0][0], contour[0][0][1] # Grab first x and y
    prevX, prevY = prevOlderX, prevOlderY
    for point in contour:
        x = point[0][0]
        y = point[0][1]
        firstDerivX = x - prevX
        firstDerivY = y - prevY
        secondDerivX = -x + 2 * prevX - prevOlderX
        secondDerivY = -y + 2 * prevY - prevOlderY
        
        if secondDerivX + secondDerivY != 0:
            curv = math.sqrt(abs( 
                math.pow(secondDerivY*firstDerivX - secondDerivX*firstDerivY, 2) 
                / math.pow(secondDerivX + secondDerivY, 3)
            ))
        else:
            curv = 0

        vecCurve.append(curv)

        prevOlderX, prevOlderY = prevX, prevY
        prevX, prevY = x, y
    return np.mean(vecCurve)

img = removeGreen(base_img)
saveImage(img, "temp2.jpg")
img = increaseContrast(img)
saveImage(img, "temp25.jpg")

img = filterByGreyscale(img)
kernel = np.ones((5,5),np.uint8)
#img2 = cv2.erode(img, kernel, iterations=6)
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=8)

#saveImage(img, "temp3.jpg")

img_flat = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to single channel for findcontours
_, img_bin = cv2.threshold(img_flat, 1, 255, cv2.THRESH_BINARY)
cv2.imwrite("temp3.jpg", img_bin)

contours, heirarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_contours = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 20000:
        continue

    # Shape factor to remove squares - https://answers.opencv.org/question/171583/eliminate-unwanted-contours-opencv/
    perimeter = cv2.arcLength(cnt, True)
    shape_factor = (4 * math.pi * area) / (perimeter ** 2)
    if shape_factor > 0.4:
        continue

    # Filter out water using color of contour?
    #https://stackoverflow.com/questions/54316588/get-the-average-color-inside-a-contour-with-open-cv/54317652
    curvature = calcCurvature(cnt)
    print(curvature)
    if curvature > 4:
        print("go")
        cv2.drawContours(base_img, [cnt], -1, (255, 0, 0), 10) 
        continue


    filtered_contours.append(cnt)

#print(filtered_contours)
#print(len(contours))
#print(len(filtered_contours))

res = cv2.drawContours(base_img, filtered_contours, -1, (0, 0, 255), 5) 

cv2.imwrite("temp4.jpg", base_img)