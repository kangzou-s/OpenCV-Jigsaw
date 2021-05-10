# This script should take an image of the unsolved puzzle from ./puzzle_generator
# and output N smaller images, each containing one piece to folder ./segmented
import copy
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt #import function library which will be used 

for i in range(16):
#part1 spin
	pattern = cv.imread('./segmented/'+'piece_'+str(i)+'.png')
	pattern1 = cv.imread('./segmented/'+'piece_'+str(i)+'.png')


	pattern = (0.3*pattern[:,:,2] + 0.6*pattern[:,:,1] + 0.1*pattern[:,:,0]).astype(np.uint8)
	pattern = 255 * (pattern > 5 ).astype(np.uint8)

	rows = pattern.shape[0]
	cols = pattern.shape[1]

	base = np.zeros([rows*3,cols*3],dtype=np.uint8)
	base[150:150+rows,150:150+cols]=pattern
	base1 = np.zeros([rows*3,cols*3,3],dtype=np.uint8)
	base1[150:150+rows,150:150+cols,:]=pattern1[:,:,:]


	contours, _ = cv.findContours(base, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	cnt=contours[0]
	rect = cv.minAreaRect(cnt)
	M = cv.getRotationMatrix2D(rect[0],rect[2],1)
	fin = cv.warpAffine(base1,M,(cols*3,rows*3))
	fin1=fin
	cv.imshow('',fin)
	cv.waitKey(0)

# part2 cut out
	fin = (0.3*fin[:,:,2] + 0.6*fin[:,:,1] + 0.1*fin[:,:,0]).astype(np.uint8)
	fin = 255 * (fin > 5 ).astype(np.uint8)

	cv.imshow('',fin)
	cv.waitKey(0)

	contours, _ = cv.findContours(fin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	x,y,w,h = cv.boundingRect(contours[0])
	'''cv.imshow('',fin1[y:y+h, x:x+w])
	cv.waitKey(0)'''
	cv.imwrite('./segmented/piece_'+'new_'+str(i)+'.png',fin1[y:y+h, x:x+w])