#importing libraries

import numpy as np 
import cv2
import math


#opens camera while for continous feed

capture = cv2.VideoCapture(0)

while capture.isOpened():

	
#to capture frames from the camera

	ret, frame = capture.read()


#get hand date from the rectangle window 

	cv2.rectangle(frame, (100,100), (300,300), (0,255,0), 0)
	crop_image = frame[100:300, 100:300

#apply gaussian blur
	blur = cv2.GaussianBlur(crop_image, (3, 3), 0)
	
#change color from BGR to HSV

	hsv = cv2.cvtcolor(blur, cv2.COLOR_BGR2HSV)

#create a binary image with where white will be skin color and rest is black
	mask2 = sv2.inRange(hsv, np.array([2,0,0]), np.array([2,0,0]))

#kernal for morphological transformation

	kernal = np.ones([5,5])

#apply morphological tranformation  to filter  out the background noise

	dilation = cv2.dilate(mask2, kernal, iterations=1)
	erosion = cv2.erode(dilation, kernal, iterations=1)

#gussion blur and threshold

	filtered = cv2.GaussianBlur(erosion, (3,3), 0)
	ret, thresh = cv2.threshold(filtered, 127, 255, 0)

#show threshold image 

	cv2.imshow("Thresholded", thresh)

#find contours 

	image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	try:
		# Find contour with maximum area
		contour = max(contours, key=lambda x: cv2.contourArea(x))

		# Create bounding rectangle around the contour
		x, y, w, h = cv2.boundingRect(contour)
		cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)

		# Find convex hull
		hull = cv2.convexHull(contour)

		# Draw contour
		drawing = np.zeros(crop_image.shape, np.uint8)
		cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
		cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

		# Find convexity defects
		hull = cv2.convexHull(contour, returnPoints=False)
		defects = cv2.convexityDefects(contour, hull)

		# Use cosine rule to find angle of the far point from the start and end point i.e. the convex points (the finger
		# tips) for all defects
		count_defects = 0

		for i in range(defects.shape[0]):
			s, e, f, d = defects[i, 0]
			start = tuple(contour[s][0])
			end = tuple(contour[e][0])
			far = tuple(contour[f][0])

			a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
			b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
			c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
			angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

			# if angle > 90 draw a circle at the far point
			if angle <= 90:
				count_defects += 1
				cv2.circle(crop_image, far, 1, [0, 0, 255], -1)

			cv2.line(crop_image, start, end, [0, 255, 0], 2)

		# Print number of fingers
		if count_defects == 0:
			cv2.putText(frame, "ONE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2)
		elif count_defects == 1:
			cv2.putText(frame, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		elif count_defects == 2:
			cv2.putText(frame, "THREE", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		elif count_defects == 3:
			cv2.putText(frame, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		elif count_defects == 4:
			cv2.putText(frame, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		else:
			pass
	except:
		pass

	# Show required images
	cv2.imshow("Gesture", frame)
	all_image = np.hstack((drawing, crop_image))
	cv2.imshow('Contours', all_image)

	# Close the camera if 'q' is pressed
	if cv2.waitKey(1) == ord('q'):
 		break
capture.release()
cv2.destroyAllWindows()

