# This script should take an image of the unsolved puzzle from ./puzzle_generator
# and output N smaller images, each containing one piece to folder ./segmented
import copy
import cv2 as cv
import numpy as np
import math
from matplotlib import pyplot as plt #import function library which will be used 
import scipy.signal

#part1 Pretreatment  enlarge the picture
pattern = cv.imread('./segmented/piece_6.png')
base = cv.imread('./segmented/piece_6.png')
rows = base.shape[0]
cols = base.shape[1]
pattern1 = np.zeros([rows*3,cols*3,3],dtype=np.uint8)
pattern1[150:150+rows,150:150+cols]=base
cv.imshow('',pattern1)
cv.waitKey(0)

pattern=np.zeros([rows*3,cols*3,3],dtype=np.uint8)
pattern=pattern1
pattern = (0.3*pattern[:,:,2] + 0.6*pattern[:,:,1] + 0.1*pattern[:,:,0]).astype(np.uint8)
pattern = 255 * (pattern > 5 ).astype(np.uint8)
cv.imshow('',pattern)
cv.waitKey(0)


#part2 get contours and make a convert for uint to float
contours, _ = cv.findContours(pattern, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cnt=contours[0]
contours = [list(map(float,point[0])) for point in contours[0]]


#part3 change origin from top-left to center of mass
M=cv.moments(cnt)
Cx = int(M['m10']/M['m00'])
Cy = int(M['m01']/M['m00'])
for i in range(len(contours)):
	contours[i][0],contours[i][1]  = contours[i][1],contours[i][0]  #change from (y,x) to (x,y)
	contours[i][0] -= Cx
	contours[i][1] -= Cy

#part4  use two new variable to store coordinates, finally coor stores the (phi,rho) and give the value to phi,rho
coor = contours
print(contours)
phi=np.ones([1,len(coor)],dtype=np.float)
rho=np.ones([1,len(coor)],dtype=np.float)
for i in range(len(coor)): 
	phi[0][i]=math.atan2(coor[i][1],coor[i][0])
	rho[0][i]=np.linalg.norm([coor[i][0],coor[i][1]])
rho_final=rho[0]
phi_final=phi[0]
	
#part5  print (phi) and peak of phi 
print(rho_final)
plt.plot(rho_final)
plt.title('rho of the piece contour')
peaks,_ =scipy.signal.find_peaks(rho_final,distance=15,height=[80,90])
#print(peaks)
plt.plot(peaks,rho_final[peaks],'x')
plt.show()

# # print(phi_final[peaks[0:4]])
# rot_angle =math.fsum(phi_final[peaks[0:4]])/4

# M = cv.getRotationMatrix2D((Cx,Cy),(-(rot_angle*180/math.pi)),1)
# pattern1 = cv.warpAffine(pattern1,M,(cols*3,rows*3))
# # cv.imshow('',pattern1)
# # cv.waitKey(0)


# # part6 cut out
# fin =pattern1.copy()
# fin1=pattern1.copy()
# fin = (0.3*fin[:,:,2] + 0.6*fin[:,:,1] + 0.1*fin[:,:,0]).astype(np.uint8)
# fin = 255 * (fin > 5 ).astype(np.uint8)


# contours, _ = cv.findContours(fin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# x,y,w,h = cv.boundingRect(contours[0])
# cv.imshow('',fin1[y:y+h, x:x+w])
# cv.waitKey(0)
# cv.imwrite('./segmented/piece_'+'new_'+'6'+'.png',fin1[y:y+h, x:x+w])



