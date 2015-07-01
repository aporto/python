# Standard imports
import cv2
import numpy as np;
import time

# Read image
im = cv2.imread("C:\\Users\\aporto\\Desktop\\whiteboard.jpg", cv2.IMREAD_GRAYSCALE)

time1 = time.time();
# Set up the detector with default parameters.

params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 100
params.maxThreshold = 150
#params.threasholdStep = 10

params.filterByArea = True
params.minArea = 50
params.filterByCircularity = False
params.filterByConvexity = True
params.minConvexity = 0.87
params.filterByInertia = False

detector = cv2.SimpleBlobDetector(params)

# Detect blobs.
keypoints = detector.detect(im)

print (time.time() - time1) * 1000
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints

cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)