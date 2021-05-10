import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('4x4_orig.jpg')
rows, cols, colors = img.shape
img = (0.3*img[:,:,2] + 0.6*img[:,:,1] + 0.1*img[:,:,0]).astype(np.uint8)
img = cv.resize(img, None, fy = 512/rows, fx = 512/cols)

img[img < 100] = 0;
img[img >= 100] = 255

img = cv.erode(img, np.ones((2,2)))

plt.imshow(img)
plt.show()
cv.imwrite('4x4.jpg', img)
