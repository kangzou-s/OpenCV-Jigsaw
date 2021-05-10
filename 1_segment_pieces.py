# This script should take an image of the unsolved puzzle from ./puzzle_generator
# and output N smaller images, each containing one piece to folder ./segmented
import copy
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt #import function library which will be used 

#part1 Pretreatment
pattern = cv.imread('./puzzle_generator/puzzle_unsolved.jpg')
pre = cv.imread('./puzzle_generator/puzzle_unsolved.jpg')

#Extract background
pattern = cv.cvtColor(pattern,cv.COLOR_BGR2HSV)
lower_green = np.array([45,50,50])
upper_green = np.array([81,255,255])
mask1 = cv.inRange(pattern,lower_green,upper_green)
res = cv.bitwise_and(pattern,pattern, mask= mask1)
pattern = cv.cvtColor(res,cv.COLOR_HSV2BGR)

#change to binary image and make filter
pattern = (0.3*pattern[:,:,2] + 0.6*pattern[:,:,1] + 0.1*pattern[:,:,0]).astype(np.uint8)
pattern = 255 * (pattern < 142).astype(np.uint8)

kernel = np.ones((5,5),np.uint8)
kernel2 = np.ones((3,3),np.uint8)
pattern = cv.erode(pattern,kernel,iterations = 1)
pattern = cv.dilate(pattern,kernel2,iterations = 1)
#part 2 find contour

contours, _ = cv.findContours(pattern, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
for k in range(len(contours)-1,-1,-1):
	if len(contours[k])<10:
		contours.pop(k)
print('Contour lengths: ', [len(i) for i in contours])

res = np.ones(pattern.shape, dtype=np.uint8) * 255
cv.drawContours(res, contours, -1, (100,100,100), thickness=cv.FILLED)

#cut pieces
pieces = []
for i in range(len(contours)):
	mask = np.ones(pattern.shape, dtype=np.uint8)*255
	cv.drawContours(mask, contours, i, (0,0,0), thickness=cv.FILLED)
	

	piece = copy.deepcopy(pre)
	piece[mask > 0] = 0
	
	x,y,w,h = cv.boundingRect(contours[i])
	print(x, y, w, h)
	pieces.append(piece[y:y+h, x:x+w])

	cv.imshow('',piece)
	cv.waitKey(0)


side = np.ceil(np.sqrt(len(pieces)))
for i in range(len(pieces)):
	plt.subplot(side, side, i+1), plt.imshow(pieces[i])
	cv.imwrite('./segmented/piece_'+str(i)+'.png', pieces[i])
	
plt.show()


