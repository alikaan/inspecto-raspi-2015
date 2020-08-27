import cv2
import numpy as np 
import os

capture = cv2.VideoCapture(0)

width = 320
height = 240

if capture.isOpened():
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
	ret, frame = capture.read()
	imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	imgGrayScale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	imgBlurred = cv2.GaussianBlur(imgGrayScale, (5, 5), 0)
	imgCanny = cv2.Canny(imgBlurred, 100, 200)

	cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)        
	cv2.namedWindow("imgGrayScale", cv2.WINDOW_AUTOSIZE)
	cv2.namedWindow("imgHSV",cv2.WINDOW_AUTOSIZE)
	cv2.namedWindow("imgBlurred",cv2.WINDOW_AUTOSIZE)
	cv2.namedWindow("imgCanny",cv2.WINDOW_AUTOSIZE)         

	cv2.imshow("imgOriginal", frame)         
	cv2.imshow("imgGrayScale", imgGrayScale)
	cv2.imshow("imgHSV",imgHSV)
	cv2.imshow("imgBlurred",imgBlurred)
	cv2.imshow("imgCanny",imgCanny)

	if cv2.waitKey(10) == 27:
		break

cv.DestroyAllWindows() 
