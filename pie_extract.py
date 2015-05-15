import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('Percentage-pie-chart-DA-determinations.png',0)
edges = cv2.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.show()

cv2.imshow('edge', edges)
cv2.waitKey(0)
