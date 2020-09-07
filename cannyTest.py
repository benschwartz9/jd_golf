import numpy as np
import canny as cn
import cv2
from PIL import Image

# Read image
img = cv2.imread("data/ackerman.jpg") # Reads in as numpy.ndarray
height, width, channels = img.shape

print(type(img))

img = cn.to_greyscale(img)

im = Image.fromarray(img)
im.save("temp.jpg")

# # Blur
# # for row in range(height):
# #     for col in range(width):
# #         
# #         img[row, col] = [0, 255, 0]

# #https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
# #img = cv2.GaussianBlur(img, (5,5), 0)


# ## Sobel filtering
# laplacian = cv2.Laplacian(img,cv2.CV_64F)
# sobelx64f = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
# sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

# # converting back to uint8
# abs_64f = np.absolute(laplacian)
# img = np.uint8(abs_64f)

# # thinning
# def non_max_suppression(img, D):
#     M, N = img.shape[:2]
#     Z = np.zeros((M,N), dtype=np.int32)
#     angle = D * 180. / np.pi
#     angle[angle < 0] += 180

    
#     for i in range(1,M-1):
#         for j in range(1,N-1):
#             try:
#                 q = 255
#                 r = 255
                
#                #angle 0
#                 if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
#                     q = img[i, j+1]
#                     r = img[i, j-1]
#                 #angle 45
#                 elif (22.5 <= angle[i,j] < 67.5):
#                     q = img[i+1, j-1]
#                     r = img[i-1, j+1]
#                 #angle 90
#                 elif (67.5 <= angle[i,j] < 112.5):
#                     q = img[i+1, j]
#                     r = img[i-1, j]
#                 #angle 135
#                 elif (112.5 <= angle[i,j] < 157.5):
#                     q = img[i-1, j-1]
#                     r = img[i+1, j+1]

#                 if (img[i,j] >= q) and (img[i,j] >= r):
#                     Z[i,j] = img[i,j]
#                 else:
#                     Z[i,j] = 0

#             except IndexError as e:
#                 pass
    
#     return Z

# img = non_max_suppression(img, 0)

