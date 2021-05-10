import cv2 as cv
import numpy as np

img = cv.imread('2x2_orig.jpg')
rows, cols, colors = img.shape
img = (0.3*img[:,:,2] + 0.6*img[:,:,1] + 0.1*img[:,:,0]).astype(np.uint8)
img = cv.resize(img, None, fy = 512/rows, fx = 512/cols)


cv.imwrite('2x2.jpg', img)
