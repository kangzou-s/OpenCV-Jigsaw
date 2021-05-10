# test circle.py 
import copy
import cv2 as cv
import numpy as np
import math
from matplotlib import pyplot as plt #import function library which will be used 
import scipy.signal

for k in range(16):
	# part1 expand pieces to prepare for further processing
	pattern = cv.imread('./segmented/piece_'+str(k)+'.png')
	base = cv.imread('./segmented/piece_'+str(k)+'.png')
	rows = pattern.shape[0]
	cols = pattern.shape[1]
	pattern1=np.zeros([rows*3,cols*3,3],dtype=np.uint8)  #pattern will be turned to gray
	pattern2=np.zeros([rows*3,cols*3,3],dtype=np.uint8)  # remain colorful to be showed
	pattern1[150:150+rows,150:150+cols,:]=base
	pattern2[150:150+rows,150:150+cols,:]=base


	# part2 contour detect and draw out
	pattern1 = (0.3*pattern1[:,:,2] + 0.6*pattern1[:,:,1] + 0.1*pattern1[:,:,0]).astype(np.uint8)
	pattern1 = 255 * (pattern1 > 5 ).astype(np.uint8)
	contours_one,_ = cv.findContours(pattern1, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)    #contours_one store the primary contours
	for k in range(len(contours_one)-1,-1,-1):
		if len(contours_one[k])<10:
			contours_one.pop(k)




	# part3 smooth contour_one
	cnt_primary = contours_one[0]
	L_primary = cv.arcLength(cnt_primary,True) 

	hull_primary = cv.convexHull(cnt_primary,returnPoints = False)
	defects_primary = cv.convexityDefects(cnt_primary,hull_primary)
	defects_primary=np.squeeze(defects_primary)
	# filter defects
	for i in range(defects_primary.shape[0]-1,-1,-1):
		s,e,f,d = defects_primary[i]
		start = tuple(cnt_primary[s][0])
		end = tuple(cnt_primary[e][0])
		far = tuple(cnt_primary[f][0]) 
		if d <= L_primary:
			defects_primary=np.delete(defects_primary,i,0)
			continue
		# print(d)         #to show convexity in pattern2
		cv.line(pattern2,start,end,[0,255,0],2) 
		cv.circle(pattern2,far,5,[0,0,255],-1)
	cv.circle(pattern2,tuple(cnt_primary[0][0]),5,[0,0,255],-1)   #mark cnt[0]    # show the initial point
	cv.imshow('pattern2',pattern2) 
	cv.waitKey(0)

	num_defects_primary=len(defects_primary)
	num_cnt_primary=len(cnt_primary)
	
	f1=defects_primary[0][2]
	f2=defects_primary[num_defects_primary-1][2]
	index_firstlast=np.hstack((np.arange(0,f1-4),np.arange(f2+4,num_cnt_primary-1)))
	cnt_firstlast=cnt_primary[index_firstlast]
	L = cv.arcLength(cnt_firstlast,True) 
	area = cv.contourArea(cnt_firstlast)
	flag = L*L/area/(4*math.pi)
	print(flag)

	for i in range(num_defects_primary-1):
		f1=defects_primary[i][2]
		f2=defects_primary[i+1][2]
		cnt_twodefects =cnt_primary[f1+4:f2-4]
		L = cv.arcLength(cnt_twodefects,True) 
		area = cv.contourArea(cnt_twodefects)
		flag = L*L/area/(4*math.pi)
		print(flag)
	print('\n')
	print('\n')
	print('\n')




















