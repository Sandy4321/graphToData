import cv2
import numpy as np 

def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print y,',', x

def connected_component(L, img, new_img):
	result = []
	while(len(L) != 0):
		#print L
		current_y, current_x = L[0]
		result.append(L[0])
		del L[0]
		for fy in xrange(3):
			for fx in xrange(3):
				p_y = current_y+fy-3/2
				p_x = current_x+fx-3/2
				if((p_x>=0 and p_x < img.shape[1]) and (p_y>=0 and p_y < img.shape[0]) and (img[p_y, p_x] == 1)):
					img[p_y, p_x] = 0
					L.append((p_y, p_x))
					new_img[p_y, p_x] = 1
	return (result, new_img)
		
# img = np.array(
# 		[
# 			[0, 0, 0, 0, 0],
# 			[0, 1, 0, 0, 0],
# 			[1, 1, 0, 0, 0],
# 			[0, 0, 1, 0, 0],
# 			[0, 0, 1, 1, 0],
# 			[0, 0, 0, 1, 1],
# 			[0, 0, 0, 0, 0]
# 		]
# 	)

# L = [(2, 0)]
# print connected_component(L, img), img

img = cv2.imread("linegraph-redriver-single.jpeg")
cv2.imshow('image_mouse', img)
cv2.setMouseCallback('image_mouse',draw_circle)
cv2.waitKey(0)

grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

bin_image = np.zeros(grayImg.shape)
actual_color = grayImg[285 , 546]


#bin_image[(grayImg <= actual_color+20) * (grayImg >= actual_color-20)] = 1

bin_image[(grayImg <= actual_color+20) * (grayImg >= actual_color-20)] = 1

new_img = np.zeros(grayImg.shape)
L = [(285 , 546)]
connected_component(L, bin_image, new_img)

cv2.imshow('img', new_img)
cv2.waitKey(0)
# def find_line_points(y, x, img):
# 	L = [(y, x)]
# 	connected_component(L, img)

# img = cv2.imread("astracharts2.jpg")
# grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# print img[134, 66]


# for i in xrange(200):
# 	cv2.circle(img, (66+i, 134), 4, (255, 255, 255), thickness=2, lineType=8, shift=0)
# 	cv2.imshow("img", img)
# 	cv2.waitKey(33)

# cv2.destroyWindow('img')


# contours, hierarchy = cv2.findContours(grayImg, cv2.cv.CV_RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE, (0, 0))

# for b,cnt in enumerate(contours):
# 	cv2.drawContours( img, contours, b, (255, 0, 0), 2, 8, hierarchy, 0, (0, 0))
# print len(contours)
# cv2.imshow('img', img)
# cv2.waitKey(0)