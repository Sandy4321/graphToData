import numpy as np
import cv2

img = cv2.imread('bar-graph.png')
# img = cv2.medianBlur(img, 3)
thresh = cv2.Canny(img,100,200)

img[thresh == 255] = 255
thresh = cv2.Canny(img,0,255)
cv2.imshow('temp', thresh)
cv2.waitKey(0)
# temp = 255 - cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB) - img

# cv2.imshow('temp', temp)
# cv2.waitKey(0)
# temp = cv2.Canny(temp,100,200)
# ret,thresh = cv2.threshold(imgray,127,255,0)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

for cnt in contours:
	approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)

	if len(approx) == 4 and len(cnt) >= 100:
		cv2.drawContours(img, cnt, -1, (255,255,0), 3)
		cv2.imshow('img', img)
		cv2.waitKey(0)

cv2.destroyWindow('img')
# for cont in contours:
# 	opencv.cvApproxPoly(cont, opencv.sizeof_CvContour, storage, opencv.CV_POLY_APPROX_DP, 3, 1)

# cv2.drawContours(img, contours, -1, (0,255,0), 3)

# cv2.imshow('sds', img)
# cv2.waitKey(0)