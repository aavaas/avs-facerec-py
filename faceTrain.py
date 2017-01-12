#/usr/bin/env python
import numpy as np
import cv2

def detect(img, cascade):
	rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(100, 100), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
	if len(rects) == 0:
		return []
	rects[:,2:] += rects[:,:2]
	return rects

def draw_rects(img, rects, color):
	for x1, y1, x2, y2 in rects:
		cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
		break

if __name__ == '__main__':
	import sys 
	
	video_src = 0
	cascade_fn = "Haar/haarcascade_frontalface_alt.xml"    

	cascade = cv2.CascadeClassifier(cascade_fn)

	cam = cv2.VideoCapture(0)
	imgno = 1
	while True:
		ret, img = cam.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#gray = cv2.equalizeHist(gray)
		gray = cv2.GaussianBlur(gray,(7,7),0)
		
		rects = detect(gray, cascade)
		
		if len(rects) != 0:			
			for x1, y1, x2, y2 in rects:
				roi = gray[y1:y2, x1:x2]
				break
			roi = cv2.equalizeHist(roi)
			cv2.imshow('face',roi)
		
		draw_rects(gray, rects, (0, 255, 0)) 
		cv2.imshow('facedetect', gray)
		
		key = 0xFF & cv2.waitKey(1)
		
		
		if key == ord(' '):
			if len(rects) != 0:	
				
				roi =cv2.resize(roi, (92,112))
				cv2.imwrite(str(imgno)+".bmp", roi)
				imgno += 1
			
		
		if  key == 27:
			break
	
	cv2.destroyAllWindows()
		
	

