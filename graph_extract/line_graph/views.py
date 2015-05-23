from django.shortcuts import render
import cv2
import numpy as np 
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib

# Create your views here.

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
	return status

# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(url):
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

@csrf_exempt
def extract_line(request):
	jsonData = None
	if request.method == 'POST':
		request_data = request.POST.get('request_data')
		data = json.loads(request_data)

		img = url_to_image(data['image_path'])

		size_y, size_x, size_z = img.shape

		size = data['points'][3]
		L = []
		L.append((int(round(size['y'] * size_y/100)), int(round(size['x'] * size_x/100))))
		
		origin_dict = data['points'][0]
		origin = (origin_dict['y'] * size_y/100, origin_dict['x'] * size_x/100)

		X_end_dict = data['points'][1]
		X_end = (X_end_dict['y'] * size_y/100, X_end_dict['x'] * size_x/100)

		Y_end_dict = data['points'][2]
		Y_end = (Y_end_dict['y'] * size_y/100, Y_end_dict['x'] * size_x/100)

		grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		bin_image = np.zeros(grayImg.shape)

		#from the actual, get all nearest closest color
		actual_color = grayImg[L[0]]
		bin_image[(grayImg <= actual_color+20) * (grayImg >= actual_color-20)] = 1

		new_img = np.zeros(grayImg.shape)

		result, new_img = connected_component(L, bin_image, new_img)

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
			if  temp_status != status:
				sample_result.append(prev)
				status = temp_status
			prev = cur

		data = []
		X_length = X_end[1] - origin[1]
		Y_length = origin[0] - Y_end[1]
		for i in xrange(len(sample_result)):
			cur_y, cur_x = sample_result[i]
			data.append((abs(cur_y - origin[0])/float(Y_length), abs(cur_x - origin[1])/float(X_length)))

		X = ["x"]
		Y = ["y"]
		for y, x in data:
			X.append(round(x*100, 3))
			Y.append(round(y*100, 3))

		print "----------------------Data----------------------"
		data = {
			"data": {
				"x":"x",
				"columns" : [
					X,
					Y
				]
			}
		}

		jsonData = json.dumps(data)
	print jsonData
	return HttpResponse(jsonData, content_type='application/json')
