# 2016-vision
Vision code used for the 2016 FRC game Stronghold.
## Overview
* The vision code itself runs on python, using OpenCV
* It runs on a raspberry pi 3 on boot
* It communicates the co-ordinates of the goal back to the RoboRIO over network tables (uses https://github.com/robotpy/pynetworktables on pi side)

###Vision code process
1. Setup (Create network table, then start video stream)
2. Take a picture
3. process picture
	1. Convert to HSV
	2. Blur image (medianBlur, 3)
	3. HSV Threshold (remove pixels outside of certain hue/saturation/value range)
	4. Canny edge detection
	5. create contour objects
	6. Add the contour to a final list if it meets the following criteria:
		* is within an area range
		* is within a perimeter range
		* It has number of sides == 6, 7 or 8
		* it's width and height are within the correct range
		* It's width/height ratio is in the correct range
		* The ratio of the perimeter of the outline (U shappe) and a box (rectangle around it) is within range
	7. Sort final contours by area, return list of contours and image with contours (pre filter) drawn on it
4. Try to add the CenterY, centerX and width to a NetworkTable
	* if it failes (because it could not find any contours) Then make Found value false (in network table)