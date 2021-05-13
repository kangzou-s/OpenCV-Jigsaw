# This script should take an individual structurized object of class Piece,
# orients (rotates and centers) it so that its image is not skewed and saves
# as an object to the disk in './results' folder.


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
	pattern3=np.zeros([rows*3,cols*3,3],dtype=np.uint8)  # finally rotate to horizontal and vertical
	pattern1[150:150+rows,150:150+cols,:]=base
	pattern2[150:150+rows,150:150+cols,:]=base
	pattern3[150:150+rows,150:150+cols,:]=base
	# cv.imshow('',pattern1)
	# cv.waitKey(0)
	# cv.imwrite('./segmented/piece_'+'expand_'+'11'+'.png',pattern1)


	# part2 contour detect and draw out
	pattern1 = (0.3*pattern1[:,:,2] + 0.6*pattern1[:,:,1] + 0.1*pattern1[:,:,0]).astype(np.uint8)
	pattern1 = 255 * (pattern1 > 5 ).astype(np.uint8)
	contours_one,_ = cv.findContours(pattern1, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)    #contours_one store the primary contours
	for i in range(len(contours_one)-1,-1,-1):
		if len(contours_one[i])<10:
			contours_one.pop(i)
	# # print(contours)
	gray_contour = np.ones(pattern1.shape, dtype=np.uint8)*255
	cv.drawContours(gray_contour, contours_one, -1, (0,0,0), thickness=cv.FILLED)
	cv.imshow('',gray_contour)
	cv.waitKey(0)


	#part3 smooth contour_one
	cnt_primary = contours_one[0]
	# print('len of cnt is{}'.format(len(cnt_one)))
	L_primary = cv.arcLength(cnt_primary,True) 
	# print('the arcLength of contours_one is :{}'.format(L_primary))
	# epsilon = L/6000
	# approx = cv.approxPolyDP(cnt,epsilon,True)
	# print('the length of cnt is {}'.format(len(cnt)))



	# find hull
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
	# cv.imshow('pattern2',pattern2) 
	# cv.waitKey(0)

	# find out which defects has formed circle in contours_primary
	num_defects_primary=len(defects_primary)
	num_cnt_primary=len(cnt_primary)
	index_cnt=[]

	# For defects in first and last
	s1=defects_primary[0][0]
	e1=defects_primary[0][1]
	f1=defects_primary[0][2]
	s2=defects_primary[num_defects_primary-1][0]
	e2=s2=defects_primary[num_defects_primary-1][1]
	f2=defects_primary[num_defects_primary-1][2]
	# tab_fin=[]
	index_firstlast=np.hstack((np.arange(0,f1-4),np.arange(f2+4,num_cnt_primary-1)))
	# print('index_firstlast   {}'.format(index_firstlast))
	cnt_firstlast=cnt_primary[index_firstlast]
	L = cv.arcLength(cnt_firstlast,True) 
	# print('the length of contours between two defects is :{}'.format(L))
	area = cv.contourArea(cnt_firstlast)
	# print("the boundary area enclosed by two defects is {}".format(area))
	flag = L*L/area/(4*math.pi)
	print(flag)
	if flag < 1.4:
		index_cnt =np.hstack(([f1,f1+3,f1+2,f1+1],[f2,f2-1,f2-2,f2-3]))
	else:
		index_cnt=np.hstack((np.arange(0,s1),np.arange(e2-3,num_cnt_primary-1)))
	print(index_cnt)
	 
	# For other defects
	for i in range(num_defects_primary-1):
		s1=defects_primary[i][0]
		e1=defects_primary[i][1]
		f1=defects_primary[i][2]
		s2=defects_primary[i+1][0]
		e2=defects_primary[i+1][1]
		f2=defects_primary[i+1][2]

		cnt_twodefects =cnt_primary[f1+4:f2-4]
		L = cv.arcLength(cnt_twodefects,True) 
		# print('the length of contours between two defects is :{}'.format(L))
		area = cv.contourArea(cnt_twodefects)
		# print("the boundary area enclosed by two defects is {}".format(area))
		flag = L*L/area/(4*math.pi)
		print(flag)
		if flag < 1.4:
			index_cnt=np.hstack((index_cnt,[f1-4,f1-3,f1-2,f1-1,f1,f2,f2+1,f2+2,f2+3,f2+4]))
		else:
			index_cnt=np.hstack((index_cnt,np.arange(e1-4,s2+4)))
	index_cnt.sort()    
	# print(index_cnt)
	cnt_cut_fill=cnt_primary[index_cnt]
	# print('len of cnt1 is{}'.format(len(cnt1)))

	# print('The indix of which can form tabs are as these {}'.format(tab_fin))
	 
	# # print tht contour cut out tabs
	pattern_rectangle = np.ones(pattern1.shape, dtype=np.uint8)*0
	cv.drawContours(pattern_rectangle, cnt_cut_fill, -1, (255,255,255), thickness=cv.FILLED)
	cv.imshow('',pattern_rectangle)
	cv.waitKey(0)
	contours_rectangle,_ = cv.findContours(pattern_rectangle,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
	test=np.ones(pattern1.shape, dtype=np.uint8)*255
	cv.drawContours(test, contours_rectangle, -1, (0,0,0), thickness=cv.FILLED)
	cv.imshow('',test)
	cv.waitKey(0)




	#part3 change origin from top-left to center of mass
	# M=cv.moments(cnt_cut_fill)
	# Cx = int(M['m10']/M['m00'])
	# Cy = int(M['m01']/M['m00'])
	# for i in range(len(cnt_cut_fill)):
	# 	cnt_cut_fill[i][0][0],cnt_cut_fill[i][0][1] =  cnt_cut_fill[i][0][1],cnt_cut_fill[i][0][0] #change from (y,x) to (x,y)
	# 	cnt_cut_fill[i][0][0] -= Cx
	# 	cnt_cut_fill[i][0][1] -= Cy

	# #use two new variable to store coordinates, finally coor stores the (phi,rho) and give the value to phi,rho
	# coor = cnt_cut_fill
	# phi=np.ones([1,len(coor)],dtype=np.float)
	# rho=np.ones([1,len(coor)],dtype=np.float)
	# for i in range(len(coor)): 
	# 	phi[0,i]=math.atan2(coor[i][0][1],coor[i][0][0])
	# 	rho[0,i]=np.linalg.norm([coor[i][0][0],coor[i][0][1]])
	# rho_final=rho[0]
	# phi_final=phi[0]
		
	# # show (phi) and peak of phi 
	# plt.plot(rho_final)
	# plt.title('rho of the piece contour')
	# peaks,_ =scipy.signal.find_peaks(rho_final,distance=15,height=[80,90])
	# plt.plot(peaks,rho_final[peaks],'x')
	# plt.show()

	
		
# rotate to horizontal and vertical and cropping
	rect = cv.minAreaRect(cnt_cut_fill)
	M = cv.getRotationMatrix2D(rect[0],rect[2],1)
	pattern3 = cv.warpAffine(pattern3,M,(cols*3,rows*3))
	cv.imshow('',pattern3)
	cv.waitKey(0)

	fin =pattern3.copy()
	fin1=pattern3.copy()
	fin = (0.3*fin[:,:,2] + 0.6*fin[:,:,1] + 0.1*fin[:,:,0]).astype(np.uint8)
	fin = 255 * (fin > 5 ).astype(np.uint8)
	contours, _ = cv.findContours(fin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	x,y,w,h = cv.boundingRect(contours[0])
	pattern3 = fin1[y:y+h, x:x+w]


	cv.imwrite('./results/piece_'+'new_'+str(k)+'.png',pattern3)

# Present all results on one graph
for i in range(16):
	plt.subplot(4, 4, i+1)
	img=cv.imread('./results/piece_'+'new_'+str(i)+'.png')
	plt.imshow(img)
plt.show()

