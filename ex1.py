import copy
import cv2 as cv
import numpy as np
import math
from matplotlib import pyplot as plt #import function library which will be used 
import scipy.signal
# This is the backup of ex.py


# part1 expand pieces to prepare for further processing
pattern = cv.imread('./segmented/piece_'+str(2)+'.png')
base = cv.imread('./segmented/piece_'+str(2)+'.png')
rows = pattern.shape[0]
cols = pattern.shape[1]
pattern1=np.zeros([rows*3,cols*3,3],dtype=np.uint8)  #pattern will be turned to gray
pattern2=np.zeros([rows*3,cols*3,3],dtype=np.uint8)  # remain colorful to be showed
pattern1[150:150+rows,150:150+cols,:]=base
pattern2[150:150+rows,150:150+cols,:]=base
# cv.imshow('',pattern1)
# cv.waitKey(0)
# cv.imwrite('./segmented/piece_'+'expand_'+'11'+'.png',pattern1)


# part2 contour detect and draw out
pattern1 = (0.3*pattern1[:,:,2] + 0.6*pattern1[:,:,1] + 0.1*pattern1[:,:,0]).astype(np.uint8)
pattern1 = 255 * (pattern1 > 5 ).astype(np.uint8)
contours_one,_ = cv.findContours(pattern1, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)    #contours_one store the primary contours
for k in range(len(contours_one)-1,-1,-1):
	if len(contours_one[k])<10:
		contours_one.pop(k)
# # print(contours)
# gray_contour = np.ones(pattern1.shape, dtype=np.uint8)*255
# cv.drawContours(gray_contour, contours_one, -1, (0,0,0), thickness=cv.FILLED)
# cv.imshow('',gray_contour)
# cv.waitKey(0)


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
# print("Here are the defects")
# print(defects)
# print('\n')
cv.imshow('pattern2',pattern2) 
cv.waitKey(0)
# print(defects)

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
	# tab_flag1=[a]
	# tab_flag2=[b]
	index_cnt =np.hstack(([f1],[f2]))
else:
	# tab_flag1=np.arange(0,a)
	# tab_flag2=np.arange(b,len(cnt-1))
	index_cnt=np.hstack((np.arange(0,s1),np.arange(e2,num_cnt_primary-1)))
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
		index_cnt=np.hstack((index_cnt,[f1,f2]))
	else:
		index_cnt=np.hstack((index_cnt,np.arange(e1,s2)))
index_cnt.sort()
print(index_cnt)
cnt_cut_fill=cnt_primary[index_cnt]
# print('len of cnt1 is{}'.format(len(cnt1)))

# print('The indix of which can form tabs are as these {}'.format(tab_fin))
 
# # print tht contour cut out tabs
test = np.ones(pattern1.shape, dtype=np.uint8)*255
cv.drawContours(test, cnt_cut_fill, -1, (0,0,0), thickness=cv.FILLED)
cv.imshow('',test)
cv.waitKey(0)
