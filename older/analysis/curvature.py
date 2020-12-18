import cv2
import numpy as np
#from scipy.ndimage.interpolation import shift
import math
import matplotlib.pyplot as plt

base_img = cv2.imread('data/box.jpg')

def calcCurvature(contour): 
    # Converts a np array of points to a n-vector array of the curvature at each point
    # https://stackoverflow.com/questions/32629806/how-can-i-calculate-the-curvature-of-an-extracted-contour-by-opencv
    
    # print(vecCurve.shape)
    # print(contour.shape) 
    #vecCurve = np.empty((contour.shape[0], 1, 1))
    #prev = shift(contour, 1, cval=0)
    
    vecCurve = []

    prevOlderX, prevOlderY = contour[0][0][0], contour[0][0][1] # Grab first x and y
    prevX, prevY = prevOlderX, prevOlderY
    for point in contour:
        print(point)
        x = point[0][0]
        y = point[0][1]
        firstDerivX = x - prevX
        firstDerivY = y - prevY
        secondDerivX = -x + 2 * prevX - prevOlderX
        secondDerivY = -y + 2 * prevY - prevOlderY
        
        if secondDerivX + secondDerivY != 0:
        #if abs(secondDerivX) > 10 ** -4 and abs(secondDerivY) > 10 ** -4:
            curv = math.sqrt(abs( 
                math.pow(secondDerivY*firstDerivX - secondDerivX*firstDerivY, 2) 
                / math.pow(secondDerivX + secondDerivY, 3)
            ))
        else:
            curv = 0

        vecCurve.append(curv)

        prevOlderX, prevOlderY = prevX, prevY
        prevX, prevY = x, y

    plt.plot(vecCurve)
    plt.show()
    return np.mean(vecCurve)

img_flat = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
_, img_bin = cv2.threshold(img_flat, 240, 255, cv2.THRESH_BINARY_INV)
contours, heirarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
res = cv2.drawContours(base_img, contours, -1, (0, 0, 255), 3) 
cv2.imwrite("temp.jpg", base_img)

curv = calcCurvature(contours[0])
print(f"\nOutput Curvature: {curv}")