import copy
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Load pattern
pattern = cv.imread('./puzzle_generator/patterns/4x4.jpg')
# Make grayscale
pattern = (0.3*pattern[:,:,2] + 0.6*pattern[:,:,1] + 0.1*pattern[:,:,0]).astype(np.uint8)
# Threshold
pattern = 255 * (pattern > 225).astype(np.uint8)
#pattern = cv.dilate(pattern, np.ones((5,5)))

cv.imshow('',pattern)
cv.waitKey(0)


contours, _ = cv.findContours(pattern, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print('Contour lengths: ', [len(i) for i in contours])

res = np.ones(pattern.shape, dtype=np.uint8) * 255
cv.drawContours(res, contours, -1, (100,100,100), thickness=cv.FILLED)
cv.imshow('',res)
cv.waitKey(0)

# Load image and cut into puzzles
img = cv.imread('./pics/seaside.jpg')
img_cols, img_rows = img.shape[:2]
pat_cols, pat_rows = pattern.shape[:2]

img = cv.resize(img, None, fy = pat_cols/img_cols, fx = pat_rows/img_rows)
img = (0.3*img[:,:,2] + 0.6*img[:,:,1] + 0.1*img[:,:,0]).astype(np.uint8) # Convert to grayscale
img = np.stack( (img, img, img, 255*np.ones(img.shape, dtype=np.uint8)) , axis=2) # Get back to color, for alpha channel

# Cut pieces
pieces = []
for i in range(len(contours)):
	mask = np.ones(pattern.shape, dtype=np.uint8)*255
	cv.drawContours(mask, contours, i, (0,0,0), thickness=cv.FILLED)

	piece = copy.deepcopy(img)
	piece[mask > 0,:] = 0
	
	cv.imshow('',piece)
	cv.waitKey(0)
	
	x,y,w,h = cv.boundingRect(contours[i])
	print(x, y, w, h)
	pieces.append(piece[y:y+h, x:x+w])

side = np.ceil(np.sqrt(len(pieces)))
for i in range(len(pieces)):
	plt.subplot(side, side, i+1), plt.imshow(pieces[i])
	cv.imwrite('piece_'+str(i)+'.png', pieces[i])
	
plt.show()
	



