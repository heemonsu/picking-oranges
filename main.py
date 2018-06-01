from imageProcessing import *
from movements import *
import time
import timeit
start = timeit.default_timer()
# Capture image from camera
## TESTED
image = captureImage()

# Calculate centroids from the image taken
## TESTED
centroids = findCentroids(image)
# centroids = [[(588, 446), (554, 971)],[]]

# transform all centroids into world coordinates
## TESTED
coordinates = []
for maturity in centroids:
    coordinate_maturity = []
    for centroid in maturity:
        coordinate_maturity.append(transformToWorld(centroid))
    coordinates.append(coordinate_maturity)

RIPE_BOX = [20, 25]
RAW_BOX = [-20, 25]
destination = [RIPE_BOX, RAW_BOX]

# Go to coordinate, pick orange, drop in the correct box, again go to intial position
i = -1
for maturity in coordinates:
    i += 1
    for coordinate in maturity:
        placeOrange(coordinate, i)

elapsed = timeit.default_timer() - start
print elapsed
