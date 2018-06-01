## Contains all other image processing functions except finding centers in the image.

import io
import time
import picamera
import cv2
import numpy as np
from centre import *
from subprocess import call

def captureImageFast():
	## Capture image using picamera
	## TESTED : Takes ~2 seconds to click a photo
	#Initialise bit stream
	stream = io.BytesIO()
	# initialise camera
	camera_width = 1024
	camera_height = 1024
	with picamera.PiCamera() as camera:
		camera.resolution = (camera_width, camera_height)
		# caputre image using video port to capture decrease processing time
		time.sleep(1)
		camera.capture(stream, format='jpeg', use_video_port=False)
		#convert bit stream into numpy array
	data = np.fromstring(stream.getvalue(), dtype=np.uint8)
	# create opencv image object from data 
	img = cv2.imdecode(data, 1)
	return img

def captureImage():
        print "Taking Image"
	call(["raspistill", "-o", "image.jpg"])
        print "Image taken."
	image = cv2.imread("image.jpg")
	return image

def correctPerspective(image):
	## Correct the perspective of the image taken from the camera
	## TESTED : Takes ~0.6 seconds for processing
        print "Correcting Perspective"
	# pixel values of the corners of the grid image
	pts1 = np.float32([[435, 222], [2328, 132], [2084, 1857], [824, 1838]])
	# pts1 = np.float32([[426, 136], [2355, 17], [2130, 1877], [805, 1921]])
	# desired pixel values of those corners
	pts2 = np.float32([[0, 0], [1000, 0], [1000, 1304], [0, 1304]])

	# get transformation matrix for the non affine operation
	M = cv2.getPerspectiveTransform(pts1, pts2)
	# apply the transformation to correct the image
	dst = cv2.warpPerspective(image, M, (1000, 1304))
	cv2.imwrite("perspective_shift.jpg", dst)
	print "Perspective shited."
	return dst

def findCentroids(image):
        print "Finding Centroids"
	image = correctPerspective(image)
	centroids = find_orange(image)
	print "Centroids Found"
	return centroids


##image = captureImage()
##correct = correctPerspective(image)
##print "Done!"
