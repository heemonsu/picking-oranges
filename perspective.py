import cv2
import numpy as np
import timeit

start_time = timeit.default_timer()


img = cv2.imread('namaste_new.jpg')

pts1 = np.float32([[661, 348], [1843, 385], [463, 1911], [2165, 1853]])
pts2 = np.float32([[0, 0], [1000, 0], [0, 1000], [1000, 1000]])

M = cv2.getPerspectiveTransform(pts1, pts2)

dst = cv2.warpPerspective(img, M, (1000, 1000))

cv2.imwrite('corrected.jpg', dst)

elapsed = timeit.default_timer() - start_time

print elapsed

