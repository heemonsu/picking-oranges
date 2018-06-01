## This contains functions which are used to find the centres from an RGB image.
## We use watershed algorithm for detecting the circles.
## The HSV values for thresholding are taken from trial and error, and are also somewhat ## dependent on external lighting conditions. The thresholded image and the image with
## centre is written as new files to help debug in the thresholding process, as the ## thresholded values are set manuall only, which is a limitation of our code.

from __future__ import division
import cv2
import numpy as np
from math import cos, sin
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import timeit

def show(image):

	#figure size in inches
	plt.figure(figsize=[10,10])
	plt.imshow(image, interpolation='nearest')

def overlay_mask(mask, image):
	#make the mask rgb
	rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
	img = cv2.addWeighted(rgb_mask, 0.2, image, 0.8, 0)
	return img

def watershed_centroids(image):
	## Find centroids of segments using watershed algorithm

	# Apply distance transform on the binary image
	D = ndimage.distance_transform_edt(image)

	# find local maximas
	localMax = peak_local_max(D, indices=False, min_distance=60, labels=image)
	# define markers for watershed
	markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
	# create lables to find unique segments
	labels = watershed(-D, markers, mask=image)
	print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))
	
	# initialise empty list to store centroids
	ripe_oranges = []
	# for each label/segment
	for label in np.unique(labels):
		if label ==0:
			continue

		# initialise zero matrix
		mask = np.zeros(image.shape, dtype="uint8")
		# copy each label into buffer variable
		mask[labels == label] = 255
		# find countour of the label to extract centroid
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		# take the largest countour
		c = max(cnts, key=cv2.contourArea)

		if cv2.contourArea(c) < 10000:
			continue
		# calculate moment of the contour
		M = cv2.moments(c)
		# calculate centroid
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		# crete list of centroids
		ripe_oranges.append((cX, cY))

	return ripe_oranges

def circle_centroids(image, centroids):
	
	image_with_centroids = image.copy()
	#add centroids
	for centroid in centroids:
		cv2.circle(image_with_centroids, centroid, 7, (0, 0, 0), -1)
	return image_with_centroids

def find_orange(image):
	# RGB is red green blue
	# BGR is blue green red
	# convert to the correct color scheme
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	# clean image
	image_blur = cv2.GaussianBlur(image, (21,21), 0)
	# separates the color from the brightness of it. Luma from chroma.
	image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

	# defining our filters
	# filter by the color
	# orange filter
	min_red = np.array([9,90,80])
	max_red = np.array([19,255,255])

	mask1 = cv2.inRange(image_blur_hsv, min_red, max_red)
	# green filter
	min_green = np.array([19, 90, 60])
	max_green = np.array([32, 255, 206])

	mask2 = cv2.inRange(image_blur_hsv, min_green, max_green)
	#combine our mas

	masks = [mask1, mask2]
	centroids = []
	location = ['mask_orange_.jpg', 'mask_green_.jpg']
	color = ['orange_centers_.jpg', 'green_centers_.jpg']
	kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17,17))
	kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31,31))
	kernel = [kernel1, kernel2]
	# for both the filters
	for i in range(2):

		# perform segmentation
		# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25,25))
		# dilation
		mask_closed = cv2.morphologyEx(masks[i], cv2.MORPH_CLOSE, kernel[i])
		# erosion
		mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel[i])

		cv2.imwrite(location[i], cv2.cvtColor(mask_clean, cv2.COLOR_GRAY2BGR))
		centers = watershed_centroids(mask_clean)

		# pass thresholded image to find centroids
		

		overlay = overlay_mask(mask_clean, image)

		centroids.append(centers)
		print centers

		#step8 - circle the biggest orange 
		centroids_added = circle_centroids(overlay, centers)
		#show(centroids_added)

		#step9 - convert back to original color scheme
		bgr = cv2.cvtColor(centroids_added, cv2.COLOR_RGB2BGR)
		cv2.imwrite(color[i], bgr)

	return centroids




#input_str = 'images/correct' + str(23) + '.jpg'
#image = cv2.imread('image27.jpg')
#centroids = find_orange(image)

#print centroids

# image = cv2.imread('output_images/correct3.jpg')
# centroids = find_orange(image, 31)
# print centroids

# image = cv2.imread('output_images/correct4.jpg')
# centroids = find_orange(image, 41)
# print centroids
