import copy
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from random import randint

# Load pieces
n_pieces = 16
pieces = []
for i in range(n_pieces):
	pieces.append(cv.imread('piece_'+str(i)+'.png', cv.IMREAD_UNCHANGED))
w_max = 0
h_max = 0
for piece in pieces:
	h,w = piece.shape[0:2]
	if h > h_max:
		h_max = h
	if w > w_max:
		w_max = w
s_max = np.round(np.sqrt(w_max**2 + h_max**2)).astype(np.int)

for i in range(len(pieces)):
	h,w = pieces[i].shape[0:2]
	bottom, right =  np.ceil(((s_max-h)/2, (s_max-w)/2)).astype(np.int)
	top, left     = np.floor(((s_max-h)/2, (s_max-w)/2)).astype(np.int)
	pieces[i] = cv.copyMakeBorder(pieces[i], top, bottom, left, right, cv.BORDER_CONSTANT, None, 0)
	
# Generate random rotations of pieces
for i in range(len(pieces)):
	angle = randint(-180,179)#/180 * np.pi
	R = cv.getRotationMatrix2D((s_max/2,s_max/2),angle,1)
	pieces[i] = cv.warpAffine(pieces[i], R, (pieces[i].shape[:2]))

# Generate background
bck_color = np.array([100, 200, 50], dtype=np.uint8)
background = np.zeros((s_max, s_max, 3), dtype=np.uint8)
for i in range(len(bck_color)):
	background[:,:,i] = bck_color[i]

	
# Put pieces in the background
side = np.ceil(np.sqrt(len(pieces))).astype(np.int)
result = np.zeros((side*s_max, side*s_max, 3), dtype=np.uint8)
n = 0
for i in range(side):
	for j in range(side):
		if n < len(pieces):
			alpha = pieces[n][:,:,3]
			dummy = copy.deepcopy(background)
			dummy[alpha > 0, :] = 0
			result[i*s_max:(i+1)*s_max, j*s_max:(j+1)*s_max] = dummy + pieces[n][:,:,:3]#cv.cvtColor(pieces[n], cv.COLOR_GRAY2BGR)
			n += 1

cv.imshow('',result)
cv.waitKey(0)

# Save result
cv.imwrite('puzzle_unsolved.jpg', result)


