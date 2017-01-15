from __future__ import division
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin

green = (0, 255, 0)

def show(image):

	#figure size in inches
	plt.figure(figsize=[10,10])
	plt.imshow(image, interpolation='nearest')

def overlay_mask(mask, image):
	#make the mask rgb
	rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
	img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
	return img

def find_biggest_contour(image):
	#copy image
	image = image.copy()
	image, contours, heirarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	#isolating the largest contour
	contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
	biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

	#return the biggest contour
	mask = np.zeros(image.shape, np.uint8)
	cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
	return biggest_contour, mask

def circle_centroids(image, centroids):
	
	image_with_centroids = image.copy()
	#add centroids
	for centroid in centroids:
		cv2.circle(image_with_centroids, centroid, 7, (0, 0, 0), -1)
	return image_with_centroids

def find_strawberry(image):
	#RGB is red green blue
	#BGR is blue green red
	#convert to the correct color scheme
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	#step2 - scale our image properly
	max_dimension = max(image.shape)
	scale = 700/max_dimension
	image = cv2.resize(image, None, fx=scale, fy=scale)

	#step3 - clean our image
	image_blur = cv2.GaussianBlur(image, (7,7), 0)

	#separates the color from the brightness of it. Luma from chroma.
	image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

	#ste4 - defining our filters
	#filter by the color
	min_red = np.array([13,100,80])
	max_red = np.array([23,256,256])

	mask1 = cv2.inRange(image_blur_hsv, min_red, max_red)

	#filter by brightness
	min_red2 = np.array([13, 100, 80])
	max_red2 = np.array([23,256,256])

	mask2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)

	#take these two masks and...
	#combine our masks

	mask = mask1 + mask2
	
	#step5 - segmentation
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
	mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)

	thresh = mask_clean.copy()
	thresh, contours, heirarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#contours = contours[1]

	ripe_oranges=[]
	for contour in contours:
		M = cv2.moments(contour)
		
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		print cX			
		print cY
		ripe_oranges.append((cX, cY))

	#step6 - Find the biggest strawberry
	#big_strawberry_contour, mask_strawberries = find_biggest_contour(mask_clean)

	#step7 - overlay
	overlay = overlay_mask(mask_clean, image)

	print ripe_oranges
	#step8 - circle the biggest strawberry
	centroids_added = circle_centroids(overlay, ripe_oranges)
	show(centroids_added)

	#step9 - convert back to original color scheme
	bgr = cv2.cvtColor(centroids_added, cv2.COLOR_RGB2BGR)

	return bgr


#read the image in 3 lines
image = cv2.imread('orangees.jpg')
result = find_strawberry(image)

#write the new image
cv2.imwrite('orangees4.jpg', result)

