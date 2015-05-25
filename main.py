import cv2
import numpy as np 
import matplotlib.pyplot as plt 

def get_point(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print y,',', x

def connected_component(L, img, new_img):
	result = []
	while(len(L) != 0):
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
		
def compare(a, b):
	y1, x1 = a
	y2, x2 = b
	return x1 - x2

#drecrease_or_increase_or_neutral -> DIN
#status descrease-> True, increase ->False, neutral -> None
def d_i_n(prev, cur):
	status = None
	if prev[0] - cur[0] < 0:
		status = False
	elif prev[0] - cur[0] > 0:
		status = True
	else:
		status = None
	return status

# L = [(217 , 56)]
# origin = (409 , 56)
# X_end = (410 , 459)
# Y_end = (49 , 55)
# X = (1, 6)
# Y = (0, 80)
# img = cv2.imread("line_example1.jpg")

img = cv2.imread("line-graph-overview-two.jpg")

size_y, size_x, size_z = img.shape
temp = {'x':	28.416666666666664, 'y': 59.5}

L = []
L.append((int(round(temp['y'] * size_y/100)), int(round(temp['x'] * size_x/100))))
print L
origin = (363 , 56)
X_end = (363 , 384)
Y_end = (35 , 56)
X = (1985, 25)
Y = (0, 5)


# L = [(234 , 145)]
# origin = (290 , 145)
# X_end = (290 , 427)
# Y_end = (103 , 145)
# X = (1985, 25)
# Y = (0, 5)
# img = cv2.imread("temp.png")


grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
bin_image = np.zeros(grayImg.shape)


# cv2.imshow('temp', img)
# cv2.setMouseCallback('temp', get_point)
# cv2.waitKey(0)



#from the actual, get all nearest closest color
actual_color = grayImg[L[0]]
bin_image[(grayImg <= actual_color+20) * (grayImg >= actual_color-20)] = 1

new_img = np.zeros(grayImg.shape)

result, new_img = connected_component(L, bin_image, new_img)

# cv2.imshow('temp', new_img)
# cv2.waitKey(0)

result = sorted(result, cmp=compare)

prev = None
new_result = []
for i in xrange(0, len(result)):
	y, x = result[i]
	if prev is None:
		prev = result[i]
		new_result.append(result[i])
	elif prev[1] != x:
		new_result.append(result[i])
		prev = result[i]

# sample_result = []
# new_img = np.zeros(new_img.shape)
# for i in xrange(0, len(new_result), len(new_result)*10/100):
# 	y, x = new_result[i]
# 	sample_result.append((y, x))
# 	new_img[y, x] = 1

#detect peak
new_img = np.zeros(new_img.shape)
sample_result = []
prev = new_result[0]
cur = new_result[1]
status = d_i_n(prev, cur)
if not status:
	prev = cur
sample_result.append(prev)

temp_status = None
for i in xrange(2, len(new_result)): 
	cur = new_result[i]
	temp_status = d_i_n(prev, cur)
	if temp_status!=None and temp_status != status:
		sample_result.append(prev)
		status = temp_status
	prev = cur


data = []
X_length = abs(X_end[1] - origin[1])
Y_length = abs(origin[0] - Y_end[1])
for i in xrange(len(sample_result)):
	cur_y, cur_x = sample_result[i]
	data.append(((origin[0] - cur_y)/float(Y_length), (cur_x - origin[1])/float(X_length)))

# print "----------------------Data----------------------"
# print data

# plt.plot([x[1] for x  in data], [x[0] for x  in data])
# plt.show()

data_scaled = []
X_length = X_end[1] - origin[1]
Y_length = origin[0] - Y_end[1]
for i in xrange(len(data)):
	cur_y, cur_x = data[i]
	data_scaled.append((Y[0]+cur_y*Y[1], X[0]+cur_x*X[1]))

# print "----------------------Scaled Data----------------------"
# print data_scaled

plt.plot([x[1] for x  in data_scaled], [x[0] for x  in data_scaled])
plt.show()